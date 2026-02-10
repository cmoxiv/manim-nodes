import pytest
from backend.models.graph import Graph, NodeData, EdgeData
from backend.core.graph_validator import GraphValidator, ValidationError


def test_empty_graph_validation():
    """Test that empty graph is invalid"""
    graph = Graph(id="test", name="Test", nodes=[], edges=[], settings={})
    validator = GraphValidator(graph)

    is_valid, errors = validator.validate()

    assert not is_valid
    assert len(errors) > 0


def test_single_node_validation():
    """Test that single valid node passes validation"""
    graph = Graph(
        id="test",
        name="Test",
        nodes=[
            NodeData(
                id="node-1",
                type="Circle",
                position={"x": 0, "y": 0},
                data={"radius": 1.0, "color": "#FFFFFF", "fill_opacity": 0.0, "stroke_width": 4.0}
            )
        ],
        edges=[],
        settings={}
    )
    validator = GraphValidator(graph)

    is_valid, errors = validator.validate()

    assert is_valid
    assert len(errors) == 0


def test_unknown_node_type():
    """Test that unknown node type fails validation"""
    graph = Graph(
        id="test",
        name="Test",
        nodes=[
            NodeData(
                id="node-1",
                type="InvalidNodeType",
                position={"x": 0, "y": 0},
                data={}
            )
        ],
        edges=[],
        settings={}
    )
    validator = GraphValidator(graph)

    is_valid, errors = validator.validate()

    assert not is_valid
    assert any("Unknown node type" in error[1] for error in errors)


def test_execution_order():
    """Test topological sort for execution order"""
    graph = Graph(
        id="test",
        name="Test",
        nodes=[
            NodeData(
                id="node-1",
                type="Circle",
                position={"x": 0, "y": 0},
                data={"radius": 1.0, "color": "#FFFFFF", "fill_opacity": 0.0, "stroke_width": 4.0}
            ),
            NodeData(
                id="node-2",
                type="FadeIn",
                position={"x": 200, "y": 0},
                data={"run_time": 1.0, "shift_x": 0.0, "shift_y": 0.0}
            )
        ],
        edges=[
            EdgeData(
                id="edge-1",
                source="node-1",
                target="node-2",
                targetHandle="mobject"
            )
        ],
        settings={}
    )
    validator = GraphValidator(graph)

    execution_order = validator.get_execution_order()

    # node-1 (Circle) should come before node-2 (FadeIn)
    assert execution_order.index("node-1") < execution_order.index("node-2")


def test_cycle_detection():
    """Test that cycles are detected"""
    graph = Graph(
        id="test",
        name="Test",
        nodes=[
            NodeData(id="node-1", type="Circle", position={"x": 0, "y": 0}, data={}),
            NodeData(id="node-2", type="Square", position={"x": 0, "y": 0}, data={}),
        ],
        edges=[
            EdgeData(id="edge-1", source="node-1", target="node-2"),
            EdgeData(id="edge-2", source="node-2", target="node-1"),
        ],
        settings={}
    )
    validator = GraphValidator(graph)

    assert validator._has_cycles()
