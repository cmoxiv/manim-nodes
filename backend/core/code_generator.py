from typing import Dict, List
import logging
from ..models.graph import Graph
from ..nodes import NODE_REGISTRY
from .graph_validator import GraphValidator, ValidationError

logger = logging.getLogger("manim_nodes")


class CodeGenerator:
    """Generates MANIM Python code from node graphs"""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.validator = GraphValidator(graph)

        # Build dynamic set of animation type names from NODE_REGISTRY
        self._animation_types: set = set()
        for reg_name, reg_cls in NODE_REGISTRY.items():
            try:
                if "Animation" in reg_cls().get_outputs().values():
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
            raise ValidationError(f"Graph validation failed:\n{error_messages}")

        # Get execution order
        execution_order = self.validator.get_execution_order()

        # Generate code
        code_parts = []

        # Imports
        code_parts.append(self._generate_imports())
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

            # Deduplicate: if name already used, append short hash suffix
            if base_name in used_names:
                base_name = f"{base_name}_{self._get_short_id(node.id)}"
            used_names.add(base_name)

            node_vars[node.id] = base_name

        # Build sets of animation nodes in Sequence and AnimationGroup
        animations_in_sequence = set()
        animations_in_group = set()
        for node in self.graph.nodes:
            if node.type == "Sequence":
                # Animations in Sequence are generated inline
                for i in range(1, 6):
                    input_name = f"anim{i}"
                    source_info = input_map.get((node.id, input_name))
                    source_node_id = source_info[0] if source_info else None

                    if source_node_id:
                        animations_in_sequence.add(source_node_id)
            elif node.type == "AnimationGroup":
                # Animations in AnimationGroup need objects created but not played
                for i in range(1, 6):
                    input_name = f"anim{i}"
                    source_info = input_map.get((node.id, input_name))
                    source_node_id = source_info[0] if source_info else None

                    if source_node_id:
                        animations_in_group.add(source_node_id)

        # Build mapping of node_id -> mobject_variable for animation chains
        node_mobjects: Dict[str, str] = {}

        # Track if any animations were played
        has_animations = False

        # Generate code for each node in execution order
        for exec_index, node_id in enumerate(execution_order, start=1):
            node = node_map.get(node_id)
            if not node:
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
                    self._emit_sequence_animations(node_id, input_map, node_map, node_vars, node_mobjects, lines)

                    has_animations = True
                    continue  # Skip normal processing for Sequence

                # Special handling for AnimationGroup node
                if node.type == "AnimationGroup":
                    var_name = node_vars[node_id]
                    # Collect connected animations
                    connected_anims = []
                    for i in range(1, 6):
                        anim_name = f"anim{i}"
                        source_info = input_map.get((node_id, anim_name))

                        source_node_id = source_info[0] if source_info else None

                        if source_node_id:
                            source_var = node_vars[source_node_id]
                            connected_anims.append(source_var)

                    if connected_anims:
                        # Add comment showing execution order
                        lines.append(f"        # Execution: {exec_index}, Order: {node_order}, Type: {node.type}")
                        anims_str = ", ".join(connected_anims)

                        # Check if this AnimationGroup is used in a Sequence
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

                    continue  # Skip normal processing for AnimationGroup

                # Special handling for Group node
                if node.type == "Group":
                    var_name = node_vars[node_id]
                    # Collect connected objects
                    connected_objs = []
                    for i in range(1, 6):
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
                            # Expand Create to create each group member
                            var_name = node_vars[node_id]
                            source_var = node_vars[mobject_source_id]

                            # Generate: self.play(*[Create(obj) for obj in group])
                            lines.append(f"        # Create each object in group")
                            lines.append(f"        self.play(*[Create(obj, run_time={node_instance.run_time}) for obj in {source_var}])")

                            # Store the group as the mobject for chaining
                            node_mobjects[node_id] = source_var

                            continue  # Skip normal processing for Create with Group

                # Skip camera nodes that are in a Sequence - they'll be handled inline in the Sequence
                if node.type in ["SetCameraOrientation", "MoveCamera", "ZoomCamera"] and node_id in animations_in_sequence:
                    continue

                var_name = node_vars[node_id]
                code = node_instance.to_manim_code(var_name)

                # Replace input placeholders with actual variable names
                inputs = node_instance.get_inputs()
                mobject_var = None  # Track the mobject variable for this animation

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

                        # If source is an animation node (chaining animations)
                        if source_node and source_node.type in animation_types:
                            # Look up the actual mobject variable from the source animation
                            chain_var = node_mobjects.get(source_node_id)
                            if not chain_var:
                                # Fallback to naming convention if not found
                                chain_var = f"{source_var}_mobject"
                            code = code.replace(placeholder, chain_var)
                            mobject_var = chain_var  # Remember for later
                            node_mobjects[node_id] = chain_var  # Store for next animation in chain
                        # If source is a shape/mobject node (start of animation path)
                        else:
                            # Check if source outputs shape/mobject type
                            source_node_class = NODE_REGISTRY.get(source_node.type) if source_node else None
                            if source_node_class and source_node:
                                source_instance = source_node_class(**source_node.data)
                                source_outputs = source_instance.get_outputs()
                                # Pass through the original shape (no copying)
                                # Animations modify the original object, making chaining more intuitive
                                if any(out_type in source_outputs.values() for out_type in ["Mobject", "shape", "mobject", "group"]):
                                    code = code.replace(placeholder, source_var)
                                    mobject_var = source_var  # Use original, not a copy
                                    node_mobjects[node_id] = source_var  # Store original for next animation in chain
                                else:
                                    code = code.replace(placeholder, source_var)
                            else:
                                code = code.replace(placeholder, source_var)

                # Special handling for Transform node matrix
                if node.type == "Transform":
                    # MANIM's ApplyMatrix only applies the 2x2 linear transformation
                    # Translation must be applied separately
                    matrix_info = input_map.get((node_id, "matrix"))

                    matrix_source_id = matrix_info[0] if matrix_info else None

                    if matrix_source_id:
                        # Use connected matrix (assume it's already in correct format)
                        matrix_var = node_vars[matrix_source_id]
                        code = code.replace("{MATRIX_2X2}", matrix_var)
                        code = code.replace("{TRANSLATION}", "[0, 0, 0]")  # No translation if matrix is connected
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

                # Special handling for Rotate node about_point
                if node.type == "Rotate":
                    # Check if custom about_point (Vec3) is connected
                    about_point_info = input_map.get((node_id, "param_about_point"))

                    about_point_source_id = about_point_info[0] if about_point_info else None

                    if about_point_source_id:
                        # Use connected Vec3 value
                        about_var = node_vars[about_point_source_id]
                        code = code.replace("{ABOUT_POINT}", about_var)
                    else:
                        # Use predefined about_point mode
                        point_map = {
                            "center": f"{mobject_var}.get_center()" if mobject_var else "ORIGIN",
                            "min": f"{mobject_var}.get_corner(DL)" if mobject_var else "DL",
                            "max": f"{mobject_var}.get_corner(UR)" if mobject_var else "UR",
                            "origin": "ORIGIN"
                        }
                        about = point_map.get(node_instance.about_point, f"{mobject_var}.get_center()" if mobject_var else "ORIGIN")
                        code = code.replace("{ABOUT_POINT}", about)

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

                # Add comment showing execution order
                lines.append(f"        # Execution: {exec_index}, Order: {node_order}, Type: {node.type}")
                lines.append(f"        {code}")

                # Color node: extract r, g, b outputs only if connected
                if node.type == "Color":
                    rgb_outputs_used = any(
                        edge.source == node_id and edge.sourceHandle in ("r", "g", "b")
                        for edge in self.graph.edges
                    )
                    if rgb_outputs_used:
                        lines.append(f"        _c = color_to_rgb({var_name})")
                        lines.append(f"        {var_name}_r, {var_name}_g, {var_name}_b = _c[0], _c[1], _c[2]")

                # Handle rendering based on node type
                outputs = node_instance.get_outputs()

                # Special handling for Show node - add mobject without animation
                if node.type == "Show":
                    if mobject_var:
                        lines.append(f"        self.add({mobject_var})")
                # If this is an animation node, play it if not in a Sequence or AnimationGroup
                elif "animation" in outputs:
                    # Check if animation should be played or applied instantly
                    should_animate = getattr(node_instance, 'animate', True)

                    # Skip if this animation is in a Sequence or AnimationGroup (handled separately)
                    # Also skip camera nodes - they execute their movements directly
                    if node_id not in animations_in_sequence and node_id not in animations_in_group:
                        # Camera nodes execute directly, don't play them
                        if node.type in ["SetCameraOrientation", "MoveCamera", "ZoomCamera"]:
                            # Camera movements already executed in their to_manim_code()
                            pass
                        elif should_animate:
                            lines.append(f"        self.play({var_name})")
                            has_animations = True
                        else:
                            # Apply transformation instantly (no animation)
                            # The transformation was already applied in the code generation
                            # Just mark that we had content
                            pass
                # Shapes are NOT automatically added - they need a Show node to render

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

    def _emit_sequence_animations(self, node_id: str, input_map: dict, node_map: dict, node_vars: dict, node_mobjects: dict, lines: list):
        """Recursively emit self.play()/self.add()/camera calls for a Sequence node."""
        node = node_map[node_id]
        instance = NODE_REGISTRY["Sequence"](**node.data)
        wait_time = instance.wait_time

        for i in range(1, 6):  # anim1 to anim5
            anim_input = f"anim{i}"
            source_info = input_map.get((node_id, anim_input))
            source_node_id = source_info[0] if source_info else None

            if not source_node_id:
                continue

            source_node = node_map.get(source_node_id)
            source_var = node_vars[source_node_id]

            if source_node and source_node.type == "Sequence":
                # Recurse into nested Sequence
                self._emit_sequence_animations(source_node_id, input_map, node_map, node_vars, node_mobjects, lines)
            elif source_node and source_node.type == "Show":
                mobject_var = f"{source_var}_mobject"
                lines.append(f"        self.add({mobject_var})")
            elif source_node and source_node.type in ["SetCameraOrientation", "MoveCamera", "ZoomCamera"]:
                lines.append(f"        # Camera movement from {source_node.type}")
                source_node_class = NODE_REGISTRY[source_node.type]
                source_instance = source_node_class(**source_node.data)

                if source_node.type == "SetCameraOrientation":
                    phi_rad = f"np.radians({source_instance.phi})"
                    theta_rad = f"np.radians({source_instance.theta})"
                    gamma_rad = f"np.radians({source_instance.gamma})"
                    if source_instance.run_time != "0" and source_instance.run_time != "0.0":
                        lines.append(f"        self.move_camera(phi={phi_rad}, theta={theta_rad}, gamma={gamma_rad}, run_time={source_instance.run_time})")
                    else:
                        lines.append(f"        self.set_camera_orientation(phi={phi_rad}, theta={theta_rad}, gamma={gamma_rad})")
                elif source_node.type == "MoveCamera":
                    lines.append(f"        self.move_camera(frame_center={source_instance.position}, run_time={source_instance.run_time})")
                elif source_node.type == "ZoomCamera":
                    lines.append(f"        self.move_camera(zoom={source_instance.scale}, run_time={source_instance.run_time})")
            else:
                lines.append(f"        self.play({source_var})")

            # Add wait time after each animation
            if wait_time != "0" and wait_time != "0.0":
                lines.append(f"        self.wait({wait_time})")

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

    def _get_node_by_id(self, node_id: str):
        """Find node by ID"""
        for node in self.graph.nodes:
            if node.id == node_id:
                return node
        return None

    def _get_short_id(self, node_id: str) -> str:
        """Generate a short hash ID from node_id"""
        import hashlib
        return hashlib.md5(node_id.encode()).hexdigest()[:6]

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

    def _safe_var_name(self, node_id: str, node_type: str, node_data: dict = {}) -> str:
        """Generate a safe Python variable name, preferring user-given name"""
        # Use user-given name if available
        if node_data and node_data.get('name'):
            return self._sanitize_var_name(node_data['name'])

        # Fallback to type + hash
        prefix = node_type.lower().replace(" ", "_")
        hash_suffix = self._get_short_id(node_id)
        return f"{prefix}_{hash_suffix}"
