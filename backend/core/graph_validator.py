from typing import Dict, List, Optional, Set, Tuple
from collections import deque
import logging
from ..models.graph import Graph
from ..nodes import NODE_REGISTRY

logger = logging.getLogger("manim_nodes")


class ValidationError(Exception):
    """Raised when graph validation fails"""
    def __init__(self, message: str, node_id: str = None):
        self.message = message
        self.node_id = node_id
        super().__init__(message)


class GraphValidator:
    """Validates node graphs before code generation"""

    def __init__(self, graph: Graph):
        self.graph = graph
        self.errors: List[Tuple[str, str]] = []  # (node_id, error_message)
        self._cycle_cache: Optional[bool] = None  # Cache for cycle detection

    def validate(self) -> Tuple[bool, List[Tuple[str, str]]]:
        """
        Validate the entire graph.

        Returns:
            Tuple of (is_valid, list of (node_id, error_message))
        """
        self.errors = []

        # Check for empty graph
        if not self.graph.nodes:
            self.errors.append((None, "Graph is empty"))
            return False, self.errors

        # Validate each node
        for node in self.graph.nodes:
            self._validate_node(node)

        # Validate connections
        self._validate_connections()

        # Check for cycles (if we don't allow them)
        if self._has_cycles():
            self.errors.append((None, "Graph contains circular dependencies"))

        return len(self.errors) == 0, self.errors

    def _validate_node(self, node):
        """Validate a single node"""
        # Check if node type exists
        if node.type not in NODE_REGISTRY:
            self.errors.append((node.id, f"Unknown node type: {node.type}"))
            return

        # Try to instantiate the node with its data
        try:
            node_class = NODE_REGISTRY[node.type]
            node_instance = node_class(**node.data)
        except Exception as e:
            self.errors.append((node.id, f"Invalid node parameters: {str(e)}"))
            return

        # Validate required inputs are connected
        required_inputs = node_instance.get_inputs()
        if required_inputs:
            connected_inputs = self._get_connected_inputs(node.id)

            # Special case: Sequence node inputs are optional
            if node.type == "Sequence":
                # At least one animation must be connected
                anim_inputs = {i for i in connected_inputs if i.startswith('anim')}
                if not anim_inputs:
                    self.errors.append((node.id, "Sequence node needs at least one animation connected"))
            # Special case: AnimationGroup node inputs are optional
            elif node.type == "AnimationGroup":
                # At least one animation must be connected
                anim_inputs = {i for i in connected_inputs if i.startswith('anim')}
                if not anim_inputs:
                    self.errors.append((node.id, "AnimationGroup node needs at least one animation connected"))
            # Special case: Group node inputs are optional
            elif node.type == "Group":
                # At least one object must be connected
                obj_inputs = {i for i in connected_inputs if i.startswith('obj')}
                if not obj_inputs:
                    self.errors.append((node.id, "Group node needs at least one object connected"))
            # Special case: Transform node matrix input is optional
            elif node.type == "Transform":
                # Only mobject is required, matrix is optional
                if "mobject" not in connected_inputs:
                    self.errors.append((node.id, "Missing required input: mobject"))
            # Special case: ComposeMatrix inputs are optional (at least one needed)
            elif node.type == "ComposeMatrix":
                m_inputs = {i for i in connected_inputs if i.startswith('m')}
                if not m_inputs:
                    self.errors.append((node.id, "ComposeMatrix needs at least one matrix connected"))
            else:
                # Normal nodes: non-parameter inputs are required
                # Parameter inputs (param_*) are optional
                for input_name in required_inputs:
                    # Skip parameter inputs - they're optional
                    if input_name.startswith("param_"):
                        continue
                    if input_name not in connected_inputs:
                        self.errors.append((node.id, f"Missing required input: {input_name}"))

    def _validate_connections(self):
        """Validate edge connections"""
        node_ids = {node.id for node in self.graph.nodes}
        node_map = {node.id: node for node in self.graph.nodes}

        for edge in self.graph.edges:
            # Check if source and target nodes exist
            if edge.source not in node_ids:
                self.errors.append((None, f"Edge references non-existent source node: {edge.source}"))
                continue
            if edge.target not in node_ids:
                self.errors.append((None, f"Edge references non-existent target node: {edge.target}"))
                continue

            # Type compatibility checking
            source_node = node_map[edge.source]
            target_node = node_map[edge.target]

            try:
                source_class = NODE_REGISTRY.get(source_node.type)
                target_class = NODE_REGISTRY.get(target_node.type)

                if not source_class or not target_class:
                    continue

                source_instance = source_class(**source_node.data)
                target_instance = target_class(**target_node.data)

                # Get output type from source
                source_outputs = source_instance.get_outputs()
                source_handle = edge.sourceHandle or list(source_outputs.keys())[0] if source_outputs else None

                # Get input type from target
                target_inputs = target_instance.get_inputs()
                target_handle = edge.targetHandle or list(target_inputs.keys())[0] if target_inputs else None

                if source_handle and target_handle:
                    source_type = source_outputs.get(source_handle)
                    target_type = target_inputs.get(target_handle)

                    # Check type compatibility
                    if source_type and target_type and not self._types_compatible(source_type, target_type):
                        self.errors.append((
                            edge.target,
                            f"Type mismatch: {source_node.type} outputs '{source_type}' but {target_node.type}.{target_handle} expects '{target_type}'"
                        ))

            except Exception as e:
                # Skip validation if we can't instantiate nodes
                logger.warning(
                    f"Failed to validate connection between {source_node.type} and {target_node.type}: {str(e)}"
                )

    def _get_node_by_id(self, node_id: str):
        """Get node by ID"""
        for node in self.graph.nodes:
            if node.id == node_id:
                return node
        return None

    def _types_compatible(self, source_type: str, target_type: str) -> bool:
        """Check if source type can connect to target type"""
        # Exact match
        if source_type == target_type:
            return True

        # Type hierarchy for compatibility checking
        type_hierarchy = {
            "Mobject": ["Mobject", "shape", "text", "axes", "plane", "tex", "vector", "dot", "arrow"],
            "Animation": ["Animation"],
        }

        # Check if source is a subtype of target
        for base_type, subtypes in type_hierarchy.items():
            if target_type == base_type and source_type in subtypes:
                return True

        return False

    def _get_connected_inputs(self, node_id: str) -> Set[str]:
        """Get set of input port names that are connected for a node"""
        connected = set()
        for edge in self.graph.edges:
            if edge.target == node_id and edge.targetHandle:
                connected.add(edge.targetHandle)
        return connected

    def _has_cycles(self) -> bool:
        """
        Detect cycles in the graph using DFS.
        Results are cached to avoid redundant computation.

        Returns:
            True if graph contains cycles
        """
        # Return cached result if available
        if self._cycle_cache is not None:
            return self._cycle_cache

        # Build adjacency list
        adj_list: Dict[str, List[str]] = {node.id: [] for node in self.graph.nodes}
        for edge in self.graph.edges:
            adj_list[edge.source].append(edge.target)

        visited = set()
        rec_stack = set()

        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            for neighbor in adj_list.get(node_id, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False

        for node in self.graph.nodes:
            if node.id not in visited:
                if dfs(node.id):
                    self._cycle_cache = True
                    return True

        self._cycle_cache = False
        return False

    def get_execution_order(self) -> List[str]:
        """
        Get topologically sorted list of node IDs (execution order).

        Returns:
            List of node IDs in execution order

        Raises:
            ValidationError if graph has cycles
        """
        if self._has_cycles():
            raise ValidationError("Cannot determine execution order: graph has cycles")

        # Build node lookup map for O(1) access
        node_map = {node.id: node for node in self.graph.nodes}

        # Kahn's algorithm for topological sort
        in_degree: Dict[str, int] = {node.id: 0 for node in self.graph.nodes}

        # Calculate in-degrees
        for edge in self.graph.edges:
            in_degree[edge.target] = in_degree.get(edge.target, 0) + 1

        # Find all nodes with no incoming edges, sorted by order parameter
        queue_candidates = [node_id for node_id, degree in in_degree.items() if degree == 0]

        # Sort by order parameter if nodes have it (shapes have order)
        def get_node_order(node_id):
            node = node_map.get(node_id)
            if node and hasattr(node, 'data') and isinstance(node.data, dict):
                return node.data.get('order', 0)
            return 0

        # Use deque for O(1) popleft operations
        queue = deque(sorted(queue_candidates, key=get_node_order))
        result = []

        while queue:
            node_id = queue.popleft()
            result.append(node_id)

            # Collect newly available nodes
            newly_available = []
            for edge in self.graph.edges:
                if edge.source == node_id:
                    in_degree[edge.target] -= 1
                    if in_degree[edge.target] == 0:
                        newly_available.append(edge.target)

            # Sort new nodes by order and add to queue
            if newly_available:
                newly_available.sort(key=get_node_order)
                queue.extend(newly_available)

        # If not all nodes processed, there's a cycle
        if len(result) != len(self.graph.nodes):
            raise ValidationError("Graph contains cycles")

        return result
