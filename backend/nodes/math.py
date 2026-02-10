from pydantic import Field
from typing import Dict
from .base import NodeBase


class AxesNode(NodeBase):
    """Creates coordinate axes"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    x_range_min: str = Field(default="-10.0")
    x_range_max: str = Field(default="10.0")
    y_range_min: str = Field(default="-10.0")
    y_range_max: str = Field(default="10.0")
    x_length: str = Field(default="10.0")
    y_length: str = Field(default="6.0")
    x_step: str = Field(default="1.0", description="Tick spacing (X)")
    y_step: str = Field(default="1.0", description="Tick spacing (Y)")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Axes(x_range=[{self.x_range_min}, {self.x_range_max}, {self.x_step}], y_range=[{self.y_range_min}, {self.y_range_max}, {self.y_step}], x_length={self.x_length}, y_length={self.y_length})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_position": "Vec3"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"axes": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class NumberPlaneNode(NodeBase):
    """Creates a number plane (grid)"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    x_range_min: str = Field(default="-10.0")
    x_range_max: str = Field(default="10.0")
    y_range_min: str = Field(default="-10.0")
    y_range_max: str = Field(default="10.0")
    x_step: str = Field(default="1.0", description="Major grid line spacing (X)")
    y_step: str = Field(default="1.0", description="Major grid line spacing (Y)")
    faded_line_ratio: str = Field(default="4", description="Minor lines per major line")
    major_line_opacity: str = Field(default="0.3", description="Major grid line opacity")
    minor_line_opacity: str = Field(default="0.1", description="Minor grid line opacity")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = NumberPlane(x_range=[{self.x_range_min}, {self.x_range_max}, {self.x_step}], y_range=[{self.y_range_min}, {self.y_range_max}, {self.y_step}], faded_line_ratio={self.faded_line_ratio}, background_line_style={{"stroke_opacity": {self.major_line_opacity}}}, faded_line_style={{"stroke_opacity": {self.minor_line_opacity}}})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_position": "Vec3"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"plane": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class MathTexNode(NodeBase):
    """Creates mathematical text (LaTeX)"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    tex: str = Field(default="x^2 + y^2 = r^2")
    font_size: str = Field(default="48.0")
    color: str = Field(default="#FFFFFF")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        escaped_tex = self.tex.replace('"', '\\"')
        code = f'{var_name} = MathTex(r"{escaped_tex}", font_size={self.font_size}, color={{param_color}})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"tex": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class VectorNode(NodeBase):
    """Creates a vector (arrow from origin)"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    direction: str = Field(default="[2, 3, 0]", description="Vector direction [x, y, z]")
    color: str = Field(default="#FFFFFF")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Vector({{param_position}}, color={{param_color}})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"vector": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class DotNode(NodeBase):
    """Creates a dot/point"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    position: str = Field(default="[0, 0, 0]", description="Position [x, y, z]")
    radius: str = Field(default="0.08")
    color: str = Field(default="#FFFFFF")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Dot(point={{param_position}}, radius={{param_radius}}, color={{param_color}})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_radius": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"dot": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class LinePlotNode(NodeBase):
    """Plots data points on an Axes (scatter, line, or both)"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    points: str = Field(default="[[0,0],[1,2],[2,1],[3,3]]", description="List of [x,y] data points")
    mode: str = Field(default="both", description="Plot mode: scatter, line, or both")
    dot_radius: str = Field(default="0.06", description="Radius of scatter dots")
    color: str = Field(default="#58C4DD")
    stroke_width: str = Field(default="2.0", description="Line stroke width")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        pfx = f"_{var_name}"
        parts = [f"{pfx}_pts = {self.points}"]
        parts.append(f"{pfx}_scene = [{{input_axes}}.coords_to_point(p[0], p[1]) for p in {pfx}_pts]")
        if self.mode in ("scatter", "both"):
            parts.append(f"{pfx}_dots = VGroup(*[Dot(point=p, radius={self.dot_radius}, color={{param_color}}) for p in {pfx}_scene])")
        if self.mode in ("line", "both"):
            parts.append(f"{pfx}_line = VMobject(color={{param_color}}, stroke_width={self.stroke_width})")
            parts.append(f"{pfx}_line.set_points_as_corners({pfx}_scene)")
        if self.mode == "both":
            parts.append(f"{var_name} = VGroup({pfx}_dots, {pfx}_line)")
        elif self.mode == "scatter":
            parts.append(f"{var_name} = {pfx}_dots")
        else:
            parts.append(f"{var_name} = {pfx}_line")
        if self.z_index != "0":
            parts.append(f"{var_name}.set_z_index({self.z_index})")
        return "\n        ".join(parts)

    def get_inputs(self) -> Dict[str, str]:
        return {
            "axes": "Mobject",
            "param_color": "Color",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"plot": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "mode" in schema["properties"]:
            schema["properties"]["mode"]["enum"] = ["scatter", "line", "both"]
        return schema


class PolylineNode(NodeBase):
    """Standalone path through scene-coordinate points"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    points: str = Field(default="[[-2,0,0],[0,2,0],[2,0,0]]", description="List of [x,y,z] points")
    closed: str = Field(default="false", description="Close path into polygon")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        if self.closed == "true":
            code = f'{var_name} = Polygon(*{self.points}, color={{param_color}}, stroke_width={self.stroke_width}, fill_opacity={self.fill_opacity})'
        else:
            parts = [f'{var_name} = VMobject(color={{param_color}}, stroke_width={self.stroke_width}, fill_opacity={self.fill_opacity})']
            parts.append(f'{var_name}.set_points_as_corners({self.points})')
            code = "\n        ".join(parts)
        if self.z_index != "0":
            code += f'\n        {var_name}.set_z_index({self.z_index})'
        code += f'\n        {var_name}.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_color": "Color",
            "param_position": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "closed" in schema["properties"]:
            schema["properties"]["closed"]["enum"] = ["false", "true"]
        return schema


class DisplayMatrixNode(NodeBase):
    """Displays a Matrix or Vec3 as a visual Manim Matrix mobject"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    mode: str = Field(default="matrix", description="Display mode: matrix or vector")
    scale: str = Field(default="0.8", description="Scale factor")
    matrix: str = Field(default="[[1, 0], [0, 1]]", description="Fallback matrix value")
    vector: str = Field(default="[1, 0, 0]", description="Fallback vector value")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        if self.mode == "vector":
            code = f'{var_name} = Matrix([[v] for v in {{param_vector}}]).scale({self.scale})'
        else:
            code = f'{var_name} = Matrix({{param_matrix}}).scale({self.scale})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_matrix": "Matrix",
            "param_vector": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"
