from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from ..models.graph import Graph
from ..core.renderer import ExportQueue
from .dependencies import get_export_queue

router = APIRouter(prefix="/api/export", tags=["export"])


class ExportRequest(BaseModel):
    """Request to export a graph"""
    graph: Graph
    quality: str = Field(default="1080p", pattern="^(480p|720p|1080p|1440p|2160p)$")
    fps: int = Field(default=30, ge=15, le=60)
    format: str = Field(default="mp4", pattern="^(mp4|gif)$")


class ExportStatus(BaseModel):
    """Export job status"""
    job_id: str
    status: str
    progress: float
    error: str | None = None
    download_url: str | None = None
    log: list[str] = []


@router.post("", response_model=dict)
async def start_export(request: ExportRequest, export_queue: ExportQueue = Depends(get_export_queue)):
    """Start a new export job"""
    try:
        job_id = export_queue.create_job(
            graph=request.graph,
            quality=request.quality,
            fps=request.fps,
            format=request.format,
        )

        return {
            "job_id": job_id,
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=ExportStatus)
async def get_export_status(job_id: str, export_queue: ExportQueue = Depends(get_export_queue)):
    """Get export job status"""
    job = export_queue.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    download_url = None
    if job.status == "completed" and job.output_file:
        download_url = f"/api/export/{job_id}/download"

    return ExportStatus(
        job_id=job.job_id,
        status=job.status,
        progress=job.progress,
        error=job.error,
        download_url=download_url,
        log=job.log
    )


@router.get("/{job_id}/download")
async def download_export(job_id: str, export_queue: ExportQueue = Depends(get_export_queue)):
    """Download exported video"""
    job = export_queue.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Export not completed")

    if not job.output_file or not job.output_file.exists():
        raise HTTPException(status_code=404, detail="Output file not found")

    is_gif = str(job.output_file).endswith('.gif')
    media_type = "image/gif" if is_gif else "video/mp4"
    ext = "gif" if is_gif else "mp4"

    return FileResponse(
        path=str(job.output_file),
        media_type=media_type,
        filename=f"animation_{job_id}.{ext}"
    )
