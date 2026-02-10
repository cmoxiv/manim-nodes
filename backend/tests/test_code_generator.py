import pytest
from backend.models.graph import Graph, NodeData, EdgeData
from backend.core.code_generator import CodeGenerator


def test_simple_circle_generation():
    """Test code generation for a simple circle"""
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

    generator = CodeGenerator(graph)
    code = generator.generate()

    assert "from manim import *" in code
    assert "class GeneratedScene(Scene):" in code
    assert "def construct(self):" in code
    assert "Circle(radius=1.0" in code
    assert "self.add(" in code


def test_circle_fadein_generation():
    """Test code generation for circle with fade in animation"""
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

    generator = CodeGenerator(graph)
    code = generator.generate()

    # Check that circle is created first
    assert code.index("Circle") < code.index("FadeIn")

    # Check that FadeIn references the circle variable
    assert "FadeIn(circle" in code

    # Check that animation is played
    assert "self.play(" in code


def test_invalid_graph_fails():
    """Test that invalid graph raises ValidationError"""
    graph = Graph(
        id="test",
        name="Test",
        nodes=[
            NodeData(
                id="node-1",
                type="InvalidType",
                position={"x": 0, "y": 0},
                data={}
            )
        ],
        edges=[],
        settings={}
    )

    generator = CodeGenerator(graph)

    with pytest.raises(Exception):
        generator.generate()
