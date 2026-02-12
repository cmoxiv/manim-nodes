from pydantic import Field
from typing import Dict, List
from .base import NodeBase


class JunctionNode(NodeBase):
    """Pass-through reroute point. Visually a small dot to tidy up wires."""

    def to_manim_code(self, var_name: str) -> str:
        return ""  # Transparent — code generator maps output to input directly

    def get_inputs(self) -> Dict[str, str]:
        return {"in": "Any"}

    def get_outputs(self) -> Dict[str, str]:
        return {"out": "Any"}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"


class DebugPrintNode(NodeBase):
    """Print the value of an input during rendering"""
    label: str = Field(default="", description="Label prefix for the output")

    def to_manim_code(self, var_name: str) -> str:
        escaped = self.label.replace('"', '\\"')
        prefix = f'{escaped}: ' if escaped else ''
        return f'print("[DEBUG:{{node_id}}] {prefix}" + str({{input_value}}))'

    def get_inputs(self) -> Dict[str, str]:
        return {"value": "Any"}

    def get_outputs(self) -> Dict[str, str]:
        return {}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"


class GroupNode(NodeBase):
    """Group multiple shapes together"""
    pivot: str = Field(
        default="center",
        description="Pivot point for the group"
    )

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = VGroup()'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "obj1": "Mobject",
            "obj2": "Mobject",
            "obj3": "Mobject",
            "obj4": "Mobject",
            "obj5": "Mobject",
            "obj6": "Mobject",
            "obj7": "Mobject",
            "obj8": "Mobject",
            "obj9": "Mobject",
            "obj10": "Mobject",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "2D"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "pivot" in schema["properties"]:
            schema["properties"]["pivot"]["enum"] = [
                "center", "first", "last", "mean", "min", "max"
            ]
        return schema


class TextCharacterNode(NodeBase):
    """Select specific character(s) from a Text/MathTex object by index or letter"""
    mode: str = Field(default="index", description="Selection mode: index or letter")
    index: str = Field(default="0", description="Character index (used in index mode)")
    letter: str = Field(default="", description="Letter to match (used in letter mode)")

    def to_manim_code(self, var_name: str) -> str:
        if self.mode == "letter":
            return f'{var_name} = VGroup(*[{{input_mobject}}[i] for i, c in enumerate({{input_mobject}}.text) if c == "{self.letter}"])'
        return f'{var_name} = {{input_mobject}}[{self.index}]'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"character": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Text & Math"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "mode" in schema["properties"]:
            schema["properties"]["mode"]["enum"] = ["index", "letter"]
        return schema


class PythonCodeNode(NodeBase):
    """Inject custom Python code into the generated scene"""
    code: str = Field(
        default="def my_func(x):\n    return x ** 2",
        description="Python code to inject"
    )

    def to_manim_code(self, var_name: str) -> str:
        return self.code

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "code" in schema["properties"]:
            schema["properties"]["code"]["format"] = "code"
        return schema


class ExtractEdgesNode(NodeBase):
    """Extract edges from a polygon as individual Line objects"""

    def to_manim_code(self, var_name: str) -> str:
        lines = []
        lines.append(f'_verts_{var_name} = {{input_mobject}}.get_vertices()')
        lines.append(f'_n_{var_name} = len(_verts_{var_name})')
        for i in range(6):
            lines.append(
                f'{var_name}_side_{i+1} = Line(_verts_{var_name}[{i}], _verts_{var_name}[{i+1} % _n_{var_name}], '
                f'color={{input_mobject}}.get_color(), stroke_width={{input_mobject}}.get_stroke_width()) '
                f'if _n_{var_name} >= {i+2} else Dot(ORIGIN).set_opacity(0)'
            )
        lines.append(
            f'{var_name}_edges = VGroup(*[Line(_verts_{var_name}[i], _verts_{var_name}[(i+1) % _n_{var_name}], '
            f'color={{input_mobject}}.get_color(), stroke_width={{input_mobject}}.get_stroke_width()) '
            f'for i in range(_n_{var_name})])'
        )
        # Set outward-facing label directions (perpendicular to each edge, oriented outward)
        lines.append(f'_centroid_{var_name} = np.mean(_verts_{var_name}, axis=0)')
        for i in range(6):
            lines.append(
                f'if isinstance({var_name}_side_{i+1}, Line): '
                f'_ed = _verts_{var_name}[{i+1} % _n_{var_name}] - _verts_{var_name}[{i}]; '
                f'_perp = np.array([-_ed[1], _ed[0], 0]); '
                f'_perp = _perp / (np.linalg.norm(_perp) + 1e-10); '
                f'_mid = (_verts_{var_name}[{i}] + _verts_{var_name}[{i+1} % _n_{var_name}]) / 2; '
                f'{var_name}_side_{i+1}._label_direction = -_perp if np.dot(_perp, _centroid_{var_name} - _mid) > 0 else _perp'
            )
        return '\n        '.join(lines)

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "side_1": "Mobject",
            "side_2": "Mobject",
            "side_3": "Mobject",
            "side_4": "Mobject",
            "side_5": "Mobject",
            "side_6": "Mobject",
            "edges": "Mobject",
        }

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"


