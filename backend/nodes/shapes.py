from pydantic import Field
from typing import Dict
from .base import NodeBase


class CircleNode(NodeBase):
    """Creates a circle shape"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    radius: str = Field(default="1.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Circle(radius={{param_radius}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_radius": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        return schema


class SquareNode(NodeBase):
    """Creates a square shape"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    side_length: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")
    label: str = Field(default="", description="Center label (MathTex)")
    edge_labels: str = Field(default="", description="Edge labels, comma-separated")
    label_font_size: str = Field(default="48.0")
    label_offset: str = Field(default="0.3", description="Edge label distance")
    write_label: bool = Field(default=False, description="Auto-add labels to scene")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Square(side_length={{param_side_length}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_side_length": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject", "side_1": "Mobject", "side_2": "Mobject", "side_3": "Mobject", "side_4": "Mobject", "edges": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class RectangleNode(NodeBase):
    """Creates a rectangle shape"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    width: str = Field(default="4.0")
    height: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")
    label: str = Field(default="", description="Center label (MathTex)")
    edge_labels: str = Field(default="", description="Edge labels, comma-separated")
    label_font_size: str = Field(default="48.0")
    label_offset: str = Field(default="0.3", description="Edge label distance")
    write_label: bool = Field(default=False, description="Auto-add labels to scene")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Rectangle(width={{param_width}}, height={{param_height}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        code += f'.move_to({{param_position}})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_width": "Number",
            "param_height": "Number",
            "param_position": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject", "side_1": "Mobject", "side_2": "Mobject", "side_3": "Mobject", "side_4": "Mobject", "edges": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class LineNode(NodeBase):
    """Creates a line between two points"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    start: str = Field(default="[-2, 0, 0]", description="Start point [x, y, z]")
    end: str = Field(default="[2, 0, 0]", description="End point [x, y, z]")
    color: str = Field(default="#FFFFFF")
    stroke_width: str = Field(default="4.0")
    label: str = Field(default="", description="Label text (MathTex, empty = no label)")
    label_font_size: str = Field(default="72.0")
    label_offset: str = Field(default="0.3", description="Label distance from line")
    write_label: bool = Field(default=False, description="Auto-add label to scene")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        parts = []
        line_code = f'{var_name} = Line(start={{param_start}}, end={{param_end}}, color={{param_color}}, stroke_width={self.stroke_width})'
        if self.z_index != "0":
            line_code += f'.set_z_index({self.z_index})'
        parts.append(line_code)
        # Set label direction (perpendicular normal)
        parts.append(f'_ld_{var_name} = {var_name}.get_unit_vector()')
        parts.append(f'{var_name}._label_direction = np.array([-_ld_{var_name}[1], _ld_{var_name}[0], 0])')
        # Shape alias for multi-output
        parts.append(f'{var_name}_shape = {var_name}')
        # Generate label
        if self.label:
            escaped = self.label.replace('"', '\\"')
            parts.append(f'{var_name}_label = MathTex(r"{escaped}", font_size={self.label_font_size}, color={{param_color}})')
            parts.append(f'{var_name}_label.move_to({var_name}.point_from_proportion(0.5) + {self.label_offset} * {var_name}._label_direction)')
        else:
            parts.append(f'{var_name}_label = Dot(ORIGIN).set_opacity(0)')
        return '\n        '.join(parts)

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_start": "Vec3",
            "param_end": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject", "label": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"


class TextNode(NodeBase):
    """Creates text object"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    text: str = Field(default="Hello")
    font_size: str = Field(default="72.0")
    color: str = Field(default="#FFFFFF")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        # Escape quotes in text
        escaped_text = self.text.replace('"', '\\"')
        code = f'{var_name} = Text("{escaped_text}", font_size={self.font_size}, color={{param_color}})'
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
        return {"text": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"


class ArrowNode(NodeBase):
    """Creates an arrow"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    start: str = Field(default="[-2, 0, 0]", description="Start point [x, y, z]")
    end: str = Field(default="[2, 0, 0]", description="End point [x, y, z]")
    color: str = Field(default="#FFFFFF")
    stroke_width: str = Field(default="4.0")
    buff: str = Field(default="0.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Arrow(start={{param_start}}, end={{param_end}}, color={{param_color}}, stroke_width={self.stroke_width}, buff={self.buff})'
        if self.z_index != "0":
            code += f'.set_z_index({self.z_index})'
        return code

    def get_inputs(self) -> Dict[str, str]:
        return {
            "param_start": "Vec3",
            "param_end": "Vec3",
            "param_color": "Color"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"arrow": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"


class TriangleNode(NodeBase):
    """Creates a regular triangle"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    side_length: str = Field(default="2.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")
    label: str = Field(default="", description="Center label (MathTex)")
    edge_labels: str = Field(default="", description="Edge labels, comma-separated (e.g. a,b,c)")
    label_font_size: str = Field(default="48.0")
    label_offset: str = Field(default="0.3", description="Edge label distance")
    write_label: bool = Field(default=False, description="Auto-add labels to scene")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Triangle(color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width}).scale({self.side_length})'
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
        return {"shape": "Mobject", "side_1": "Mobject", "side_2": "Mobject", "side_3": "Mobject", "edges": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class RegularPolygonNode(NodeBase):
    """Creates a regular polygon with n sides"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    n_sides: str = Field(default="6", description="Number of sides")
    radius: str = Field(default="1.0")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = RegularPolygon(n={self.n_sides}, radius={{param_radius}}, color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
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
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class RightTriangleNode(NodeBase):
    """Creates a right-angled triangle"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    base: str = Field(default="2.0", description="Base length (horizontal leg)")
    height: str = Field(default="1.5", description="Height (vertical leg)")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")
    label: str = Field(default="", description="Center label (MathTex)")
    edge_labels: str = Field(default="", description="Edge labels, comma-separated (e.g. a,b,c)")
    label_font_size: str = Field(default="48.0")
    label_offset: str = Field(default="0.3", description="Edge label distance")
    write_label: bool = Field(default=False, description="Auto-add labels to scene")

    def to_manim_code(self, var_name: str) -> str:
        code = f'{var_name} = Polygon([0, 0, 0], [{self.base}, 0, 0], [0, {self.height}, 0], color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
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
        return {"shape": "Mobject", "side_1": "Mobject", "side_2": "Mobject", "side_3": "Mobject", "edges": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class IsoscelesTriangleNode(NodeBase):
    """Creates an isosceles triangle (two equal sides)"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    base: str = Field(default="2.0", description="Base length")
    height: str = Field(default="1.5", description="Height from base to apex")
    color: str = Field(default="#FFFFFF")
    fill_opacity: str = Field(default="0.0")
    stroke_width: str = Field(default="4.0")
    z_index: str = Field(default="0", description="Draw order (higher = front)")
    position: str = Field(default="[0, 0, 0]", description="3D position [x, y, z]")
    label: str = Field(default="", description="Center label (MathTex)")
    edge_labels: str = Field(default="", description="Edge labels, comma-separated (e.g. a,b,c)")
    label_font_size: str = Field(default="48.0")
    label_offset: str = Field(default="0.3", description="Edge label distance")
    write_label: bool = Field(default=False, description="Auto-add labels to scene")

    def to_manim_code(self, var_name: str) -> str:
        # Expression: half_base calculated at render time via Python
        code = f'{var_name} = Polygon([-({self.base})/2, 0, 0], [({self.base})/2, 0, 0], [0, {self.height}, 0], color={{param_color}}, fill_opacity={self.fill_opacity}, stroke_width={self.stroke_width})'
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
        return {"shape": "Mobject", "side_1": "Mobject", "side_2": "Mobject", "side_3": "Mobject", "edges": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes 2D"

    @classmethod
    def get_schema(cls) -> Dict:
        return cls.model_json_schema()


class LineLabelNode(NodeBase):
    """Places a MathTex label along a Line at a configurable position with perpendicular offset"""
    order: int = Field(default=0, ge=-100, le=100, description="Creation order (lower = created first)")
    text: str = Field(default="a", description="Label content (rendered as MathTex)")
    font_size: str = Field(default="72.0")
    color: str = Field(default="#FFFFFF")
    position: str = Field(default="0.5", description="Proportion along line (0.0 = start, 1.0 = end)")
    offset: str = Field(default="0.3", description="Perpendicular distance from line")

    def to_manim_code(self, var_name: str) -> str:
        escaped_text = self.text.replace('"', '\\"')
        lines = []
        # Use _label_direction from line if set (outward for shape edges), else compute perpendicular
        lines.append(f'_ud_{var_name} = {{input_line}}.get_unit_vector()')
        lines.append(f'_dir_{var_name} = getattr({{input_line}}, "_label_direction", np.array([-_ud_{var_name}[1], _ud_{var_name}[0], 0]))')
        lines.append(f'{var_name} = MathTex(r"{escaped_text}", font_size={self.font_size}, color={{param_color}})')
        lines.append(f'{var_name}.move_to({{input_line}}.point_from_proportion({self.position}) + {self.offset} * _dir_{var_name})')
        return '\n        '.join(lines)

    def get_inputs(self) -> Dict[str, str]:
        return {
            "line": "Mobject",
            "param_color": "Color",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"label": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"
