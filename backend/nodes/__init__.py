from .base import NodeBase
from .shapes import CircleNode, SquareNode, RectangleNode, LineNode, TextNode, ArrowNode, TriangleNode, RegularPolygonNode, RightTriangleNode, IsoscelesTriangleNode
from .animations import (
    FadeInNode, FadeOutNode, ShowNode, WriteNode, CreateNode,
    MorphNode, RotateNode, ScaleNode, MoveToNode, SequenceNode, AnimationGroupNode,
    # Creation
    UncreateNode, UnwriteNode, DrawBorderThenFillNode, SpiralInNode,
    # Growing
    GrowFromCenterNode, GrowFromPointNode, GrowFromEdgeNode, GrowArrowNode, SpinInFromNothingNode,
    # Indication
    IndicateNode, FlashNode, CircumscribeNode, WiggleNode, ApplyWaveNode, FocusOnNode,
    # Movement
    MoveAlongPathNode,
    # Transform
    ReplacementTransformNode, TransformFromCopyNode, FadeTransformNode,
    TransformMatchingShapesNode, TransformMatchingTexNode, FadeToColorNode, ShrinkToCenterNode,
    # Other
    BroadcastNode,
)
from .math import AxesNode, NumberPlaneNode, MathTexNode, VectorNode, DotNode, LinePlotNode, PolylineNode, DisplayMatrixNode
from .utilities import GroupNode, TextCharacterNode, TransformNode
from .shapes3d import SphereNode, CubeNode, ConeNode, CylinderNode, TorusNode, Axes3DNode
from .camera import (
    SetCameraOrientationNode, MoveCameraNode, ZoomCameraNode,
)
from .math_ops import (
    AddNode, SubtractNode, MultiplyNode, DivideNode, NumberNode, Vec3Node,
    Vec3SplitNode, Vec3CombineNode,
    MatrixNode, MatrixMultiplyNode, MatrixScaleNode, ColorNode
)

# Registry of all available node types
NODE_REGISTRY = {
    # Shapes
    "Circle": CircleNode,
    "Square": SquareNode,
    "Rectangle": RectangleNode,
    "Line": LineNode,
    "Text": TextNode,
    "Arrow": ArrowNode,
    "Triangle": TriangleNode,
    "RegularPolygon": RegularPolygonNode,
    "RightTriangle": RightTriangleNode,
    "IsoscelesTriangle": IsoscelesTriangleNode,
    "FadeIn": FadeInNode,
    "FadeOut": FadeOutNode,
    "Show": ShowNode,
    "Write": WriteNode,
    "Create": CreateNode,
    "Morph": MorphNode,
    "Rotate": RotateNode,
    "Scale": ScaleNode,
    "MoveTo": MoveToNode,
    "Sequence": SequenceNode,
    "AnimationGroup": AnimationGroupNode,
    # Creation animations
    "Uncreate": UncreateNode,
    "Unwrite": UnwriteNode,
    "DrawBorderThenFill": DrawBorderThenFillNode,
    "SpiralIn": SpiralInNode,
    # Growing animations
    "GrowFromCenter": GrowFromCenterNode,
    "GrowFromPoint": GrowFromPointNode,
    "GrowFromEdge": GrowFromEdgeNode,
    "GrowArrow": GrowArrowNode,
    "SpinInFromNothing": SpinInFromNothingNode,
    # Indication animations
    "Indicate": IndicateNode,
    "Flash": FlashNode,
    "Circumscribe": CircumscribeNode,
    "Wiggle": WiggleNode,
    "ApplyWave": ApplyWaveNode,
    "FocusOn": FocusOnNode,
    # Movement animations
    "MoveAlongPath": MoveAlongPathNode,
    # Transform animations
    "ReplacementTransform": ReplacementTransformNode,
    "TransformFromCopy": TransformFromCopyNode,
    "FadeTransform": FadeTransformNode,
    "TransformMatchingShapes": TransformMatchingShapesNode,
    "TransformMatchingTex": TransformMatchingTexNode,
    "FadeToColor": FadeToColorNode,
    "ShrinkToCenter": ShrinkToCenterNode,
    # Other animations
    "Broadcast": BroadcastNode,
    "Axes": AxesNode,
    "NumberPlane": NumberPlaneNode,
    "MathTex": MathTexNode,
    "Vector": VectorNode,
    "Dot": DotNode,
    "DisplayMatrix": DisplayMatrixNode,
    "LinePlot": LinePlotNode,
    "Polyline": PolylineNode,
    # Utilities
    "Group": GroupNode,
    "TextCharacter": TextCharacterNode,
    "Transform": TransformNode,
    # 3D Shapes
    "Sphere": SphereNode,
    "Cube": CubeNode,
    "Cone": ConeNode,
    "Cylinder": CylinderNode,
    "Torus": TorusNode,
    "Axes3D": Axes3DNode,
    # Camera
    "SetCameraOrientation": SetCameraOrientationNode,
    "MoveCamera": MoveCameraNode,
    "ZoomCamera": ZoomCameraNode,
    # Math Operations
    "Add": AddNode,
    "Subtract": SubtractNode,
    "Multiply": MultiplyNode,
    "Divide": DivideNode,
    "Number": NumberNode,
    "Vec3": Vec3Node,
    "Vec3Split": Vec3SplitNode,
    "Vec3Combine": Vec3CombineNode,
    "Matrix": MatrixNode,
    "MatrixMultiply": MatrixMultiplyNode,
    "MatrixScale": MatrixScaleNode,
    "Color": ColorNode,
}