class ExposeParametersNode(NodeBase):
    """Expose any shape's construction and runtime parameters as typed outputs"""
    param_1: str = Field(default="none", description="Parameter 1")
    param_2: str = Field(default="none", description="Parameter 2")
    param_3: str = Field(default="none", description="Parameter 3")

    def to_manim_code(self, var_name: str) -> str:
        m = '{input_mobject}'
        parts = [f'{var_name}_shape = {m}']
        selected = {self.param_1, self.param_2, self.param_3} - {"none"}
        CODE_MAP = {
            "position": f'{var_name}_position = list({m}.get_center())',
            "color": f'{var_name}_color = {m}.get_color()',
            "width": f'{var_name}_width = {m}.width',
            "height": f'{var_name}_height = {m}.height',
            "radius": f'{var_name}_radius = getattr({m}, "radius", {m}.width / 2)',
            "side_length": f'{var_name}_side_length = getattr({m}, "side_length", {m}.width)',
            "stroke_width": f'{var_name}_stroke_width = {m}.get_stroke_width()',
            "fill_opacity": f'{var_name}_fill_opacity = {m}.get_fill_opacity()',
            "start": f'{var_name}_start = list({m}.get_start())',
            "end": f'{var_name}_end = list({m}.get_end())',
            "length": f'{var_name}_length = float(np.linalg.norm(np.array({m}.get_end()) - np.array({m}.get_start())))',
            "direction": f'{var_name}_direction = list({m}.get_unit_vector()) if hasattr({m}, "get_unit_vector") else [1, 0, 0]',
        }
        for param in selected:
            if param in CODE_MAP:
                parts.append(CODE_MAP[param])
        return '\n        '.join(parts)

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {
            "shape": "Mobject",
            "position": "Vec3",
            "color": "Color",
            "width": "Number",
            "height": "Number",
            "radius": "Number",
            "side_length": "Number",
            "stroke_width": "Number",
            "fill_opacity": "Number",
            "start": "Vec3",
            "end": "Vec3",
            "length": "Number",
            "direction": "Vec3",
        }

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        PARAM_OPTIONS = [
            "none", "position", "color", "width", "height", "radius",
            "side_length", "stroke_width", "fill_opacity", "start", "end",
            "length", "direction"
        ]
        for p in ["param_1", "param_2", "param_3"]:
            if "properties" in schema and p in schema["properties"]:
                schema["properties"][p]["enum"] = PARAM_OPTIONS
        return schema


