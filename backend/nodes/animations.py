from pydantic import Field
from typing import Dict
from .base import NodeBase


class FadeInNode(NodeBase):
    """Fade in animation"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    run_time: str = Field(default="1.0")
    shift: str = Field(default="[0, 0, 0]", description="Shift direction [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        if self.shift != "[0, 0, 0]":
            return f'{var_name} = FadeIn({{input_mobject}}, shift={self.shift}, run_time={self.run_time})'
        return f'{var_name} = FadeIn({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class FadeOutNode(NodeBase):
    """Fade out animation"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    run_time: str = Field(default="1.0")
    shift: str = Field(default="[0, 0, 0]", description="Shift direction [x, y, z]")

    def to_manim_code(self, var_name: str) -> str:
        if self.shift != "[0, 0, 0]":
            return f'{var_name} = FadeOut({{input_mobject}}, shift={self.shift}, run_time={self.run_time})'
        return f'{var_name} = FadeOut({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class ShowNode(NodeBase):
    """Display a shape in the scene without animation"""

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = {{input_mobject}}'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class WriteNode(NodeBase):
    """Write animation (for text/shapes)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Write({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class CreateNode(NodeBase):
    """Create animation (draws the shape)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Create({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class MorphNode(NodeBase):
    """Morph one shape into another"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Transform({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class RotateNode(NodeBase):
    """Rotate animation in 3D (axis-angle rotation)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    angle: str = Field(default="90.0", description="Angle in degrees")
    run_time: str = Field(default="1.0")
    axis: str = Field(default="[0, 0, 1]", description="Rotation axis [x, y, z]")
    about_point: str = Field(default="center", description="Pivot point for rotation")

    def to_manim_code(self, var_name: str) -> str:
        if self.animate:
            return var_name + ' = Rotate({input_mobject}, angle={param_angle_rad}, axis={param_axis}, about_point={ABOUT_POINT}, run_time=' + str(self.run_time) + ')'
        else:
            return '{input_mobject}.rotate(angle={param_angle_rad}, axis={param_axis}, about_point={ABOUT_POINT}); ' + var_name + ' = None'

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "about_point" in schema["properties"]:
            schema["properties"]["about_point"]["enum"] = ["center", "min", "max", "origin"]
        return schema

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "param_angle_rad": "Number",
            "param_axis": "Vec3",
            "param_about_point": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class ScaleNode(NodeBase):
    """Scale animation"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    scale_factor: str = Field(default="2.0")
    run_time: str = Field(default="1.0")
    about_point: str = Field(default="center", description="Pivot point for scaling")

    def to_manim_code(self, var_name: str) -> str:
        if self.animate:
            return var_name + ' = {input_mobject}.animate(run_time=' + str(self.run_time) + ').scale({param_scale_factor})'
        else:
            point_map = {
                "center": "{input_mobject}.get_center()",
                "min": "{input_mobject}.get_corner(DL)",
                "max": "{input_mobject}.get_corner(UR)",
                "origin": "ORIGIN"
            }
            about = point_map.get(self.about_point, "{input_mobject}.get_center()")
            return '{input_mobject}.scale({param_scale_factor}, about_point=' + about + '); ' + var_name + ' = None'

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "about_point" in schema["properties"]:
            schema["properties"]["about_point"]["enum"] = ["center", "min", "max", "origin"]
        return schema

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "param_scale_factor": "Number",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class MoveToNode(NodeBase):
    """Move to position animation (3D)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    target: str = Field(default="[0, 0, 0]", description="Target position [x, y, z]")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        if self.animate:
            return f'{var_name} = ApplyMethod({{input_mobject}}.move_to, {{param_target}}, run_time={self.run_time})'
        else:
            return f'{{input_mobject}}.move_to({{param_target}}); {var_name} = None'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "param_target": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "shape_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class SequenceNode(NodeBase):
    """Play animations in sequence"""
    wait_time: str = Field(default="0.5", description="Pause between animations (seconds)")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = "SEQUENCE"'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "anim1": "Animation",
            "anim2": "Animation",
            "anim3": "Animation",
            "anim4": "Animation",
            "anim5": "Animation",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class AnimationGroupNode(NodeBase):
    """Play multiple animations together (parallel)"""
    run_time: str = Field(default="1.0", description="Duration for all animations")
    lag_ratio: str = Field(default="0.0", description="Stagger animations (0=together, 1=sequential)")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = "ANIMATION_GROUP"'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "anim1": "Animation",
            "anim2": "Animation",
            "anim3": "Animation",
            "anim4": "Animation",
            "anim5": "Animation",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"

    @classmethod
    def get_display_name(cls) -> str:
        return "AnimationGroup"


# ── Creation animations ──────────────────────────────────────────────


class UncreateNode(NodeBase):
    """Reverse of Create - removes shape by untracing"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Uncreate({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class UnwriteNode(NodeBase):
    """Reverse of Write - removes text/shape by unwriting"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Unwrite({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class DrawBorderThenFillNode(NodeBase):
    """Draw the border of a shape, then fill it in"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = DrawBorderThenFill({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class SpiralInNode(NodeBase):
    """Spiral a shape into the scene"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = SpiralIn({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


# ── Growing animations ───────────────────────────────────────────────


class GrowFromCenterNode(NodeBase):
    """Grow a shape from its center"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = GrowFromCenter({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class GrowFromPointNode(NodeBase):
    """Grow a shape from a specific point"""
    run_time: str = Field(default="1.0")
    point: str = Field(default="[0,0,0]", description="Point to grow from [x,y,z]")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = GrowFromPoint({{input_mobject}}, point={{param_point}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject", "param_point": "Vec3"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class GrowFromEdgeNode(NodeBase):
    """Grow a shape from a specific edge"""
    run_time: str = Field(default="1.0")
    edge: str = Field(default="DOWN", description="Edge to grow from")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = GrowFromEdge({{input_mobject}}, edge={self.edge}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "edge" in schema["properties"]:
            schema["properties"]["edge"]["enum"] = ["UP", "DOWN", "LEFT", "RIGHT", "UL", "UR", "DL", "DR"]
        return schema

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class GrowArrowNode(NodeBase):
    """Grow an arrow into the scene"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = GrowArrow({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class SpinInFromNothingNode(NodeBase):
    """Spin a shape in from nothing (rotate + scale up)"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = SpinInFromNothing({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


# ── Indication animations ────────────────────────────────────────────


class IndicateNode(NodeBase):
    """Briefly highlight a shape with color and scale"""
    scale_factor: str = Field(default="1.2", description="Scale factor during indication")
    color: str = Field(default="#FFFF00", description="Highlight color")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Indicate({{input_mobject}}, scale_factor={self.scale_factor}, color={self._quote_color()}, run_time={self.run_time})'

    def _quote_color(self) -> str:
        if self.color.startswith('#'):
            return f'"{self.color}"'
        return self.color

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class FlashNode(NodeBase):
    """Flash lines radiating from a shape"""
    line_length: str = Field(default="0.2", description="Length of flash lines")
    num_lines: str = Field(default="12", description="Number of flash lines")
    color: str = Field(default="#FFFF00", description="Flash color")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        color = f'"{self.color}"' if self.color.startswith('#') else self.color
        return f'{var_name} = Flash({{input_mobject}}, line_length={self.line_length}, num_lines={self.num_lines}, color={color}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class CircumscribeNode(NodeBase):
    """Draw a temporary shape around a mobject to highlight it"""
    color: str = Field(default="#FFFF00", description="Circumscribe color")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        color = f'"{self.color}"' if self.color.startswith('#') else self.color
        return f'{var_name} = Circumscribe({{input_mobject}}, color={color}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class WiggleNode(NodeBase):
    """Wiggle a shape back and forth"""
    scale_value: str = Field(default="1.1", description="Scale during wiggle")
    rotation_angle: str = Field(default="0.02", description="Rotation angle (fraction of TAU)")
    n_wiggles: str = Field(default="6", description="Number of wiggles")
    run_time: str = Field(default="2.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Wiggle({{input_mobject}}, scale_value={self.scale_value}, rotation_angle={self.rotation_angle}*TAU, n_wiggles={self.n_wiggles}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class ApplyWaveNode(NodeBase):
    """Apply a wave effect to a shape"""
    amplitude: str = Field(default="0.2", description="Wave amplitude")
    direction: str = Field(default="UP", description="Wave direction")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = ApplyWave({{input_mobject}}, amplitude={self.amplitude}, direction={self.direction}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "direction" in schema["properties"]:
            schema["properties"]["direction"]["enum"] = ["UP", "DOWN", "LEFT", "RIGHT"]
        return schema

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class FocusOnNode(NodeBase):
    """Focus on a shape with a shrinking circle highlight"""
    opacity: str = Field(default="0.2", description="Background opacity")
    color: str = Field(default="#888888", description="Focus color")
    run_time: str = Field(default="2.0")

    def to_manim_code(self, var_name: str) -> str:
        color = f'"{self.color}"' if self.color.startswith('#') else self.color
        return f'{var_name} = FocusOn({{input_mobject}}, opacity={self.opacity}, color={color}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


# ── Movement animations ──────────────────────────────────────────────


class MoveAlongPathNode(NodeBase):
    """Move a shape along another path mobject"""
    run_time: str = Field(default="2.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = MoveAlongPath({{input_mobject}}, {{input_path}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject", "path": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


# ── Transform animations ─────────────────────────────────────────────


class ReplacementTransformNode(NodeBase):
    """Transform source into target, replacing source in the scene"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = ReplacementTransform({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class TransformFromCopyNode(NodeBase):
    """Transform a copy of the source into the target"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = TransformFromCopy({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class FadeTransformNode(NodeBase):
    """Transform by fading source out and target in"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = FadeTransform({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class TransformMatchingShapesNode(NodeBase):
    """Transform matching sub-shapes between source and target"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = TransformMatchingShapes({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class TransformMatchingTexNode(NodeBase):
    """Transform matching TeX elements between source and target"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = TransformMatchingTex({{input_source}}, {{input_target}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"source": "Mobject", "target": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class FadeToColorNode(NodeBase):
    """Animate changing a shape's color"""
    color: str = Field(default="#FFFF00", description="Target color")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        color = f'"{self.color}"' if self.color.startswith('#') else self.color
        return f'{var_name} = {{input_mobject}}.animate(run_time={self.run_time}).set_color({color})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class ShrinkToCenterNode(NodeBase):
    """Shrink a shape to its center (reverse of GrowFromCenter)"""
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = ShrinkToCenter({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


# ── Other animations ─────────────────────────────────────────────────


class BroadcastNode(NodeBase):
    """Broadcast expanding rings from a shape"""
    run_time: str = Field(default="2.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Broadcast({{input_mobject}}, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"animation": "Animation", "shape_out": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Animations"
