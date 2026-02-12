from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..models.graph import Graph
from ..core.renderer import Renderer, RenderError
import json
import asyncio

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/preview")
async def websocket_preview(websocket: WebSocket):
    """WebSocket endpoint for real-time preview"""
    await websocket.accept()

    # Get storage from app state
    storage = websocket.app.state.storage
    renderer = Renderer(storage)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "render":
                # Extract graph data
                graph_data = message.get("graph")
                if not graph_data:
                    await websocket.send_json({
                        "type": "error",
                        "message": "No graph data provided"
                    })
                    continue

                try:
                    # Parse graph
                    graph = Graph(**graph_data)

                    # Send status update
                    await websocket.send_json({
                        "type": "status",
                        "message": "Starting render..."
                    })

                    # Render preview
                    async def progress_callback(msg: str):
                        await websocket.send_json({
                            "type": "progress",
                            "message": msg
                        })

                    output_file, python_code = await renderer.render_preview(
                        graph=graph,
                        progress_callback=progress_callback
                    )

                    # Send video URL (relative to temp directory)
                    relative_path = output_file.relative_to(storage.temp_dir)
                    await websocket.send_json({
                        "type": "complete",
                        "video_url": f"/temp/{relative_path}",
                        "code": python_code
                    })

                except RenderError as e:
                    error_payload = {
                        "type": "error",
                        "message": f"Render failed: {str(e)}",
                        "code": e.code,
                    }
                    if e.node_id:
                        error_payload["node_id"] = e.node_id
                    await websocket.send_json(error_payload)
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unexpected error: {str(e)}"
                    })

            elif message.get("type") == "ping":
                # Keepalive
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