class TransformInPlaceNode(NodeBase):
    """Apply Scale, Rotation, and Translation relative to the mobject's current center"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    copy: bool = Field(default=False, description="Animate a copy (preserves original)")
    translation: str = Field(default="[0, 0, 0]", description="Translation [x, y, z]")
    angle: str = Field(default="0", description="Rotation angle in degrees")
    axis: str = Field(default="[0, 0, 1]", description="Rotation axis [x, y, z]")
    scale: str = Field(default="[1, 1, 1]", description="Scale [x, y, z]")
    target: str = Field(default="[0, 0, 0]", description="Final target position [x, y, z]")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        lines = [
            f'_{var_name}_orig = {{input_mobject}}.copy()',
            f'_{var_name}_ctr = {{input_mobject}}.get_center()',
            f'_{var_name}_s = np.array({{param_scale}}, dtype=float)',
            f'_{var_name}_a = np.radians({{param_angle}})',
            f'_{var_name}_ax = np.array({{param_axis}}, dtype=float)',
            f'_{var_name}_tr = np.array({{param_translation}}, dtype=float)',
            f'def _{var_name}_upd(m, alpha):',
            f'    m.become(_{var_name}_orig.copy())',
            f'    _cs = np.ones(3) + alpha * (_{var_name}_s - np.ones(3))',
            f'    m.apply_matrix(np.diag(_cs), about_point=_{var_name}_ctr)',
            f'    m.rotate(alpha * _{var_name}_a, axis=_{var_name}_ax, about_point=_{var_name}_ctr)',
            f'    m.shift(alpha * _{var_name}_tr)',
            f'    {{MOVE_TO}}',
            f'{var_name} = UpdateFromAlphaFunc({{input_mobject}}, _{var_name}_upd, run_time={self.run_time})',
        ]
        return '\n        '.join(lines)

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "param_translation": "Vec3",
            "param_angle": "Number",
            "param_axis": "Vec3",
            "param_scale": "Vec3",
            "param_target": "Vec3",
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "mobject_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"


class TransformNode(NodeBase):
    """Apply a 2D transformation matrix (augmented 3x3 homogeneous coordinates)"""
    animate: bool = Field(default=True, description="Animate (True) or apply instantly (False)")
    m11: str = Field(default="1", description="Scale/rotate X (a)")
    m12: str = Field(default="0", description="Skew X (b)")
    m13: str = Field(default="0", description="Translate X (tx)")
    m21: str = Field(default="0", description="Skew Y (c)")
    m22: str = Field(default="1", description="Scale/rotate Y (d)")
    m23: str = Field(default="0", description="Translate Y (ty)")
    run_time: str = Field(default="1.0")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name}_target = {{input_mobject}}.copy(); {var_name}_target.apply_matrix({{MATRIX_2X2}}); {var_name}_target.shift({{TRANSLATION}}); {var_name} = Transform({{input_mobject}}, {var_name}_target, run_time={self.run_time})'

    def get_inputs(self) -> Dict[str, str]:
        return {
            "mobject": "Mobject",
            "matrix": "Matrix"
        }

    def get_outputs(self) -> Dict[str, str]:
        return {
            "animation": "Animation",
            "mobject_out": "Mobject"
        }

    @classmethod
    def get_category(cls) -> str:
        return "Animations"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        schema["matrixGrid"] = {
            "rows": 2,
            "cols": 3,
            "fields": ["m11", "m12", "m13", "m21", "m22", "m23"],
            "note": "Bottom row [0, 0, 1] is fixed for 2D transforms"
        }
        return schema


class ImportGraphNode(NodeBase):
    """Import objects from another graph file"""
    graph_file: str = Field(default="", description="Path to graph JSON file")
    expose_1: str = Field(default="none", description="Object name to expose as output 1")
    expose_2: str = Field(default="none", description="Object name to expose as output 2")
    expose_3: str = Field(default="none", description="Object name to expose as output 3")

    def to_manim_code(self, var_name: str) -> str:
        # Code generation for ImportGraph is handled specially in the code generator
        # This placeholder generates a comment
        return f'# ImportGraph: {self.graph_file}'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        for i, expose in enumerate([self.expose_1, self.expose_2, self.expose_3], 1):
            if expose and expose != "none":
                outputs[f"obj_{i}"] = "Mobject"
        return outputs

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        # expose fields will be populated dynamically by the frontend
        # based on the selected graph file's named objects
        return schema


class FunctionDefNode(NodeBase):
    """Define a reusable Python function"""
    func_name: str = Field(default="my_func", description="Function name")
    code: str = Field(
        default="def my_func(x):\n    return {'result': x ** 2}",
        description="Function code (must return a dict of outputs)"
    )

    def to_manim_code(self, var_name: str) -> str:
        return self.code

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"

    @classmethod
    def get_schema(cls) -> Dict:
        schema = cls.model_json_schema()
        if "properties" in schema and "code" in schema["properties"]:
            schema["properties"]["code"]["format"] = "code"
        return schema


def parse_function_code(code: str):
    """Parse a function definition to extract parameter names and return dict keys."""
    import re
    params: List[str] = []
    outputs: List[str] = []

    def_match = re.search(r'def\s+\w+\(([^)]*)\)', code)
    if def_match:
        params = [p.strip().split('=')[0].strip() for p in def_match.group(1).split(',')]
        params = [p for p in params if p and p != 'self']

    return_match = re.search(r'return\s*\{(.+?)\}', code, re.DOTALL)
    if return_match:
        outputs = re.findall(r"['\"](\w+)['\"]", return_match.group(1))

    return params, outputs


class FunctionCallNode(NodeBase):
    """Call a defined function"""
    func_name: str = Field(default="my_func", description="Function to call")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name}_result = {self.func_name}({{FUNC_ARGS}})'

    def get_inputs(self) -> Dict[str, str]:
        return {f"arg_{i}": "Any" for i in range(1, 9)}

    def get_outputs(self) -> Dict[str, str]:
        return {f"out_{i}": "Any" for i in range(1, 9)}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"


class GetVertexNode(NodeBase):
    """Get a vertex position from a polygon"""
    index: str = Field(default="0", description="Vertex index (0-based)")

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = list({{input_mobject}}.get_vertices()[{self.index}])'

    def get_inputs(self) -> Dict[str, str]:
        return {"mobject": "Mobject"}

    def get_outputs(self) -> Dict[str, str]:
        return {"position": "Vec3"}

    @classmethod
    def get_category(cls) -> str:
        return "Utilities"
