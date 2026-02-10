from pydantic import Field
from typing import Dict
from .base import NodeBase


class SetCameraOrientationNode(NodeBase):
    """Set 3D camera orientation (phi, theta, gamma angles)"""
    order: int = Field(default=0, ge=-100, le=100, description="Execution order (lower = earlier)")
    phi: str = Field(default="75.0", description="Elevation angle (degrees)")
    theta: str = Field(default="-45.0", description="Azimuth angle (degrees)")
    gamma: str = Field(default="0.0", description="Roll angle (degrees)")
    run_time: str = Field(default="1.0", description="Animation duration (0=instant)")

    def to_manim_code(self, var_name: str) -> str:
        phi_rad = f"np.radians({self.phi})"
        theta_rad = f"np.radians({self.theta})"
        gamma_rad = f"np.radians({self.gamma})"
        return f'{var_name} = CameraMove(self, phi={phi_rad}, theta={theta_rad}, gamma={gamma_rad}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Camera"


class MoveCameraNode(NodeBase):
    """Move camera to a position"""
    order: int = Field(default=0, ge=-100, le=100, description="Execution order (lower = earlier)")
    position: str = Field(default="[0, 0, 0]", description="Camera target position [x, y, z]")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = CameraMove(self, frame_center={self.position}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "camera_out": "Camera"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Camera"


class ZoomCameraNode(NodeBase):
    """Zoom camera (scale the frame)"""
    order: int = Field(default=0, ge=-100, le=100, description="Execution order (lower = earlier)")
    scale: str = Field(default="2.0")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = CameraMove(self, zoom={self.scale}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "camera_out": "Camera"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Camera"


