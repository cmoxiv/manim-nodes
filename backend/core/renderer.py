import asyncio
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Callable
from .code_generator import CodeGenerator
from .storage import StorageManager
from ..models.graph import Graph


class RenderError(Exception):
    """Raised when rendering fails"""
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code


class Renderer:
    """Handles MANIM rendering for preview and export"""

    def __init__(self, storage: StorageManager):
        self.storage = storage

    async def render_preview(
        self,
        graph: Graph,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> tuple[Path, str]:
        """
        Render graph for preview (low quality, fast).

        Args:
            graph: Graph to render
            progress_callback: Optional callback for progress updates

        Returns:
            Tuple of (Path to rendered video file, Generated Python code)

        Raises:
            RenderError if rendering fails
        """
        return await self._render(
            graph=graph,
            quality="low",
            fps=15,
            progress_callback=progress_callback
        )

    async def render_export(
        self,
        graph: Graph,
        quality: str = "1080p",
        fps: int = 30,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> tuple[Path, str]:
        """
        Render graph for export (high quality).

        Args:
            graph: Graph to render
            quality: Quality preset (480p, 720p, 1080p, 1440p, 2160p)
            fps: Frames per second
            progress_callback: Optional callback for progress updates

        Returns:
            Tuple of (Path to rendered video file, Generated Python code)

        Raises:
            RenderError if rendering fails
        """
        quality_map = {
            "480p": "low",
            "720p": "medium",
            "1080p": "high",
            "1440p": "high",
            "2160p": "high"
        }

        return await self._render(
            graph=graph,
            quality=quality_map.get(quality, "high"),
            fps=fps,
            progress_callback=progress_callback
        )

    async def _render(
        self,
        graph: Graph,
        quality: str,
        fps: int,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> tuple[Path, str]:
        """
        Internal method to render graph.

        Args:
            graph: Graph to render
            quality: Quality preset (low, medium, high)
            fps: Frames per second
            progress_callback: Optional callback for progress updates

        Returns:
            Tuple of (Path to rendered video file, Generated Python code)

        Raises:
            RenderError if rendering fails
        """
        # Generate Python code
        try:
            generator = CodeGenerator(graph)
            python_code = generator.generate()
        except Exception as e:
            raise RenderError(f"Code generation failed: {str(e)}")

        # Create temporary Python file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            dir=self.storage.temp_dir
        ) as f:
            f.write(python_code)
            python_file = Path(f.name)

        try:
            # Prepare manim command
            quality_flags = {
                "low": ["-ql", "--format=mp4"],  # 480p, 15fps
                "medium": ["-qm", "--format=mp4"],  # 720p, 30fps
                "high": ["-qh", "--format=mp4"],  # 1080p, 60fps
            }

            cmd = [
                "manim",
                "render",
                str(python_file),
                "GeneratedScene",
                *quality_flags.get(quality, quality_flags["medium"]),
                f"--frame_rate={fps}",
                "--disable_caching"
            ]

            if progress_callback:
                progress_callback("Starting render...")

            # Run manim command
            # Ensure /Library/TeX/texbin is on PATH so dvisvgm can find TeX resources
            env = os.environ.copy()
            tex_bin = "/Library/TeX/texbin"
            if tex_bin not in env.get("PATH", ""):
                env["PATH"] = tex_bin + ":" + env.get("PATH", "")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.storage.temp_dir),
                env=env,
            )

            # Stream output
            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                line_str = line.decode().strip()
                if progress_callback and line_str:
                    progress_callback(line_str)

            # Wait for completion
            await process.wait()

            if process.returncode != 0:
                stderr = await process.stderr.read()
                error_msg = stderr.decode()
                raise RenderError(f"Manim rendering failed:\n{error_msg}", code=python_code)

            # Find output video file
            # Manim outputs to media/videos/[filename]/[quality]/[scene].mp4
            media_dir = self.storage.temp_dir / "media" / "videos" / python_file.stem
            output_file = None

            for quality_dir in media_dir.rglob("*.mp4"):
                output_file = quality_dir
                break

            if not output_file or not output_file.exists():
                raise RenderError("Output video file not found")

            return output_file, python_code

        except RenderError:
            raise
        except Exception as e:
            raise RenderError(f"Rendering failed: {str(e)}")
        finally:
            # Clean up temporary Python file
            try:
                python_file.unlink()
            except Exception:
                pass


class ExportJob:
    """Represents an export job"""

    def __init__(self, job_id: str, graph: Graph, quality: str, fps: int):
        self.job_id = job_id
        self.graph = graph
        self.quality = quality
        self.fps = fps
        self.status = "pending"  # pending, running, completed, failed
        self.progress = 0.0
        self.error: Optional[str] = None
        self.output_file: Optional[Path] = None
        self.log: list[str] = []

    def add_log(self, message: str):
        """Add log message"""
        self.log.append(message)


class ExportQueue:
    """Manages background export jobs"""

    def __init__(self, storage: StorageManager, renderer: Renderer):
        self.storage = storage
        self.renderer = renderer
        self.jobs: dict[str, ExportJob] = {}

    def create_job(self, graph: Graph, quality: str = "1080p", fps: int = 30) -> str:
        """
        Create a new export job.

        Args:
            graph: Graph to export
            quality: Quality preset
            fps: Frames per second

        Returns:
            Job ID
        """
        import uuid
        job_id = str(uuid.uuid4())
        job = ExportJob(job_id, graph, quality, fps)
        self.jobs[job_id] = job

        # Start job in background
        asyncio.create_task(self._run_job(job))

        return job_id

    def get_job(self, job_id: str) -> Optional[ExportJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    async def _run_job(self, job: ExportJob):
        """Run export job"""
        job.status = "running"
        job.add_log("Starting export...")

        try:
            # Render
            output_file, _ = await self.renderer.render_export(
                graph=job.graph,
                quality=job.quality,
                fps=job.fps,
                progress_callback=lambda msg: job.add_log(msg)
            )

            # Move to exports directory
            final_path = self.storage.exports_dir / f"{job.job_id}.mp4"
            output_file.rename(final_path)

            job.output_file = final_path
            job.status = "completed"
            job.progress = 100.0
            job.add_log("Export completed successfully")

        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            job.add_log(f"Export failed: {str(e)}")
