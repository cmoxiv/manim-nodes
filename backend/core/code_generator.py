from typing import Dict, List
import logging
from ..models.graph import Graph
from ..nodes import NODE_REGISTRY
from ..nodes.utilities import parse_function_code
from .graph_validator import GraphValidator, ValidationError

logger = logging.getLogger("manim_nodes")


class CodeGenerator:
    """Generates MANIM Python code from node graphs"""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.validator = GraphValidator(graph)
        self._type_counters: Dict[str, int] = {}
        self.var_to_node_id: Dict[str, str] = {}  # var_name -> node_id reverse mapping

        # Build dynamic set of animation type names from NODE_REGISTRY
        # Animation nodes CONSUME a mobject input; shape nodes CREATE mobjects
        self._animation_types: set = set()
        for reg_name, reg_cls in NODE_REGISTRY.items():
            try:
                instance = reg_cls()
                outputs = instance.get_outputs()
                inputs = instance.get_inputs()
                has_animation_output = "Animation" in outputs.values()
                has_mobject_input = "mobject" in inputs or "source" in inputs
                # Animation nodes have Animation output AND take a mobject/source input
                if has_animation_output and has_mobject_input:
                    self._animation_types.add(reg_name)
            except Exception:
                pass

    def generate(self) -> str:
        """
        Generate complete MANIM Python code.

        Returns:
            Python code as a string

        Raises:
            ValidationError if graph is invalid
        """
        # Validate graph first
        is_valid, errors = self.validator.validate()
        if not is_valid:
            error_messages = "\n".join([f"  - {node_id or 'Graph'}: {msg}" for node_id, msg in errors])
            # Attach the first offending node_id for highlighting
            first_node_id = next((nid for nid, _ in errors if nid), None)
            raise ValidationError(f"Graph validation failed:\n{error_messages}", node_id=first_node_id)

        # Get execution order
        execution_order = self.validator.get_execution_order()

        # Generate code
        code_parts = []

        # Imports
        code_parts.append(self._generate_imports())
        code_parts.append("")

        # Module-level function definitions (FunctionDef nodes)
        node_map = {node.id: node for node in self.graph.nodes}
        for node_id in execution_order:
            node = node_map.get(node_id)
            if node and node.type == "FunctionDef":
                node_data = node.data if isinstance(node.data, dict) else {}
                code = node_data.get("code", "")
                if code.strip():
                    code_parts.append(code)
                    code_parts.append("")

        # Scene class
        code_parts.append(self._generate_scene_class(execution_order))

        generated_code = "\n".join(code_parts)

        # Debug: Save generated code for inspection
        from pathlib import Path
        debug_file = Path.home() / "manim-nodes" / "temp" / "last_generated.py"
        debug_file.parent.mkdir(parents=True, exist_ok=True)
        debug_file.write_text(generated_code)

        return generated_code

    def _generate_imports(self) -> str:
        """Generate import statements"""
        return """from manim import *
import math
import numpy as np"""

    def _generate_scene_class(self, execution_order: List[str]) -> str:
        """Generate the Scene class with construct method"""
        animation_types = self._animation_types

        # Build node lookup map for O(1) access
        node_map = {node.id: node for node in self.graph.nodes}

        # Always use ThreeDScene (3D-first architecture)
        # 2D shapes work fine in 3D space with z=0
        scene_class = "ThreeDScene"
        lines = [f"class GeneratedScene({scene_class}):"]
        lines.append("    def construct(self):")

        # Build edge mapping (target_node_id, target_handle) -> (source_node_id, source_handle)
        input_map: Dict[tuple, tuple] = {}
        for edge in self.graph.edges:
            key = (edge.target, edge.targetHandle or "default")
            input_map[key] = (edge.source, edge.sourceHandle or "default")

        # Build node ID to variable name mapping
        node_vars = {}
        used_names = set()
        for node in self.graph.nodes:
            node_data = node.data if isinstance(node.data, dict) else {}
            base_name = self._safe_var_name(node.id, node.type, node_data)

            # Constant vectors are singletons — all instances share the same name
            if node.type not in self.CONST_VEC_TYPES and node.type not in self.CONST_VEC_ALIASES:
                # Deduplicate: if name already used, append incrementing suffix
                if base_name in used_names:
                    suffix = 2
                    while f"{base_name}_{suffix}" in used_names:
                        suffix += 1
                    base_name = f"{base_name}_{suffix}"
            used_names.add(base_name)

            node_vars[node.id] = base_name
            self.var_to_node_id[base_name] = node.id

        # Resolve junctions: map each junction's variable to its input source
        # Iterates until stable to handle chained junctions
        changed = True
        while changed:
            changed = False
            for node in self.graph.nodes:
                if node.type == "Junction":
                    source_info = input_map.get((node.id, "in"))
                    if source_info:
                        source_node_id, source_handle = source_info
                        source_var = node_vars.get(source_node_id)
                        if source_var:
                            # For multi-output source nodes, append handle name
                            source_node = node_map.get(source_node_id)
                            if source_node and source_node.type != "Junction":
                                source_class = NODE_REGISTRY.get(source_node.type)
                                if source_class:
                                    try:
                                        source_instance = source_class(**source_node.data)
                                        source_outputs = source_instance.get_outputs()
                                        if len(source_outputs) > 1 and source_handle != "default":
                                            source_var = f"{source_var}_{source_handle}"
                                    except Exception:
                                        pass
                            if node_vars[node.id] != source_var:
                                node_vars[node.id] = source_var
                                changed = True

        # Build sets of animation nodes in Sequence and AnimationGroup
        animations_in_sequence = set()
        animations_in_group = set()
        for node in self.graph.nodes:
            if node.type == "Sequence":
                # Animations in Sequence are generated inline
                for i in range(1, 11):
                    input_name = f"anim{i}"
                    source_info = input_map.get((node.id, input_name))
                    source_node_id = source_info[0] if source_info else None

                    if source_node_id:
                        animations_in_sequence.add(source_node_id)
            elif node.type == "AnimationGroup":
                # Animations in AnimationGroup need objects created but not played
                for i in range(1, 11):
                    input_name = f"anim{i}"
                    source_info = input_map.get((node.id, input_name))
                    source_node_id = source_info[0] if source_info else None

                    if source_node_id:
                        animations_in_group.add(source_node_id)

        # Build mapping of node_id -> mobject_variable for animation chains
        node_mobjects: Dict[str, str] = {}

        # Deferred labels: shape_var -> [label_var_names] (added after animation plays)
        pending_shape_labels: Dict[str, list] = {}

        # Track if any animations were played
        has_animations = False

        # Generate code for each node in execution order
        for exec_index, node_id in enumerate(execution_order, start=1):
            node = node_map.get(node_id)
            if not node:
                continue

            # FunctionDef nodes are emitted at module level, skip here
            if node.type == "FunctionDef":
                continue

            # Skip frame nodes — visual-only (frontend grouping)
            if node.type == "__groupFrame":
                continue

            try:
                node_class = NODE_REGISTRY[node.type]
                node_instance = node_class(**node.data)

                # Get the node's order field if it has one
                node_order = node.data.get('order', 'N/A') if isinstance(node.data, dict) else 'N/A'

                # Special handling for Sequence node
                if node.type == "Sequence":
                    # Skip inner Sequences — they are expanded by their parent
                    if node_id in animations_in_sequence:
                        continue

                    lines.append(f"        # Sequence: play animations in order")
                    self._emit_sequence_animations(node_id, input_map, node_map, node_vars,
                                                   node_mobjects, lines, pending_shape_labels,
                                                   animations_in_sequence, animations_in_group)

                    has_animations = True
                    continue  # Skip normal processing for Sequence

                # Special handling for AnimationGroup node
                if node.type == "AnimationGroup":
                    var_name = node_vars[node_id]
                    CAMERA_TYPES = {"SetCameraOrientation", "MoveCamera", "ZoomCamera"}
                    # Collect connected animations, separating camera nodes
                    connected_anims = []
                    camera_node_ids = []
                    for i in range(1, 11):
                        anim_name = f"anim{i}"
                        source_info = input_map.get((node_id, anim_name))

                        source_node_id = source_info[0] if source_info else None

                        if source_node_id:
                            source_node_obj = node_map.get(source_node_id)
                            if source_node_obj and source_node_obj.type in CAMERA_TYPES:
                                camera_node_ids.append(source_node_id)
                            else:
                                source_var = node_vars[source_node_id]
                                connected_anims.append(source_var)

                    if connected_anims or camera_node_ids:
                        # Add comment showing execution order
                        lines.append(f"        # Execution: {exec_index}, Order: {node_order}, Type: {node.type}, ID: {node.id}")

                        # Play upstream chain animations before the group
                        for j in range(1, 11):
                            src = input_map.get((node_id, f"anim{j}"))
                            if not src:
                                continue
                            anim_node_id = src[0]
                            chain = self._collect_chain_animations(anim_node_id, input_map, node_map,
                                                                   animations_in_sequence, animations_in_group)
                            for chain_id in chain:
                                self._play_with_labels(chain_id, node_vars[chain_id], node_mobjects,
                                                       pending_shape_labels, lines)

                        # Emit camera commands before the group (not AnimationGroup-compatible)
                        for cam_id in camera_node_ids:
                            cam_node = node_map[cam_id]
                            self._emit_camera_command(cam_node, lines)

                        # Build AnimationGroup from non-camera animations
                        if connected_anims:
                            anims_str = ", ".join(connected_anims)
                            lag = node_instance.lag_ratio
                            has_lag = lag != "0" and lag != "0.0"
                            if node_id in animations_in_sequence:
                                if has_lag:
                                    lines.append(f"        {var_name} = AnimationGroup({anims_str}, lag_ratio={lag}, run_time={node_instance.run_time})")
                                else:
                                    lines.append(f"        {var_name} = AnimationGroup({anims_str}, run_time={node_instance.run_time})")
                            else:
                                if has_lag:
                                    lines.append(f"        self.play({anims_str}, lag_ratio={lag}, run_time={node_instance.run_time})")
                                else:
                                    lines.append(f"        self.play({anims_str}, run_time={node_instance.run_time})")
                                has_animations = True

                                # Emit deferred labels for shapes animated in this group
                                for j in range(1, 11):
                                    src = input_map.get((node_id, f"anim{j}"))
                                    if not src:
                                        continue
                                    anim_node_id = src[0]
                                    mob_var = node_mobjects.get(anim_node_id)
                                    lbl_key = (mob_var[:-6] if mob_var and mob_var.endswith('_shape') else mob_var) if mob_var else None
                                    if lbl_key and lbl_key in pending_shape_labels:
                                        for lbl_var in pending_shape_labels.pop(lbl_key):
                                            lines.append(f"        self.add({lbl_var})")

                    continue  # Skip normal processing for AnimationGroup

                # Special handling for Group node
                if node.type == "Group":
                    var_name = node_vars[node_id]
                    # Collect connected objects
                    connected_objs = []
                    for i in range(1, 11):
                        obj_name = f"obj{i}"
                        source_info = input_map.get((node_id, obj_name))

                        source_node_id = source_info[0] if source_info else None

                        if source_node_id:
                            source_node = node_map.get(source_node_id)
                            # If source is an animation node, use its mobject variable
                            if source_node and source_node.type in animation_types:
                                # Get the mobject variable from the mapping
                                source_var = node_mobjects.get(source_node_id)
                                if not source_var:
                                    # Fallback to naming convention
                                    source_var = f"{node_vars[source_node_id]}_mobject"
                            else:
                                # Regular shape/mobject node
                                source_var = node_vars[source_node_id]
                            connected_objs.append(source_var)

                    if connected_objs:
                        # Create VGroup
                        objs_str = ", ".join(connected_objs)
                        lines.append(f"        {var_name} = VGroup({objs_str})")

                        # Set pivot point based on pivot parameter
                        pivot = node_instance.pivot
                        if pivot == "first":
                            lines.append(f"        {var_name}.move_to({connected_objs[0]}.get_center())")
                        elif pivot == "last":
                            lines.append(f"        {var_name}.move_to({connected_objs[-1]}.get_center())")
                        elif pivot == "mean":
                            lines.append(f"        {var_name}.move_to({var_name}.get_center())")
                        elif pivot == "min":
                            lines.append(f"        {var_name}.move_to({var_name}.get_corner(DL))")
                        elif pivot == "max":
                            lines.append(f"        {var_name}.move_to({var_name}.get_corner(UR))")
                        # center is the default, no need to adjust

                    continue  # Skip normal processing for Group

                # Special handling for Create node with Group input
                if node.type == "Create":
                    # Check if input is a Group
                    mobject_info = input_map.get((node_id, "mobject"))

                    mobject_source_id = mobject_info[0] if mobject_info else None

                    if mobject_source_id:
                        source_node = node_map.get(mobject_source_id)
                        if source_node and source_node.type == "Group":
                            var_name = node_vars[node_id]
                            source_var = node_vars[mobject_source_id]
                            create_copy_flag = getattr(node_instance, 'copy', False)

                            lines.append(f"        # Create each object in group")
                            if create_copy_flag:
                                copy_src = f"{var_name}_src"
                                lines.append(f"        {copy_src} = {source_var}.copy()")
                                target_var = copy_src
                            else:
                                target_var = source_var
                            # Store as animation variable — only plays via Sequence/AnimationGroup
                            lines.append(f"        {var_name} = AnimationGroup(*[Create(obj, run_time={node_instance.run_time}) for obj in {target_var}])")

                            # Store the mobject for chaining
                            node_mobjects[node_id] = target_var

                            continue  # Skip normal processing for Create with Group

                # Skip camera nodes in Sequence/AnimationGroup - handled inline
                if node.type in ["SetCameraOrientation", "MoveCamera", "ZoomCamera"] and (node_id in animations_in_sequence or node_id in animations_in_group):
                    continue

                # Skip animation nodes in Sequence - they'll be generated inline
                # (AnimationGroup needs its variable created here since it collects refs)
                # Don't skip shape nodes with presentation - they need shape code generated here
                if node_id in animations_in_sequence and node.type not in ("AnimationGroup", "Sequence"):
                    if self._is_shape_with_presentation(node):
                        pass  # Shape code still needed; presentation handled inline in Sequence
                    else:
                        # Pre-populate node_mobjects so downstream nodes (e.g. GetVertex)
                        # can reference the mobject this animation operates on
                        self._pre_populate_node_mobjects(
                            node_id, node_instance, input_map, node_map,
                            node_vars, node_mobjects
                        )
                        continue

                var_name = node_vars[node_id]

                # Constant vector nodes and junctions — no code needed
                if node.type in self.CONST_VEC_TYPES or node.type in self.CONST_VEC_ALIASES or node.type == "Junction":
                    continue

                code = node_instance.to_manim_code(var_name)

                # Replace input placeholders with actual variable names
                inputs = node_instance.get_inputs()
                mobject_var = None  # Track the mobject variable for this animation
                copy_flag = getattr(node_instance, 'copy', False)
                copy_var_name = f"{var_name}_src" if copy_flag else None
                copy_prepend = None

                for input_name in inputs:
                    placeholder = f"{{input_{input_name}}}"
                    source_info = input_map.get((node_id, input_name))
                    if source_info:
                        source_node_id, source_handle = source_info
                        source_node = node_map.get(source_node_id)
                        source_var = node_vars[source_node_id]

                        # Check if source has multiple outputs (like Vec3Split)
                        if source_node:
                            source_node_class = NODE_REGISTRY.get(source_node.type)
                            if source_node_class:
                                source_instance = source_node_class(**source_node.data)
                                source_outputs = source_instance.get_outputs()
                                # If source has multiple outputs, append the handle name
                                if len(source_outputs) > 1 and source_handle != "default":
                                    source_var = f"{source_var}_{source_handle}"

                        # Resolve through junctions to find the real source for type checks
                        real_source_id, real_source_node = self._resolve_through_junctions(
                            source_node_id, source_node, node_map, input_map
                        )

                        # If real source is an animation node (chaining animations)
                        if real_source_node and real_source_node.type in animation_types:
                            # Look up the actual mobject variable from the real source animation
                            chain_var = node_mobjects.get(real_source_id) or node_mobjects.get(source_node_id)
                            if not chain_var:
                                chain_var = f"{node_vars.get(real_source_id, source_var)}_mobject"
                            if copy_flag and input_name in ("mobject", "source"):
                                copy_prepend = f"{copy_var_name} = {chain_var}.copy()"
                                code = code.replace(placeholder, copy_var_name)
                                mobject_var = copy_var_name
                                node_mobjects[node_id] = copy_var_name
                            else:
                                code = code.replace(placeholder, chain_var)
                                mobject_var = chain_var
                                node_mobjects[node_id] = chain_var
                        # If real source is a shape/mobject node (start of animation path)
                        else:
                            # Use real source (past junctions) for type checking
                            real_cls = NODE_REGISTRY.get(real_source_node.type) if real_source_node else None
                            if real_cls and real_source_node:
                                real_instance = real_cls(**real_source_node.data)
                                real_outputs = real_instance.get_outputs()
                                if any(out_type in real_outputs.values() for out_type in ["Mobject", "shape", "mobject", "group"]):
                                    if copy_flag and input_name in ("mobject", "source"):
                                        copy_prepend = f"{copy_var_name} = {source_var}.copy()"
                                        code = code.replace(placeholder, copy_var_name)
                                        mobject_var = copy_var_name
                                        node_mobjects[node_id] = copy_var_name
                                    else:
                                        code = code.replace(placeholder, source_var)
                                        mobject_var = source_var
                                        node_mobjects[node_id] = source_var
                                else:
                                    code = code.replace(placeholder, source_var)
                            else:
                                code = code.replace(placeholder, source_var)

                # Special handling for ComposeMatrix: multiply connected matrices
                if node.type == "ComposeMatrix":
                    connected = []
                    for slot in ["m1", "m2", "m3", "m4"]:
                        src = input_map.get((node_id, slot))
                        if src:
                            connected.append(node_vars[src[0]])
                    if len(connected) >= 2:
                        # Reverse so m1 is applied first (rightmost in product)
                        connected = list(reversed(connected))
                        expr = f"np.matmul({connected[0]}, {connected[1]})"
                        for m in connected[2:]:
                            expr = f"np.matmul({expr}, {m})"
                        code = f"{var_name} = {expr}"
                    elif len(connected) == 1:
                        code = f"{var_name} = {connected[0]}.copy()"
                    else:
                        code = f"{var_name} = np.eye(4)"

                # Special handling for Transform node matrix
                if node.type == "Transform":
                    # Connected matrix is 4x4 homogeneous: extract 3x3 linear part + translation
                    # MANIM's apply_matrix takes a 3x3 for 3D linear transforms
                    matrix_info = input_map.get((node_id, "matrix"))

                    matrix_source_id = matrix_info[0] if matrix_info else None

                    if matrix_source_id:
                        matrix_var = node_vars[matrix_source_id]
                        code = code.replace("{MATRIX_2X2}", f"{matrix_var}[:3, :3]")
                        code = code.replace("{TRANSLATION}", f"{matrix_var}[:3, 3]")
                    else:
                        # Extract 2x2 linear transformation (rotation/scale/skew)
                        matrix_2x2 = f"[[{node_instance.m11}, {node_instance.m12}], [{node_instance.m21}, {node_instance.m22}]]"
                        # Extract translation vector from third column
                        translation = f"[{node_instance.m13}, {node_instance.m23}, 0]"
                        code = code.replace("{MATRIX_2X2}", matrix_2x2)
                        code = code.replace("{TRANSLATION}", translation)

                    # Store the mobject variable for chaining (Transform modifies the source mobject in place)
                    # The mobject_var should already be set from the input processing above
                    if mobject_var:
                        node_mobjects[node_id] = mobject_var

                # TransformInPlace: resolve {MOVE_TO} and track mobject
                if node.type == "TransformInPlace" and "{MOVE_TO}" in code:
                    target_info = input_map.get((node_id, "param_target"))
                    if target_info:
                        target_var = node_vars[target_info[0]]
                        code = code.replace("{MOVE_TO}", f"m.move_to(_{var_name}_ctr + alpha * (np.array({target_var}, dtype=float) - _{var_name}_ctr))")
                    else:
                        # No connected target — use node's own target parameter
                        target_val = getattr(node_instance, 'target', '[0, 0, 0]')
                        if target_val and target_val != '[0, 0, 0]':
                            code = code.replace("{MOVE_TO}", f"m.move_to(_{var_name}_ctr + alpha * (np.array({target_val}, dtype=float) - _{var_name}_ctr))")
                        else:
                            code = code.replace("{MOVE_TO}", "pass")
                    if mobject_var:
                        node_mobjects[node_id] = mobject_var

                # Resolve {ABOUT_POINT} placeholder for Rotate and Scale nodes
                if node.type in ("Rotate", "Scale") and "{ABOUT_POINT}" in code:
                    about_point_info = input_map.get((node_id, "param_about_point"))
                    about_point_source_id = about_point_info[0] if about_point_info else None

                    if about_point_source_id:
                        about_val = node_vars[about_point_source_id]
                    elif node_instance.about_point == "self":
                        # Use mobject's current center at runtime (respects prior MoveTo etc.)
                        about_val = f"{mobject_var}.get_center()" if mobject_var else "ORIGIN"
                    else:
                        point_map = {
                            "center": f"{mobject_var}.get_center()" if mobject_var else "ORIGIN",
                            "min": f"{mobject_var}.get_corner(DL)" if mobject_var else "DL",
                            "max": f"{mobject_var}.get_corner(UR)" if mobject_var else "UR",
                            "origin": "ORIGIN"
                        }
                        about_val = point_map.get(node_instance.about_point, f"{mobject_var}.get_center()" if mobject_var else "ORIGIN")

                    if about_val is None:
                        code = code.replace("{ABOUT_POINT}", "")
                    elif node.type == "Rotate":
                        # Rotate animated: "..., {ABOUT_POINT}run_time=..." → needs trailing comma
                        # Rotate instant: "...axis=...{ABOUT_POINT})" → needs leading comma
                        code = code.replace("{ABOUT_POINT}run_time", f"about_point={about_val}, run_time")
                        code = code.replace("{ABOUT_POINT}", f", about_point={about_val}")
                    else:
                        # Scale: "{param_scale_factor}{ABOUT_POINT})" → needs leading comma
                        code = code.replace("{ABOUT_POINT}", f", about_point={about_val}")

                # Special handling for Color node: Vec3 RGB input override and RGB output extraction
                if node.type == "Color":
                    rgb_info = input_map.get((node_id, "param_rgb"))
                    rgb_source_id = rgb_info[0] if rgb_info else None
                    if rgb_source_id:
                        rgb_var = node_vars[rgb_source_id]
                        # Override the color assignment with RGB conversion
                        code = f"_rgb = {rgb_var}\n        if any(v > 1.0 for v in _rgb): _rgb = [v/255.0 for v in _rgb]\n        {var_name} = rgb_to_color(np.array(_rgb))"

                # Handle parameter inputs (param_X placeholders)
                for input_name in inputs:
                    if input_name.startswith("param_"):
                        param_name = input_name[6:]  # Remove 'param_' prefix
                        placeholder = f"{{param_{param_name}}}"
                        source_info = input_map.get((node_id, input_name))

                        source_node_id = source_info[0] if source_info else None


                        if source_node_id:
                            # Use connected value
                            source_var = node_vars[source_node_id]

                            # Special handling for angle conversion (degrees to radians)
                            if param_name == "angle_rad":
                                code = code.replace(placeholder, f"np.radians({source_var})")
                            else:
                                code = code.replace(placeholder, source_var)
                        else:
                            # Use node's parameter value as fallback
                            if param_name == "angle_rad":
                                # Convert angle from degrees to radians
                                angle_str = getattr(node_instance, "angle", "90.0")
                                code = code.replace(placeholder, f"np.radians({angle_str})")
                            elif param_name == "color":
                                # Color fallback: use node's color field (quoted if hex)
                                color_val = getattr(node_instance, "color", "#FFFFFF")
                                if color_val.startswith('#'):
                                    code = code.replace(placeholder, f'"{color_val}"')
                                else:
                                    code = code.replace(placeholder, color_val)
                            elif hasattr(node_instance, param_name):
                                # Direct field access - fields are now expression strings
                                param_value = getattr(node_instance, param_name)
                                code = code.replace(placeholder, str(param_value))
                            else:
                                # Migration shim: handle old xyz format
                                if param_name == "position" and hasattr(node_instance, "x"):
                                    x = getattr(node_instance, "x", "0")
                                    y = getattr(node_instance, "y", "0")
                                    z = getattr(node_instance, "z", "0")
                                    code = code.replace(placeholder, f"[{x}, {y}, {z}]")
                                elif param_name == "start" and hasattr(node_instance, "start_x"):
                                    code = code.replace(placeholder, f"[{getattr(node_instance, 'start_x', '0')}, {getattr(node_instance, 'start_y', '0')}, {getattr(node_instance, 'start_z', '0')}]")
                                elif param_name == "end" and hasattr(node_instance, "end_x"):
                                    code = code.replace(placeholder, f"[{getattr(node_instance, 'end_x', '0')}, {getattr(node_instance, 'end_y', '0')}, {getattr(node_instance, 'end_z', '0')}]")
                                elif param_name == "axis" and hasattr(node_instance, "axis_x"):
                                    code = code.replace(placeholder, f"[{getattr(node_instance, 'axis_x', '0')}, {getattr(node_instance, 'axis_y', '0')}, {getattr(node_instance, 'axis_z', '1')}]")
                                elif param_name == "target" and hasattr(node_instance, "target_x"):
                                    code = code.replace(placeholder, f"[{getattr(node_instance, 'target_x', '0')}, {getattr(node_instance, 'target_y', '0')}, {getattr(node_instance, 'target_z', '0')}]")
                                else:
                                    code = code.replace(placeholder, "0")

                # DebugPrint: inject node ID and replace unresolved input placeholder
                if node.type == "DebugPrint":
                    code = code.replace("{node_id}", node_id)
                    if "{input_value}" in code:
                        code = code.replace("{input_value}", '"(no input connected)"')

                # FunctionCall: find matching FunctionDef, parse code, build args
                if node.type == "FunctionCall" and "{FUNC_ARGS}" in code:
                    func_args = []
                    for i in range(1, 9):
                        src = input_map.get((node_id, f"arg_{i}"))
                        if src:
                            func_args.append(node_vars[src[0]])
                    code = code.replace("{FUNC_ARGS}", ", ".join(func_args))

                # Add comment showing execution order
                lines.append(f"        # Execution: {exec_index}, Order: {node_order}, Type: {node.type}, ID: {node.id}")
                if copy_prepend:
                    lines.append(f"        {copy_prepend}")
                lines.append(f"        {code}")

                # FunctionCall: extract outputs from returned dict by key names
                if node.type == "FunctionCall":
                    # Find matching FunctionDef to get output key names
                    func_name = node_instance.func_name
                    func_def_code = None
                    for fn in self.graph.nodes:
                        if fn.type == "FunctionDef":
                            fn_data = fn.data if isinstance(fn.data, dict) else {}
                            if fn_data.get("func_name") == func_name:
                                func_def_code = fn_data.get("code", "")
                                break
                    if func_def_code:
                        _, output_keys = parse_function_code(func_def_code)
                    else:
                        output_keys = []

                    if output_keys:
                        for i, key in enumerate(output_keys):
                            lines.append(f"        {var_name}_out_{i+1} = {var_name}_result['{key}']")
                    else:
                        # Fallback: single output
                        lines.append(f"        {var_name}_out_1 = {var_name}_result")

                # Color node: extract r, g, b outputs only if connected
                if node.type == "Color":
                    rgb_outputs_used = any(
                        edge.source == node_id and edge.sourceHandle in ("r", "g", "b")
                        for edge in self.graph.edges
                    )
                    if rgb_outputs_used:
                        lines.append(f"        _c = color_to_rgb({var_name})")
                        lines.append(f"        {var_name}_r, {var_name}_g, {var_name}_b = _c[0], _c[1], _c[2]")

                # Shapes with edge outputs: alias + edge extraction + labels
                EDGE_SHAPE_SIDES = {"Triangle": 3, "Square": 4, "Rectangle": 4, "RightTriangle": 3, "IsoscelesTriangle": 3}
                if node.type in EDGE_SHAPE_SIDES:
                    n_sides = EDGE_SHAPE_SIDES[node.type]
                    lines.append(f"        {var_name}_shape = {var_name}")
                    edge_handles = {f"side_{i+1}" for i in range(n_sides)} | {"edges"}
                    edge_used = any(
                        edge.source == node_id and edge.sourceHandle in edge_handles
                        for edge in self.graph.edges
                    )
                    edge_labels_text = getattr(node_instance, 'edge_labels', '')
                    need_edges = edge_used or bool(edge_labels_text)
                    if need_edges:
                        lines.append(f"        _verts_{var_name} = {var_name}.get_vertices()")
                        for i in range(n_sides):
                            lines.append(f"        {var_name}_side_{i+1} = Line(_verts_{var_name}[{i}], _verts_{var_name}[{(i+1) % n_sides}], color={var_name}.get_color(), stroke_width={var_name}.get_stroke_width())")
                        side_list = ", ".join(f"{var_name}_side_{i+1}" for i in range(n_sides))
                        lines.append(f"        {var_name}_edges = VGroup({side_list})")
                        # Set outward-facing label directions (perpendicular to each edge, oriented outward)
                        lines.append(f"        _centroid_{var_name} = np.mean(_verts_{var_name}, axis=0)")
                        for i in range(n_sides):
                            j = (i + 1) % n_sides
                            lines.append(
                                f"        _ed = _verts_{var_name}[{j}] - _verts_{var_name}[{i}]; "
                                f"_perp = np.array([-_ed[1], _ed[0], 0]); "
                                f"_perp = _perp / (np.linalg.norm(_perp) + 1e-10); "
                                f"_mid = (_verts_{var_name}[{i}] + _verts_{var_name}[{j}]) / 2; "
                                f"{var_name}_side_{i+1}._label_direction = -_perp if np.dot(_perp, _centroid_{var_name} - _mid) > 0 else _perp"
                            )

                    # Generate center + edge labels
                    center_label_text = getattr(node_instance, 'label', '')
                    lbl_font = getattr(node_instance, 'label_font_size', '48.0')
                    lbl_offset = getattr(node_instance, 'label_offset', '0.3')
                    shape_label_vars = []

                    if center_label_text:
                        escaped = center_label_text.replace('"', '\\"')
                        lines.append(f'        {var_name}_center_label = MathTex(r"{escaped}", font_size={lbl_font})')
                        lines.append(f'        {var_name}_center_label.move_to({var_name}.get_center())')
                        shape_label_vars.append(f'{var_name}_center_label')

                    if edge_labels_text:
                        edge_label_list = [l.strip() for l in edge_labels_text.split(',')]
                        for i, el in enumerate(edge_label_list):
                            if el and i < n_sides:
                                escaped = el.replace('"', '\\"')
                                lbl_var = f'{var_name}_side_{i+1}_label'
                                lines.append(f'        {lbl_var} = MathTex(r"{escaped}", font_size={lbl_font})')
                                lines.append(f'        {lbl_var}.move_to({var_name}_side_{i+1}.point_from_proportion(0.5) + {lbl_offset} * {var_name}_side_{i+1}._label_direction)')
                                shape_label_vars.append(lbl_var)

                    if getattr(node_instance, 'write_label', False) and shape_label_vars:
                        pending_shape_labels[var_name] = shape_label_vars

                # Create output handle aliases for multi-output nodes
                # EDGE_SHAPE_SIDES and Line already create their own aliases above
                if node.type not in EDGE_SHAPE_SIDES and node.type != "Line":
                    _node_outputs = node_instance.get_outputs()
                    if len(_node_outputs) > 1:
                        for _handle_name in _node_outputs:
                            if _handle_name != "animation":
                                lines.append(f"        {var_name}_{_handle_name} = {var_name}")

                # Generate presentation animation for shapes with present != "none"
                present_mode = getattr(node_instance, 'present', 'show')
                if present_mode != "none" and node.type not in self._animation_types:
                    present_rt = getattr(node_instance, 'present_run_time', '1.0')
                    # Only generate presentation variable if NOT in a Sequence
                    # (Sequence handles presentation inline via _emit_shape_presentation)
                    if node_id not in animations_in_sequence:
                        pres_var = f"{var_name}_pres"
                        PRESENT_MAP = {
                            "show": None,  # handled inline
                            "create": f"Create({var_name}, run_time={present_rt})",
                            "fadein": f"FadeIn({var_name}, run_time={present_rt})",
                            "write": f"Write({var_name}, run_time={present_rt})",
                        }
                        pres_expr = PRESENT_MAP.get(present_mode)
                        if present_mode == "show":
                            if node_id in animations_in_group:
                                pass  # Can't put self.add() in AnimationGroup
                        elif pres_expr:
                            lines.append(f"        {pres_var} = {pres_expr}")
                    # Track the presentation variable for Sequence/AnimationGroup
                    node_mobjects[node_id] = var_name

                # Handle rendering based on node type
                outputs = node_instance.get_outputs()

                # Defer LineNode labels for post-animation rendering
                if node.type == "Line" and getattr(node_instance, 'write_label', False):
                    pending_shape_labels[var_name] = [f'{var_name}_label']

                # Generate center label for shapes that have label but no edge_labels (Circle, RegularPolygon)
                EDGE_SHAPE_TYPES = {"Triangle", "Square", "Rectangle", "RightTriangle", "IsoscelesTriangle"}
                if node.type not in EDGE_SHAPE_TYPES and node.type not in self._animation_types:
                    center_label_text = getattr(node_instance, 'label', '')
                    if center_label_text:
                        lbl_font = getattr(node_instance, 'label_font_size', '48.0')
                        escaped = center_label_text.replace('"', '\\"')
                        lines.append(f'        {var_name}_label = MathTex(r"{escaped}", font_size={lbl_font})')
                        lines.append(f'        {var_name}_label.move_to({var_name}.get_center())')

                # Resolve pending label key: strip _shape suffix to match base var
                _lbl_key = (mobject_var[:-6] if mobject_var and mobject_var.endswith('_shape') else mobject_var) if mobject_var else None
                if _lbl_key and _lbl_key not in pending_shape_labels:
                    _lbl_key = None  # no pending labels for this shape

                # Special handling for Show node - add mobject without animation
                if node.type == "Show":
                    if mobject_var:
                        lines.append(f"        self.add({mobject_var})")
                        # Add deferred labels from source shape
                        if _lbl_key:
                            for lbl_var in pending_shape_labels.pop(_lbl_key):
                                lines.append(f"        self.add({lbl_var})")
                # Animation nodes are NOT auto-played.
                # They only play through Sequence or AnimationGroup nodes.
                elif "animation" in outputs:
                    pass
                # Shapes are NOT automatically added - they need a Show node to render

                # Auto-add label for animation nodes with built-in labels (e.g. SquareFromEdge)
                if getattr(node_instance, 'write_label', False) and "animation" in outputs and node.type not in EDGE_SHAPE_SIDES:
                    lines.append(f"        self.add({var_name}_label)")

            except Exception as e:
                error_msg = f"Error generating code for node {node_id}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                lines.append(f"        # {error_msg}")

        # If no animations were played, add a wait to ensure video is generated
        if not has_animations and len(lines) > 2:
            lines.append("        self.wait(2)  # Show static scene")

        # If no nodes generated code, add a pass statement
        if len(lines) == 2:
            lines.append("        pass")

        return "\n".join(lines)

    def _collect_chain_animations(self, anim_node_id: str, input_map: dict, node_map: dict,
                                    animations_in_sequence: set, animations_in_group: set) -> list:
        """Walk back from an animation node through mobject/source inputs to find
        upstream animation nodes not directly in any Sequence or AnimationGroup.
        Returns list of node IDs in chain order (upstream first)."""
        chain = []
        current_id = anim_node_id
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            current_node = node_map.get(current_id)
            if not current_node or current_node.type not in self._animation_types:
                break

            # Walk back through mobject/source input
            upstream_anim_id = None
            for handle in ["mobject", "source"]:
                source_info = input_map.get((current_id, handle))
                if source_info:
                    src_id = source_info[0]
                    src_node = node_map.get(src_id)
                    if src_node and src_node.type in self._animation_types:
                        upstream_anim_id = src_id
                        break

            if not upstream_anim_id:
                break

            # Only include if not already directly in a Sequence or AnimationGroup
            if upstream_anim_id not in animations_in_sequence and upstream_anim_id not in animations_in_group:
                chain.append(upstream_anim_id)

            current_id = upstream_anim_id

        return list(reversed(chain))  # upstream first

    def _play_with_labels(self, node_id: str, var_name: str, node_mobjects: dict,
                          pending_shape_labels: dict, lines: list):
        """Play an animation and emit any deferred labels for its shape."""
        lines.append(f"        self.play({var_name})")
        mob_var = node_mobjects.get(node_id)
        lbl_key = (mob_var[:-6] if mob_var and mob_var.endswith('_shape') else mob_var) if mob_var else None
        if lbl_key and lbl_key in pending_shape_labels:
            for lbl_var in pending_shape_labels.pop(lbl_key):
                lines.append(f"        self.add({lbl_var})")

    def _emit_animation_inline(self, node_id: str, input_map: dict, node_map: dict,
                               node_vars: dict, node_mobjects: dict, lines: list,
                               pending_shape_labels: dict):
        """Generate animation code inline and play it immediately.

        This is used by Sequences so that animations are created and played
        back-to-back, ensuring runtime evaluations (e.g. mob.get_center())
        happen AFTER prior animations in the sequence have played.
        """
        node = node_map.get(node_id)
        if not node:
            return

        node_class = NODE_REGISTRY[node.type]
        node_instance = node_class(**node.data)
        var_name = node_vars[node_id]
        code = node_instance.to_manim_code(var_name)

        # Resolve input placeholders
        inputs = node_instance.get_inputs()
        mobject_var = None
        copy_flag = getattr(node_instance, 'copy', False)
        copy_var_name = f"{var_name}_src" if copy_flag else None
        copy_prepend = None

        for input_name in inputs:
            placeholder = f"{{input_{input_name}}}"
            source_info = input_map.get((node_id, input_name))
            if source_info:
                source_node_id, source_handle = source_info
                source_node = node_map.get(source_node_id)
                source_var = node_vars[source_node_id]

                # Multi-output handle
                if source_node:
                    source_node_class = NODE_REGISTRY.get(source_node.type)
                    if source_node_class:
                        source_instance = source_node_class(**source_node.data)
                        source_outputs = source_instance.get_outputs()
                        if len(source_outputs) > 1 and source_handle != "default":
                            source_var = f"{source_var}_{source_handle}"

                # Resolve through junctions to find the real source for type checks
                real_source_id, real_source_node = self._resolve_through_junctions(
                    source_node_id, source_node, node_map, input_map
                )

                # Animation chaining
                if real_source_node and real_source_node.type in self._animation_types:
                    chain_var = node_mobjects.get(real_source_id) or node_mobjects.get(source_node_id)
                    if not chain_var:
                        chain_var = f"{node_vars.get(real_source_id, source_var)}_mobject"
                    if copy_flag and input_name in ("mobject", "source"):
                        copy_prepend = f"{copy_var_name} = {chain_var}.copy()"
                        code = code.replace(placeholder, copy_var_name)
                        mobject_var = copy_var_name
                        node_mobjects[node_id] = copy_var_name
                    else:
                        code = code.replace(placeholder, chain_var)
                        mobject_var = chain_var
                        node_mobjects[node_id] = chain_var
                else:
                    real_cls = NODE_REGISTRY.get(real_source_node.type) if real_source_node else None
                    if real_cls and real_source_node:
                        real_instance = real_cls(**real_source_node.data)
                        real_outputs = real_instance.get_outputs()
                        if any(out_type in real_outputs.values() for out_type in ["Mobject", "shape", "mobject", "group"]):
                            if copy_flag and input_name in ("mobject", "source"):
                                copy_prepend = f"{copy_var_name} = {source_var}.copy()"
                                code = code.replace(placeholder, copy_var_name)
                                mobject_var = copy_var_name
                                node_mobjects[node_id] = copy_var_name
                            else:
                                code = code.replace(placeholder, source_var)
                                mobject_var = source_var
                                node_mobjects[node_id] = source_var
                        else:
                            code = code.replace(placeholder, source_var)
                    else:
                        code = code.replace(placeholder, source_var)

        # Resolve {MOVE_TO} for TransformInPlace
        if node.type == "TransformInPlace" and "{MOVE_TO}" in code:
            target_info = input_map.get((node_id, "param_target"))
            if target_info:
                target_var = node_vars[target_info[0]]
                code = code.replace("{MOVE_TO}", f"m.move_to(_{var_name}_ctr + alpha * (np.array({target_var}, dtype=float) - _{var_name}_ctr))")
            else:
                # No connected target — use node's own target parameter
                target_val = getattr(node_instance, 'target', '[0, 0, 0]')
                if target_val and target_val != '[0, 0, 0]':
                    code = code.replace("{MOVE_TO}", f"m.move_to(_{var_name}_ctr + alpha * (np.array({target_val}, dtype=float) - _{var_name}_ctr))")
                else:
                    code = code.replace("{MOVE_TO}", "pass")
            if mobject_var:
                node_mobjects[node_id] = mobject_var

        # Resolve {MATRIX_2X2} and {TRANSLATION} for Transform
        if node.type == "Transform" and ("{MATRIX_2X2}" in code or "{TRANSLATION}" in code):
            matrix_info = input_map.get((node_id, "matrix"))
            matrix_source_id = matrix_info[0] if matrix_info else None
            if matrix_source_id:
                matrix_var = node_vars[matrix_source_id]
                code = code.replace("{MATRIX_2X2}", f"{matrix_var}[:3, :3]")
                code = code.replace("{TRANSLATION}", f"{matrix_var}[:3, 3]")
            else:
                matrix_2x2 = f"[[{node_instance.m11}, {node_instance.m12}], [{node_instance.m21}, {node_instance.m22}]]"
                translation = f"[{node_instance.m13}, {node_instance.m23}, 0]"
                code = code.replace("{MATRIX_2X2}", matrix_2x2)
                code = code.replace("{TRANSLATION}", translation)
            if mobject_var:
                node_mobjects[node_id] = mobject_var

        # Resolve {ABOUT_POINT} for Rotate and Scale
        if node.type in ("Rotate", "Scale") and "{ABOUT_POINT}" in code:
            about_point_info = input_map.get((node_id, "param_about_point"))
            about_point_source_id = about_point_info[0] if about_point_info else None
            if about_point_source_id:
                about_val = node_vars[about_point_source_id]
            elif node_instance.about_point == "self":
                about_val = f"{mobject_var}.get_center()" if mobject_var else "ORIGIN"
            else:
                point_map = {
                    "center": f"{mobject_var}.get_center()" if mobject_var else "ORIGIN",
                    "min": f"{mobject_var}.get_corner(DL)" if mobject_var else "DL",
                    "max": f"{mobject_var}.get_corner(UR)" if mobject_var else "UR",
                    "origin": "ORIGIN"
                }
                about_val = point_map.get(node_instance.about_point, f"{mobject_var}.get_center()" if mobject_var else "ORIGIN")
            if about_val is None:
                code = code.replace("{ABOUT_POINT}", "")
            elif node.type == "Rotate":
                code = code.replace("{ABOUT_POINT}run_time", f"about_point={about_val}, run_time")
                code = code.replace("{ABOUT_POINT}", f", about_point={about_val}")
            else:
                code = code.replace("{ABOUT_POINT}", f", about_point={about_val}")

        # Resolve parameter inputs
        for input_name in inputs:
            if input_name.startswith("param_"):
                param_name = input_name[6:]
                placeholder = f"{{param_{param_name}}}"
                source_info = input_map.get((node_id, input_name))
                source_node_id = source_info[0] if source_info else None
                if source_node_id:
                    source_var = node_vars[source_node_id]
                    if param_name == "angle_rad":
                        code = code.replace(placeholder, f"np.radians({source_var})")
                    else:
                        code = code.replace(placeholder, source_var)
                else:
                    if param_name == "angle_rad":
                        angle_str = getattr(node_instance, "angle", "90.0")
                        code = code.replace(placeholder, f"np.radians({angle_str})")
                    elif param_name == "color":
                        color_val = getattr(node_instance, "color", "#FFFFFF")
                        if color_val.startswith('#'):
                            code = code.replace(placeholder, f'"{color_val}"')
                        else:
                            code = code.replace(placeholder, color_val)
                    elif hasattr(node_instance, param_name):
                        param_value = getattr(node_instance, param_name)
                        code = code.replace(placeholder, str(param_value))
                    else:
                        if param_name == "position" and hasattr(node_instance, "x"):
                            x = getattr(node_instance, "x", "0")
                            y = getattr(node_instance, "y", "0")
                            z = getattr(node_instance, "z", "0")
                            code = code.replace(placeholder, f"[{x}, {y}, {z}]")
                        elif param_name == "target" and hasattr(node_instance, "target_x"):
                            code = code.replace(placeholder, f"[{getattr(node_instance, 'target_x', '0')}, {getattr(node_instance, 'target_y', '0')}, {getattr(node_instance, 'target_z', '0')}]")
                        elif param_name == "axis" and hasattr(node_instance, "axis_x"):
                            code = code.replace(placeholder, f"[{getattr(node_instance, 'axis_x', '0')}, {getattr(node_instance, 'axis_y', '0')}, {getattr(node_instance, 'axis_z', '1')}]")
                        else:
                            code = code.replace(placeholder, "0")

        # Emit code
        if copy_prepend:
            lines.append(f"        {copy_prepend}")
        lines.append(f"        {code}")

        # Play the animation
        lines.append(f"        self.play({var_name})")

        # State extraction after animation plays
        if node.type == "MoveTo" and mobject_var:
            lines.append(f"        {var_name}_position = list({mobject_var}.get_center())")
        elif node.type == "Rotate" and mobject_var:
            angle_str = getattr(node_instance, "angle", "90.0")
            lines.append(f"        {var_name}_angle = {angle_str}")
        elif node.type == "Scale" and mobject_var:
            sf_str = getattr(node_instance, "scale_factor", "2.0")
            lines.append(f"        {var_name}_scale_factor = {sf_str}")

        # Emit deferred labels
        _lbl_key = (mobject_var[:-6] if mobject_var and mobject_var.endswith('_shape') else mobject_var) if mobject_var else None
        if _lbl_key and _lbl_key in pending_shape_labels:
            for lbl_var in pending_shape_labels.pop(_lbl_key):
                lines.append(f"        self.add({lbl_var})")

    def _emit_sequence_animations(self, node_id: str, input_map: dict, node_map: dict,
                                  node_vars: dict, node_mobjects: dict, lines: list,
                                  pending_shape_labels: dict = {},
                                  animations_in_sequence: set = set(),
                                  animations_in_group: set = set()):
        """Recursively emit self.play()/self.add()/camera calls for a Sequence node."""
        node = node_map[node_id]
        instance = NODE_REGISTRY["Sequence"](**node.data)
        wait_time = instance.wait_time

        for i in range(1, 11):  # anim1 to anim10
            anim_input = f"anim{i}"
            source_info = input_map.get((node_id, anim_input))
            source_node_id = source_info[0] if source_info else None

            if not source_node_id:
                continue

            source_node = node_map.get(source_node_id)
            source_var = node_vars[source_node_id]

            if source_node and source_node.type == "Sequence":
                # Recurse into nested Sequence
                self._emit_sequence_animations(source_node_id, input_map, node_map, node_vars,
                                               node_mobjects, lines, pending_shape_labels,
                                               animations_in_sequence, animations_in_group)
            elif source_node and source_node.type == "Show":
                # Show node: resolve mobject inline
                mob_var = node_mobjects.get(source_node_id)
                if not mob_var:
                    mob_var = f"{source_var}_mobject"
                lines.append(f"        self.add({mob_var})")
                # Add deferred labels
                _lbl_key = (mob_var[:-6] if mob_var.endswith('_shape') else mob_var) if mob_var else None
                if _lbl_key and _lbl_key in pending_shape_labels:
                    for lbl_var in pending_shape_labels.pop(_lbl_key):
                        lines.append(f"        self.add({lbl_var})")
            elif source_node and source_node.type in ["SetCameraOrientation", "MoveCamera", "ZoomCamera"]:
                self._emit_camera_command(source_node, lines)
            elif source_node and source_node.type == "AnimationGroup":
                # AnimationGroup was pre-created in main loop, just play it
                lines.append(f"        self.play({source_var})")
            elif source_node and self._is_shape_with_presentation(source_node):
                # Shape with built-in presentation: emit presentation inline
                self._emit_shape_presentation(source_node_id, node_map, node_vars,
                                              pending_shape_labels, lines)
            else:
                # Regular animation: generate code inline and play immediately
                # First, handle upstream chain animations (not in any Sequence or Group)
                chain = self._collect_chain_animations(source_node_id, input_map, node_map,
                                                       animations_in_sequence, animations_in_group)
                for chain_id in chain:
                    self._emit_animation_inline(chain_id, input_map, node_map, node_vars,
                                                node_mobjects, lines, pending_shape_labels)

                # Generate and play this animation inline
                self._emit_animation_inline(source_node_id, input_map, node_map, node_vars,
                                            node_mobjects, lines, pending_shape_labels)

            # Add wait time after each animation
            if wait_time != "0" and wait_time != "0.0":
                lines.append(f"        self.wait({wait_time})")

    def _emit_camera_command(self, cam_node, lines: list):
        """Emit a self.move_camera() or self.set_camera_orientation() call for a camera node."""
        cam_class = NODE_REGISTRY[cam_node.type]
        inst = cam_class(**cam_node.data)
        lines.append(f"        # Camera movement from {cam_node.type}")
        if cam_node.type == "SetCameraOrientation":
            phi_rad = f"np.radians({inst.phi})"
            theta_rad = f"np.radians({inst.theta})"
            gamma_rad = f"np.radians({inst.gamma})"
            if inst.run_time != "0" and inst.run_time != "0.0":
                lines.append(f"        self.move_camera(phi={phi_rad}, theta={theta_rad}, gamma={gamma_rad}, run_time={inst.run_time})")
            else:
                lines.append(f"        self.set_camera_orientation(phi={phi_rad}, theta={theta_rad}, gamma={gamma_rad})")
        elif cam_node.type == "MoveCamera":
            lines.append(f"        self.move_camera(frame_center={inst.position}, run_time={inst.run_time})")
        elif cam_node.type == "ZoomCamera":
            lines.append(f"        self.move_camera(zoom={inst.scale}, run_time={inst.run_time})")

    def _is_shape_with_presentation(self, node) -> bool:
        """Check if a node is a shape with built-in presentation enabled."""
        if node.type in self._animation_types:
            return False
        # Check the data dict directly
        node_data = node.data if isinstance(node.data, dict) else {}
        present = node_data.get('present', 'create')
        return present != 'none' and present is not None

    def _emit_shape_presentation(self, node_id: str, node_map: dict, node_vars: dict,
                                 pending_shape_labels: dict, lines: list):
        """Emit presentation animation for a shape with present != 'none'."""
        node = node_map.get(node_id)
        if not node:
            return

        node_class = NODE_REGISTRY[node.type]
        node_instance = node_class(**node.data)
        var_name = node_vars[node_id]
        present_mode = getattr(node_instance, 'present', 'show')
        present_rt = getattr(node_instance, 'present_run_time', '1.0')

        if present_mode == "show":
            lines.append(f"        self.add({var_name})")
        elif present_mode == "create":
            lines.append(f"        self.play(Create({var_name}, run_time={present_rt}))")
        elif present_mode == "fadein":
            lines.append(f"        self.play(FadeIn({var_name}, run_time={present_rt}))")
        elif present_mode == "write":
            lines.append(f"        self.play(Write({var_name}, run_time={present_rt}))")

        # Emit deferred labels after the animation completes
        if var_name in pending_shape_labels:
            for lbl_var in pending_shape_labels.pop(var_name):
                lines.append(f"        self.add({lbl_var})")

    def _find_root_mobject(self, anim_node_id: str, input_map: dict, node_vars: dict, node_map: dict) -> str:
        """Find the root mobject in an animation chain by walking backwards"""
        current_node = node_map.get(anim_node_id)
        if not current_node:
            return node_vars.get(anim_node_id, "unknown")

        # Walk back through the chain until we find a shape node
        while current_node:
            # Check if this is a shape node (not an animation)
            if current_node.type not in self._animation_types:
                # Found the root shape
                return node_vars[current_node.id]

            # This is an animation node, find what's connected to its mobject input
            mobject_input = None
            for handle in ["mobject", "source"]:  # Check common input names
                source_info = input_map.get((current_node.id, handle))

                source_node_id = source_info[0] if source_info else None

                if source_node_id:
                    mobject_input = source_node_id
                    break

            if not mobject_input:
                # No input found, return current node's var
                return node_vars[current_node.id]

            # Continue walking back
            current_node = node_map.get(mobject_input)

        # Fallback
        return node_vars.get(anim_node_id, "unknown")

    @staticmethod
    def _resolve_through_junctions(source_node_id, source_node, node_map, input_map):
        """Follow junction chain to find the real (non-Junction) source node."""
        visited = set()
        current_id = source_node_id
        current_node = source_node
        while current_node and current_node.type == "Junction" and current_id not in visited:
            visited.add(current_id)
            upstream = input_map.get((current_id, "in"))
            if upstream:
                current_id = upstream[0]
                current_node = node_map.get(current_id)
            else:
                break
        return current_id, current_node

    def _pre_populate_node_mobjects(self, node_id: str, node_instance, input_map: dict,
                                     node_map: dict, node_vars: dict, node_mobjects: dict):
        """Pre-populate node_mobjects for a skipped animation node.

        When an animation is in a Sequence, it's skipped in the main loop.
        But downstream non-animation nodes (e.g. GetVertex) may need to
        reference the mobject this animation operates on. This method
        resolves the input mobject and stores it in node_mobjects so the
        fallback f"{var}_mobject" pattern is never reached.
        """
        for handle in ("mobject", "source"):
            source_info = input_map.get((node_id, handle))
            if not source_info:
                continue
            source_node_id, source_handle = source_info
            source_node = node_map.get(source_node_id)
            source_var = node_vars.get(source_node_id, "")

            # Multi-output handle
            if source_node:
                src_cls = NODE_REGISTRY.get(source_node.type)
                if src_cls:
                    src_inst = src_cls(**source_node.data)
                    src_outs = src_inst.get_outputs()
                    if len(src_outs) > 1 and source_handle != "default":
                        source_var = f"{source_var}_{source_handle}"

            # Resolve through junctions
            real_id, real_node = self._resolve_through_junctions(
                source_node_id, source_node, node_map, input_map
            )

            # If upstream is an animation, use its tracked mobject
            if real_node and real_node.type in self._animation_types:
                mob_var = node_mobjects.get(real_id) or node_mobjects.get(source_node_id)
                if mob_var:
                    node_mobjects[node_id] = mob_var
                else:
                    # Fallback: use the source variable directly
                    node_mobjects[node_id] = source_var
            else:
                node_mobjects[node_id] = source_var
            break  # Only process the first mobject/source input

    def _get_node_by_id(self, node_id: str):
        """Find node by ID"""
        for node in self.graph.nodes:
            if node.id == node_id:
                return node
        return None

    def _sanitize_var_name(self, name: str) -> str:
        """Sanitize a string into a valid Python identifier"""
        import re
        # Replace non-alphanumeric with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure doesn't start with digit
        if sanitized and sanitized[0].isdigit():
            sanitized = '_' + sanitized
        # Fallback if empty
        if not sanitized:
            sanitized = 'node'
        return sanitized

    # Manim built-in constant vectors — singleton names, no code generated
    CONST_VEC_TYPES = {"RIGHT", "LEFT", "UP", "DOWN", "OUT", "IN", "ORIGIN"}
    CONST_VEC_ALIASES = {"X": "RIGHT", "Y": "UP", "Z": "OUT"}

    def _safe_var_name(self, node_id: str, node_type: str, node_data: dict = {}) -> str:
        """Generate a safe Python variable name, preferring user-given name"""
        # Built-in constant vectors always use their Manim name
        if node_type in self.CONST_VEC_TYPES:
            return node_type
        if node_type in self.CONST_VEC_ALIASES:
            return self.CONST_VEC_ALIASES[node_type]

        # Use user-given name if available
        if node_data and node_data.get('name'):
            return self._sanitize_var_name(node_data['name'])

        # Sequential counter per type: circle_1, circle_2, etc.
        prefix = node_type.lower().replace(" ", "_")
        count = self._type_counters.get(prefix, 0) + 1
        self._type_counters[prefix] = count
        return f"{prefix}_{count}"