__all__ = [
    "NodeBase",
    "NODE_REGISTRY",
    # Shapes
    "CircleNode",
    "SquareNode",
    "RectangleNode",
    "LineNode",
    "TextNode",
    "ArrowNode",
    "TriangleNode",
    "RegularPolygonNode",
    "RightTriangleNode",
    "IsoscelesTriangleNode",
    "FadeInNode",
    "FadeOutNode",
    "ShowNode",
    "WriteNode",
    "CreateNode",
    "MorphNode",
    "RotateNode",
    "ScaleNode",
    "MoveToNode",
    "SequenceNode",
    "AnimationGroupNode",
    # Creation animations
    "UncreateNode",
    "UnwriteNode",
    "DrawBorderThenFillNode",
    "SpiralInNode",
    # Growing animations
    "GrowFromCenterNode",
    "GrowFromPointNode",
    "GrowFromEdgeNode",
    "GrowArrowNode",
    "SpinInFromNothingNode",
    # Indication animations
    "IndicateNode",
    "FlashNode",
    "CircumscribeNode",
    "WiggleNode",
    "ApplyWaveNode",
    "FocusOnNode",
    # Movement animations
    "MoveAlongPathNode",
    # Transform animations
    "ReplacementTransformNode",
    "TransformFromCopyNode",
    "FadeTransformNode",
    "TransformMatchingShapesNode",
    "TransformMatchingTexNode",
    "FadeToColorNode",
    "ShrinkToCenterNode",
    # Other animations
    "BroadcastNode",
    "AxesNode",
    "NumberPlaneNode",
    "MathTexNode",
    "VectorNode",
    "DotNode",
    "DisplayMatrixNode",
    "LinePlotNode",
    "PolylineNode",
    # Utilities
    "GroupNode",
    "TextCharacterNode",
    "TransformNode",
    # 3D Shapes
    "SphereNode",
    "CubeNode",
    "ConeNode",
    "CylinderNode",
    "TorusNode",
    "Axes3DNode",
    # Camera
    "SetCameraOrientationNode",
    "MoveCameraNode",
    "ZoomCameraNode",
    # Math Operations
    "AddNode",
    "SubtractNode",
    "MultiplyNode",
    "DivideNode",
    "NumberNode",
    "Vec3Node",
    "Vec3SplitNode",
    "Vec3CombineNode",
    "MatrixNode",
    "MatrixMultiplyNode",
    "MatrixScaleNode",
    "ColorNode",
]
