EXAMPLES = [
    {
        "id": "basic_shapes",
        "name": "Basic Shapes",
        "description": "Circle, Square, and Text with FadeIn sequence",
        "graph": {
            "id": "example-basic-shapes",
            "name": "Basic Shapes",
            "nodes": [
                {
                    "id": "node-1",
                    "type": "Circle",
                    "position": {"x": 100, "y": 100},
                    "data": {
                        "type": "Circle",
                        "radius": "1.0",
                        "color": "#58C4DD",
                        "fill_opacity": "0.5",
                        "position": "[-3, 0, 0]",
                        "present": "none",
                    },
                },
                {
                    "id": "node-2",
                    "type": "Square",
                    "position": {"x": 100, "y": 350},
                    "data": {
                        "type": "Square",
                        "side_length": "2.0",
                        "color": "#83C167",
                        "fill_opacity": "0.5",
                        "position": "[0, 0, 0]",
                        "present": "none",
                    },
                },
                {
                    "id": "node-3",
                    "type": "Text",
                    "position": {"x": 100, "y": 600},
                    "data": {
                        "type": "Text",
                        "text": "Hello Manim!",
                        "font_size": "48.0",
                        "color": "#FFFFFF",
                        "position": "[3, 0, 0]",
                        "present": "none",
                    },
                },
                {
                    "id": "node-4",
                    "type": "FadeIn",
                    "position": {"x": 450, "y": 100},
                    "data": {
                        "type": "FadeIn",
                        "run_time": "1.0",
                        "shift": "[0, 0, 0]",
                    },
                },
                {
                    "id": "node-5",
                    "type": "FadeIn",
                    "position": {"x": 450, "y": 350},
                    "data": {
                        "type": "FadeIn",
                        "run_time": "1.0",
                        "shift": "[0, 0, 0]",
                    },
                },
                {
                    "id": "node-6",
                    "type": "Write",
                    "position": {"x": 450, "y": 600},
                    "data": {
                        "type": "Write",
                        "run_time": "1.5",
                    },
                },
                {
                    "id": "node-7",
                    "type": "Sequence",
                    "position": {"x": 800, "y": 350},
                    "data": {
                        "type": "Sequence",
                        "wait_time": "0.5",
                    },
                },
            ],
            "edges": [
                {"id": "e1", "source": "node-1", "target": "node-4", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "e2", "source": "node-2", "target": "node-5", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "e3", "source": "node-3", "target": "node-6", "sourceHandle": "text", "targetHandle": "mobject"},
                {"id": "e4", "source": "node-4", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e5", "source": "node-5", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e6", "source": "node-6", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim3"},
            ],
            "settings": {},
        },
    },
    {
        "id": "pythagorean",
        "name": "Pythagorean Theorem",
        "description": "Rearrangement proof with frames & junctions for organised layout",
        "graph": {
            "id": "example-pythagorean",
            "name": "Pythagorean Theorem",
            "nodes": [
                # ═══════════════════════════════════════════════════
                # FRAMES (groupFrame nodes, zIndex=-1)
                # ═══════════════════════════════════════════════════
                {"id": "frame-setup", "type": "__groupFrame", "position": {"x": 50, "y": 0},
                 "style": {"width": 700, "height": 180}, "zIndex": -1,
                 "data": {"label": "1 - Title & Setup", "width": 700, "height": 180}},
                {"id": "frame-squares", "type": "__groupFrame", "position": {"x": 430, "y": 200},
                 "style": {"width": 600, "height": 575}, "zIndex": -1,
                 "data": {"label": "2 - Edge Squares", "width": 600, "height": 575}},
                {"id": "frame-labels", "type": "__groupFrame", "position": {"x": 430, "y": 810},
                 "style": {"width": 750, "height": 440}, "zIndex": -1,
                 "data": {"label": "3 - Side Labels", "width": 750, "height": 440}},
                {"id": "frame-c2proof", "type": "__groupFrame", "position": {"x": 430, "y": 1280},
                 "style": {"width": 750, "height": 620}, "zIndex": -1,
                 "data": {"label": "4 - c\u00b2 Proof (right)", "width": 750, "height": 620}},
                {"id": "frame-plabels", "type": "__groupFrame", "position": {"x": 430, "y": 1930},
                 "style": {"width": 750, "height": 705}, "zIndex": -1,
                 "data": {"label": "5 - Proof Labels & Equation", "width": 750, "height": 705}},
                {"id": "frame-ab2", "type": "__groupFrame", "position": {"x": 430, "y": 2665},
                 "style": {"width": 750, "height": 1270}, "zIndex": -1,
                 "data": {"label": "6 - a\u00b2+b\u00b2 Proof (left)", "width": 750, "height": 1270}},

                # ═══════════════════════════════════════════════════
                # JUNCTION NODES (fan-out triangle shape + sides)
                # ═══════════════════════════════════════════════════
                # shape junction: tri.shape → junc-shape → (create, 4 TIP-R, 4 TIP-L)
                {"id": "junc-shape", "type": "Junction", "position": {"x": 310, "y": 210},
                 "data": {"type": "Junction", "name": "junc_shape"}},
                # side_1 junction: tri.side_1 → junc-s1 → (sq-a, lbl-a)
                {"id": "junc-s1", "type": "Junction", "position": {"x": 310, "y": 260},
                 "data": {"type": "Junction", "name": "junc_s1"}},
                # side_2 junction: tri.side_2 → junc-s2 → (sq-c, lbl-c)
                {"id": "junc-s2", "type": "Junction", "position": {"x": 310, "y": 310},
                 "data": {"type": "Junction", "name": "junc_s2"}},
                # side_3 junction: tri.side_3 → junc-s3 → (sq-b, lbl-b)
                {"id": "junc-s3", "type": "Junction", "position": {"x": 310, "y": 360},
                 "data": {"type": "Junction", "name": "junc_s3"}},

                # ═══════════════════════════════════════════════════
                # FRAME 1: Title & Setup
                # ═══════════════════════════════════════════════════
                {"id": "cam-zoom", "type": "PythonCode", "position": {"x": 20, "y": 40},
                 "data": {"type": "PythonCode", "name": "cam_zoom", "code": "self.set_camera_orientation(zoom=0.75)"},
                 "parentNode": "frame-setup"},
                {"id": "title", "type": "Text", "position": {"x": 250, "y": 40},
                 "data": {"type": "Text", "name": "title", "text": "Pythagorean Theorem", "font_size": "56.0", "color": "#FFFFFF", "position": "[0, 4.5, 0]", "present": "none"},
                 "parentNode": "frame-setup"},
                {"id": "show-title", "type": "Show", "position": {"x": 490, "y": 40},
                 "data": {"type": "Show", "name": "show_title"},
                 "parentNode": "frame-setup"},

                # ═══════════════════════════════════════════════════
                # TRIANGLE (standalone - feeds many frames via junctions)
                # ═══════════════════════════════════════════════════
                {"id": "tri", "type": "RightTriangle", "position": {"x": 70, "y": 220},
                 "data": {"type": "RightTriangle", "name": "triangle", "base": "1.5", "height": "2.0", "color": "#FFFFFF", "fill_opacity": "0.08", "stroke_width": "3.0", "position": "[0, 3.0, 0]", "present": "none"}},

                # ═══════════════════════════════════════════════════
                # FRAME 2: Edge Squares
                # ═══════════════════════════════════════════════════
                {"id": "create-tri", "type": "Create", "position": {"x": 20, "y": 40},
                 "data": {"type": "Create", "name": "create_tri", "run_time": "1.5"},
                 "parentNode": "frame-squares"},
                {"id": "sq-a", "type": "SquareFromEdge", "position": {"x": 20, "y": 170},
                 "data": {"type": "SquareFromEdge", "name": "sq_a", "run_time": "1.0", "color": "#58C4DD", "fill_opacity": "0.25"},
                 "parentNode": "frame-squares"},
                {"id": "sq-c", "type": "SquareFromEdge", "position": {"x": 20, "y": 300},
                 "data": {"type": "SquareFromEdge", "name": "sq_c", "run_time": "1.0", "color": "#FC6255", "fill_opacity": "0.25"},
                 "parentNode": "frame-squares"},
                {"id": "sq-b", "type": "SquareFromEdge", "position": {"x": 20, "y": 430},
                 "data": {"type": "SquareFromEdge", "name": "sq_b", "run_time": "1.0", "color": "#83C167", "fill_opacity": "0.25"},
                 "parentNode": "frame-squares"},
                {"id": "grp-squares", "type": "AnimationGroup", "position": {"x": 300, "y": 230},
                 "data": {"type": "AnimationGroup", "name": "grp_squares", "run_time": "1.5", "lag_ratio": "0.3"},
                 "parentNode": "frame-squares"},

                # ═══════════════════════════════════════════════════
                # FRAME 3: Side Labels
                # ═══════════════════════════════════════════════════
                {"id": "lbl-a", "type": "LineLabel", "position": {"x": 20, "y": 40},
                 "data": {"type": "LineLabel", "name": "lbl_a", "text": "a", "font_size": "72.0", "color": "#58C4DD", "position": "0.5", "offset": "0.5", "present": "none"},
                 "parentNode": "frame-labels"},
                {"id": "lbl-c", "type": "LineLabel", "position": {"x": 20, "y": 170},
                 "data": {"type": "LineLabel", "name": "lbl_c", "text": "c", "font_size": "72.0", "color": "#FC6255", "position": "0.5", "offset": "0.5", "present": "none"},
                 "parentNode": "frame-labels"},
                {"id": "lbl-b", "type": "LineLabel", "position": {"x": 20, "y": 300},
                 "data": {"type": "LineLabel", "name": "lbl_b", "text": "b", "font_size": "72.0", "color": "#83C167", "position": "0.5", "offset": "0.5", "present": "none"},
                 "parentNode": "frame-labels"},
                {"id": "write-a", "type": "Write", "position": {"x": 270, "y": 40},
                 "data": {"type": "Write", "name": "write_a", "run_time": "0.8"},
                 "parentNode": "frame-labels"},
                {"id": "write-c", "type": "Write", "position": {"x": 270, "y": 170},
                 "data": {"type": "Write", "name": "write_c", "run_time": "0.8"},
                 "parentNode": "frame-labels"},
                {"id": "write-b", "type": "Write", "position": {"x": 270, "y": 300},
                 "data": {"type": "Write", "name": "write_b", "run_time": "0.8"},
                 "parentNode": "frame-labels"},
                {"id": "grp-labels", "type": "AnimationGroup", "position": {"x": 520, "y": 170},
                 "data": {"type": "AnimationGroup", "name": "grp_labels", "run_time": "1.0", "lag_ratio": "0.0"},
                 "parentNode": "frame-labels"},

                # ═══════════════════════════════════════════════════
                # FRAME 4: c² Proof (right) — arrange triangles + show frame/inner
                # ═══════════════════════════════════════════════════
                {"id": "proof-outer", "type": "Polyline", "position": {"x": 20, "y": 40},
                 "data": {"type": "Polyline", "name": "proof_frame", "points": "[[-1.75,-1.75,0],[1.75,-1.75,0],[1.75,1.75,0],[-1.75,1.75,0]]", "closed": "true", "color": "#FFFFFF", "fill_opacity": "0.0", "stroke_width": "2.0", "position": "[3.5, -1.0, 0]", "present": "none"},
                 "parentNode": "frame-c2proof"},
                {"id": "proof-inner", "type": "Polyline", "position": {"x": 20, "y": 170},
                 "data": {"type": "Polyline", "name": "proof_c2", "points": "[[-0.25,-1.75,0],[1.75,-0.25,0],[0.25,1.75,0],[-1.75,0.25,0]]", "closed": "true", "color": "#FC6255", "fill_opacity": "0.15", "stroke_width": "2.0", "position": "[3.5, -1.0, 0]", "present": "none"},
                 "parentNode": "frame-c2proof"},
                {"id": "create-frame", "type": "Create", "position": {"x": 270, "y": 40},
                 "data": {"type": "Create", "name": "create_frame", "run_time": "1.0"},
                 "parentNode": "frame-c2proof"},
                {"id": "fadein-inner", "type": "FadeIn", "position": {"x": 270, "y": 170},
                 "data": {"type": "FadeIn", "name": "fadein_inner", "run_time": "1.0", "shift": "[0, 0, 0]"},
                 "parentNode": "frame-c2proof"},
                {"id": "grp-proof", "type": "AnimationGroup", "position": {"x": 520, "y": 105},
                 "data": {"type": "AnimationGroup", "name": "grp_proof", "run_time": "1.0", "lag_ratio": "0.0"},
                 "parentNode": "frame-c2proof"},
                {"id": "tip-1", "type": "TransformInPlace", "position": {"x": 20, "y": 340},
                 "data": {"type": "TransformInPlace", "name": "tip_1", "copy": True, "angle": "0", "target": "[2.5, -1.75, 0]", "run_time": "1.5"},
                 "parentNode": "frame-c2proof"},
                {"id": "tip-2", "type": "TransformInPlace", "position": {"x": 20, "y": 470},
                 "data": {"type": "TransformInPlace", "name": "tip_2", "copy": True, "angle": "90", "target": "[4.25, -2.0, 0]", "run_time": "1.5"},
                 "parentNode": "frame-c2proof"},
                {"id": "tip-3", "type": "TransformInPlace", "position": {"x": 270, "y": 340},
                 "data": {"type": "TransformInPlace", "name": "tip_3", "copy": True, "angle": "180", "target": "[4.5, -0.25, 0]", "run_time": "1.5"},
                 "parentNode": "frame-c2proof"},
                {"id": "tip-4", "type": "TransformInPlace", "position": {"x": 270, "y": 470},
                 "data": {"type": "TransformInPlace", "name": "tip_4", "copy": True, "angle": "-90", "target": "[2.75, 0.0, 0]", "run_time": "1.5"},
                 "parentNode": "frame-c2proof"},
                {"id": "grp-arrange", "type": "AnimationGroup", "position": {"x": 520, "y": 400},
                 "data": {"type": "AnimationGroup", "name": "grp_arrange", "run_time": "1.5", "lag_ratio": "0.2"},
                 "parentNode": "frame-c2proof"},

                # ═══════════════════════════════════════════════════
                # FRAME 5: Proof Labels & Equation
                # ═══════════════════════════════════════════════════
                {"id": "plbl-a", "type": "MathTex", "position": {"x": 20, "y": 40},
                 "data": {"type": "MathTex", "name": "plbl_a", "tex": "a", "font_size": "48.0", "color": "#58C4DD", "position": "[2.5, -3.1, 0]", "present": "none"},
                 "parentNode": "frame-plabels"},
                {"id": "plbl-b", "type": "MathTex", "position": {"x": 20, "y": 170},
                 "data": {"type": "MathTex", "name": "plbl_b", "tex": "b", "font_size": "48.0", "color": "#83C167", "position": "[1.35, -1.75, 0]", "present": "none"},
                 "parentNode": "frame-plabels"},
                {"id": "plbl-c", "type": "MathTex", "position": {"x": 20, "y": 300},
                 "data": {"type": "MathTex", "name": "plbl_c", "tex": "c", "font_size": "48.0", "color": "#FC6255", "position": "[2.75, -1.5, 0]", "present": "none"},
                 "parentNode": "frame-plabels"},
                {"id": "write-pa", "type": "Write", "position": {"x": 270, "y": 40},
                 "data": {"type": "Write", "name": "write_pa", "run_time": "0.6"},
                 "parentNode": "frame-plabels"},
                {"id": "write-pb", "type": "Write", "position": {"x": 270, "y": 170},
                 "data": {"type": "Write", "name": "write_pb", "run_time": "0.6"},
                 "parentNode": "frame-plabels"},
                {"id": "write-pc", "type": "Write", "position": {"x": 270, "y": 300},
                 "data": {"type": "Write", "name": "write_pc", "run_time": "0.6"},
                 "parentNode": "frame-plabels"},
                {"id": "grp-plabels", "type": "AnimationGroup", "position": {"x": 520, "y": 170},
                 "data": {"type": "AnimationGroup", "name": "grp_plabels", "run_time": "0.8", "lag_ratio": "0.0"},
                 "parentNode": "frame-plabels"},
                {"id": "lbl-c2", "type": "MathTex", "position": {"x": 20, "y": 430},
                 "data": {"type": "MathTex", "name": "lbl_c2", "tex": "c^2", "font_size": "72.0", "color": "#FC6255", "position": "[3.5, -1.0, 0]", "present": "none"},
                 "parentNode": "frame-plabels"},
                {"id": "write-c2", "type": "Write", "position": {"x": 270, "y": 430},
                 "data": {"type": "Write", "name": "write_c2", "run_time": "0.8"},
                 "parentNode": "frame-plabels"},
                {"id": "equation", "type": "MathTex", "position": {"x": 20, "y": 560},
                 "data": {"type": "MathTex", "name": "equation", "tex": "a^2 + b^2 = c^2", "font_size": "72.0", "color": "#FFFF00", "position": "[0, -3.8, 0]", "present": "none"},
                 "parentNode": "frame-plabels"},
                {"id": "write-eq", "type": "Write", "position": {"x": 270, "y": 560},
                 "data": {"type": "Write", "name": "write_eq", "run_time": "1.5"},
                 "parentNode": "frame-plabels"},

                # ═══════════════════════════════════════════════════
                # FRAME 6: a²+b² Proof (left)
                # ═══════════════════════════════════════════════════
                # Section A: Transforms (2-column layout)
                {"id": "tip-L1", "type": "TransformInPlace", "position": {"x": 20, "y": 40},
                 "data": {"type": "TransformInPlace", "name": "tip_L1", "copy": True, "angle": "0", "target": "[-2.5, -1.75, 0]", "run_time": "1.5"},
                 "parentNode": "frame-ab2"},
                {"id": "tip-L2", "type": "TransformInPlace", "position": {"x": 250, "y": 40},
                 "data": {"type": "TransformInPlace", "name": "tip_L2", "copy": True, "angle": "180", "target": "[-2.5, -1.75, 0]", "run_time": "1.5"},
                 "parentNode": "frame-ab2"},
                {"id": "tip-L3", "type": "TransformInPlace", "position": {"x": 20, "y": 170},
                 "data": {"type": "TransformInPlace", "name": "tip_L3", "copy": True, "angle": "90", "target": "[-4.25, 0.0, 0]", "run_time": "1.5"},
                 "parentNode": "frame-ab2"},
                {"id": "tip-L4", "type": "TransformInPlace", "position": {"x": 250, "y": 170},
                 "data": {"type": "TransformInPlace", "name": "tip_L4", "copy": True, "angle": "-90", "target": "[-4.25, 0.0, 0]", "run_time": "1.5"},
                 "parentNode": "frame-ab2"},
                {"id": "grp-arrange-L", "type": "AnimationGroup", "position": {"x": 520, "y": 105},
                 "data": {"type": "AnimationGroup", "name": "grp_arrange_L", "run_time": "1.5", "lag_ratio": "0.2"},
                 "parentNode": "frame-ab2"},
                # Section B: Shapes + Proof (starts at y=340)
                {"id": "proof-outer-L", "type": "Polyline", "position": {"x": 20, "y": 340},
                 "data": {"type": "Polyline", "name": "proof_frame_L", "points": "[[-1.75,-1.75,0],[1.75,-1.75,0],[1.75,1.75,0],[-1.75,1.75,0]]", "closed": "true", "color": "#FFFFFF", "fill_opacity": "0.0", "stroke_width": "2.0", "position": "[-3.5, -1.0, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "create-frame-L", "type": "Create", "position": {"x": 250, "y": 340},
                 "data": {"type": "Create", "name": "create_frame_L", "run_time": "0.8"},
                 "parentNode": "frame-ab2"},
                {"id": "sq-a2", "type": "Polyline", "position": {"x": 20, "y": 470},
                 "data": {"type": "Polyline", "name": "sq_a2", "points": "[[-0.75,-0.75,0],[0.75,-0.75,0],[0.75,0.75,0],[-0.75,0.75,0]]", "closed": "true", "color": "#58C4DD", "fill_opacity": "0.2", "stroke_width": "2.0", "position": "[-2.5, 0.0, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "fadein-a2", "type": "FadeIn", "position": {"x": 250, "y": 470},
                 "data": {"type": "FadeIn", "name": "fadein_a2", "run_time": "0.8", "shift": "[0, 0, 0]"},
                 "parentNode": "frame-ab2"},
                {"id": "sq-b2", "type": "Polyline", "position": {"x": 20, "y": 600},
                 "data": {"type": "Polyline", "name": "sq_b2", "points": "[[-1.0,-1.0,0],[1.0,-1.0,0],[1.0,1.0,0],[-1.0,1.0,0]]", "closed": "true", "color": "#83C167", "fill_opacity": "0.2", "stroke_width": "2.0", "position": "[-4.25, -1.75, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "fadein-b2", "type": "FadeIn", "position": {"x": 250, "y": 600},
                 "data": {"type": "FadeIn", "name": "fadein_b2", "run_time": "0.8", "shift": "[0, 0, 0]"},
                 "parentNode": "frame-ab2"},
                # Section C: Labels (continues from y=730)
                {"id": "lbl-a2", "type": "MathTex", "position": {"x": 20, "y": 730},
                 "data": {"type": "MathTex", "name": "lbl_a2", "tex": "a^2", "font_size": "60.0", "color": "#58C4DD", "position": "[-2.5, 0.0, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "write-a2", "type": "Write", "position": {"x": 250, "y": 730},
                 "data": {"type": "Write", "name": "write_a2", "run_time": "0.6"},
                 "parentNode": "frame-ab2"},
                {"id": "lbl-b2", "type": "MathTex", "position": {"x": 20, "y": 860},
                 "data": {"type": "MathTex", "name": "lbl_b2", "tex": "b^2", "font_size": "60.0", "color": "#83C167", "position": "[-4.25, -1.75, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "write-b2", "type": "Write", "position": {"x": 250, "y": 860},
                 "data": {"type": "Write", "name": "write_b2", "run_time": "0.6"},
                 "parentNode": "frame-ab2"},
                {"id": "plbl-a-L", "type": "MathTex", "position": {"x": 20, "y": 990},
                 "data": {"type": "MathTex", "name": "plbl_a_L", "tex": "a", "font_size": "42.0", "color": "#58C4DD", "position": "[-3.6, 0.0, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "write-pa-L", "type": "Write", "position": {"x": 250, "y": 990},
                 "data": {"type": "Write", "name": "write_pa_L", "run_time": "0.6"},
                 "parentNode": "frame-ab2"},
                {"id": "plbl-b-L", "type": "MathTex", "position": {"x": 20, "y": 1120},
                 "data": {"type": "MathTex", "name": "plbl_b_L", "tex": "b", "font_size": "42.0", "color": "#83C167", "position": "[-4.25, -3.1, 0]", "present": "none"},
                 "parentNode": "frame-ab2"},
                {"id": "write-pb-L", "type": "Write", "position": {"x": 250, "y": 1120},
                 "data": {"type": "Write", "name": "write_pb_L", "run_time": "0.6"},
                 "parentNode": "frame-ab2"},
                {"id": "grp-proof-L", "type": "AnimationGroup", "position": {"x": 520, "y": 730},
                 "data": {"type": "AnimationGroup", "name": "grp_proof_L", "run_time": "1.2", "lag_ratio": "0.15"},
                 "parentNode": "frame-ab2"},

                # ═══════════════════════════════════════════════════
                # SEQUENCE (outside frames, collects all phase outputs)
                # ═══════════════════════════════════════════════════
                {"id": "seq", "type": "Sequence", "position": {"x": 1320, "y": 2000},
                 "data": {"type": "Sequence", "name": "sequence", "wait_time": "0.5"}},
            ],
            "edges": [
                # ── Title → Show ──
                {"id": "eT1", "source": "title", "target": "show-title", "sourceHandle": "text", "targetHandle": "mobject"},
                # ── Triangle → junctions ──
                {"id": "ej1", "source": "tri", "target": "junc-shape", "sourceHandle": "shape", "targetHandle": "in"},
                {"id": "ej2", "source": "tri", "target": "junc-s1", "sourceHandle": "side_1", "targetHandle": "in"},
                {"id": "ej3", "source": "tri", "target": "junc-s2", "sourceHandle": "side_2", "targetHandle": "in"},
                {"id": "ej4", "source": "tri", "target": "junc-s3", "sourceHandle": "side_3", "targetHandle": "in"},
                # ── shape junction → Create + 8 TransformInPlace ──
                {"id": "e1", "source": "junc-shape", "target": "create-tri", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e17", "source": "junc-shape", "target": "tip-1", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e18", "source": "junc-shape", "target": "tip-2", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e19", "source": "junc-shape", "target": "tip-3", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e20", "source": "junc-shape", "target": "tip-4", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "eL1", "source": "junc-shape", "target": "tip-L1", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "eL2", "source": "junc-shape", "target": "tip-L2", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "eL3", "source": "junc-shape", "target": "tip-L3", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "eL4", "source": "junc-shape", "target": "tip-L4", "sourceHandle": "out", "targetHandle": "mobject"},
                # ── side junctions → SquareFromEdge + LineLabel ──
                {"id": "e2", "source": "junc-s1", "target": "sq-a", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e8", "source": "junc-s1", "target": "lbl-a", "sourceHandle": "out", "targetHandle": "line"},
                {"id": "e3", "source": "junc-s2", "target": "sq-c", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e9", "source": "junc-s2", "target": "lbl-c", "sourceHandle": "out", "targetHandle": "line"},
                {"id": "e4", "source": "junc-s3", "target": "sq-b", "sourceHandle": "out", "targetHandle": "mobject"},
                {"id": "e10", "source": "junc-s3", "target": "lbl-b", "sourceHandle": "out", "targetHandle": "line"},
                # ── SquareFromEdge → AnimationGroup ──
                {"id": "e5", "source": "sq-a", "target": "grp-squares", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e6", "source": "sq-c", "target": "grp-squares", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e7", "source": "sq-b", "target": "grp-squares", "sourceHandle": "animation", "targetHandle": "anim3"},
                # ── Labels → Write → AnimationGroup ──
                {"id": "e11", "source": "lbl-a", "target": "write-a", "sourceHandle": "label", "targetHandle": "mobject"},
                {"id": "e12", "source": "lbl-c", "target": "write-c", "sourceHandle": "label", "targetHandle": "mobject"},
                {"id": "e13", "source": "lbl-b", "target": "write-b", "sourceHandle": "label", "targetHandle": "mobject"},
                {"id": "e14", "source": "write-a", "target": "grp-labels", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e15", "source": "write-c", "target": "grp-labels", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e16", "source": "write-b", "target": "grp-labels", "sourceHandle": "animation", "targetHandle": "anim3"},
                # ── TransformInPlace (right) → AnimationGroup ──
                {"id": "e21", "source": "tip-1", "target": "grp-arrange", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e22", "source": "tip-2", "target": "grp-arrange", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e23", "source": "tip-3", "target": "grp-arrange", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "e24", "source": "tip-4", "target": "grp-arrange", "sourceHandle": "animation", "targetHandle": "anim4"},
                # ── Proof frame/inner → Create/FadeIn → AnimationGroup ──
                {"id": "e25", "source": "proof-outer", "target": "create-frame", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "e26", "source": "proof-inner", "target": "fadein-inner", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "e27", "source": "create-frame", "target": "grp-proof", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e28", "source": "fadein-inner", "target": "grp-proof", "sourceHandle": "animation", "targetHandle": "anim2"},
                # ── Proof labels → Write → AnimationGroup ──
                {"id": "e29", "source": "plbl-a", "target": "write-pa", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e30", "source": "plbl-b", "target": "write-pb", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e31", "source": "plbl-c", "target": "write-pc", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e32", "source": "write-pa", "target": "grp-plabels", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e33", "source": "write-pb", "target": "grp-plabels", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e34", "source": "write-pc", "target": "grp-plabels", "sourceHandle": "animation", "targetHandle": "anim3"},
                # ── c² label + equation → Write ──
                {"id": "e35", "source": "lbl-c2", "target": "write-c2", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e36", "source": "equation", "target": "write-eq", "sourceHandle": "tex", "targetHandle": "mobject"},
                # ── TransformInPlace (left) → AnimationGroup ──
                {"id": "eL5", "source": "tip-L1", "target": "grp-arrange-L", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "eL6", "source": "tip-L2", "target": "grp-arrange-L", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "eL7", "source": "tip-L3", "target": "grp-arrange-L", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "eL8", "source": "tip-L4", "target": "grp-arrange-L", "sourceHandle": "animation", "targetHandle": "anim4"},
                # ── Left frame/squares → Create/FadeIn ──
                {"id": "eL9", "source": "proof-outer-L", "target": "create-frame-L", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "eL10", "source": "sq-a2", "target": "fadein-a2", "sourceHandle": "shape", "targetHandle": "mobject"},
                {"id": "eL11", "source": "sq-b2", "target": "fadein-b2", "sourceHandle": "shape", "targetHandle": "mobject"},
                # ── a²/b² labels + side labels → Write ──
                {"id": "eL12", "source": "lbl-a2", "target": "write-a2", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "eL13", "source": "lbl-b2", "target": "write-b2", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "eL12b", "source": "plbl-a-L", "target": "write-pa-L", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "eL12c", "source": "plbl-b-L", "target": "write-pb-L", "sourceHandle": "tex", "targetHandle": "mobject"},
                # ── Left proof → AnimationGroup ──
                {"id": "eL14", "source": "create-frame-L", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "eL15", "source": "fadein-a2", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "eL16", "source": "fadein-b2", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "eL17", "source": "write-a2", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim4"},
                {"id": "eL18", "source": "write-b2", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim5"},
                {"id": "eL19", "source": "write-pa-L", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim6"},
                {"id": "eL20", "source": "write-pb-L", "target": "grp-proof-L", "sourceHandle": "animation", "targetHandle": "anim7"},
                # ── All phases → Sequence ──
                {"id": "e40", "source": "create-tri", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e41", "source": "grp-squares", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e42", "source": "grp-labels", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "e43", "source": "grp-arrange", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim4"},
                {"id": "e44", "source": "grp-proof", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim5"},
                {"id": "e45", "source": "grp-plabels", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim6"},
                {"id": "e47", "source": "write-c2", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim7"},
                {"id": "e48", "source": "grp-arrange-L", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim8"},
                {"id": "e49", "source": "grp-proof-L", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim9"},
                {"id": "e50", "source": "write-eq", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim10"},
            ],
            "settings": {},
        },
    },
    {
        "id": "parametric2d",
        "name": "2D Parametric Curves",
        "description": "Parametric sine and cosine curves with animated dots",
        "graph": {
            "id": "example-parametric2d",
            "name": "2D Parametric Sine & Cosine Curves",
            "nodes": [
                # ═══════════════════════════════════════════════════
                # FRAMES
                # ═══════════════════════════════════════════════════
                {"id": "frame-setup", "type": "__groupFrame", "position": {"x": -500, "y": -400},
                 "style": {"width": 400, "height": 230}, "zIndex": -1,
                 "data": {"label": "1 - Camera & Grid", "width": 400, "height": 230}},
                {"id": "frame-curves", "type": "__groupFrame", "position": {"x": -500, "y": -140},
                 "style": {"width": 400, "height": 260}, "zIndex": -1,
                 "data": {"label": "2 - Parametric Curves", "width": 400, "height": 260}},
                {"id": "frame-dots", "type": "__groupFrame", "position": {"x": -500, "y": 150},
                 "style": {"width": 800, "height": 260}, "zIndex": -1,
                 "data": {"label": "3 - Dot Animations", "width": 800, "height": 260}},

                # ═══════════════════════════════════════════════════
                # FRAME 1: Camera & Grid
                # ═══════════════════════════════════════════════════
                {"id": "node-44aa6d55-7ccb-45d7-a906-b209e4d4f91e",
                 "type": "ZoomCamera", "position": {"x": 20, "y": 40},
                 "data": {"type": "ZoomCamera", "name": "zoomcamera_1", "order": 2, "scale": ".75", "run_time": ".1"},
                 "parentNode": "frame-setup"},
                {"id": "node-3fb978b1-398c-40d4-b93a-965489d9cc07",
                 "type": "NumberPlane", "position": {"x": 20, "y": 130},
                 "data": {"type": "NumberPlane", "name": "numberplane_1", "order": 1,
                          "x_range_min": "-10.0", "x_range_max": "10.0",
                          "y_range_min": "-10.0", "y_range_max": "10.0",
                          "x_step": "1.0", "y_step": "1.0", "faded_line_ratio": "4",
                          "major_line_opacity": "0.75", "minor_line_opacity": "0.1",
                          "z_index": "0", "position": "[0, 0, 0]",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-setup"},

                # ═══════════════════════════════════════════════════
                # FRAME 2: Parametric Curves
                # ═══════════════════════════════════════════════════
                {"id": "node-2",
                 "type": "ParametricFunction", "position": {"x": 20, "y": 40},
                 "data": {"type": "ParametricFunction",
                          "code": "import numpy as np\nx = t\ny = t*np.sin(2*t)\nz = 0\nreturn [x, y, z]",
                          "t_range_min": "-4", "t_range_max": "4",
                          "color": "#58C4DD", "stroke_width": "3.0",
                          "position": "[0, 0, 0]", "present": "write"},
                 "parentNode": "frame-curves"},
                {"id": "node-3",
                 "type": "ParametricFunction", "position": {"x": 20, "y": 150},
                 "data": {"type": "ParametricFunction",
                          "code": "import numpy as np\nx = t\ny = np.cos(t-np.pi) - t\nz = 0\nreturn [x, y, z]",
                          "t_range_min": "-4", "t_range_max": "4",
                          "color": "#FC6255", "stroke_width": "3.0",
                          "position": "[0, 0, 0]", "present": "write"},
                 "parentNode": "frame-curves"},

                # ═══════════════════════════════════════════════════
                # FRAME 3: Dot Animations
                # ═══════════════════════════════════════════════════
                {"id": "dot_b624a068-6095-4a84-842e-84d619bb3c3c",
                 "type": "Dot", "position": {"x": 20, "y": 40},
                 "data": {"type": "Dot", "name": "dot_1", "order": 0,
                          "position": "[0, 0, 0]", "radius": "0.08",
                          "color": "#FFFFFF", "z_index": "0",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-dots"},
                {"id": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22",
                 "type": "MoveAlongPath", "position": {"x": 280, "y": 40},
                 "data": {"type": "MoveAlongPath", "name": "movealongpath_1",
                          "copy": False, "run_time": "2.0"},
                 "parentNode": "frame-dots"},
                {"id": "dot_5e1ed778-d42b-4e9e-9a0d-3d5aa7b804dc",
                 "type": "Dot", "position": {"x": 20, "y": 150},
                 "data": {"type": "Dot", "name": "dot_2", "order": 0,
                          "position": "[0, 0, 0]", "radius": "0.08",
                          "color": "#FFFFFF", "z_index": "0",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-dots"},
                {"id": "node-c2961991-f792-40d6-8e7e-a3a94df670ec",
                 "type": "MoveAlongPath", "position": {"x": 280, "y": 150},
                 "data": {"type": "MoveAlongPath", "name": "movealongpath_1_copy",
                          "copy": False, "run_time": "2.0"},
                 "parentNode": "frame-dots"},
                {"id": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2",
                 "type": "AnimationGroup", "position": {"x": 560, "y": 90},
                 "data": {"type": "AnimationGroup", "name": "animationgroup_1",
                          "run_time": "2.0", "lag_ratio": "0.0"},
                 "parentNode": "frame-dots"},

                # ═══════════════════════════════════════════════════
                # SEQUENCE (outside frames)
                # ═══════════════════════════════════════════════════
                {"id": "node-7",
                 "type": "Sequence", "position": {"x": 450, "y": -100},
                 "data": {"type": "Sequence", "wait_time": "0.5"}},
            ],
            "edges": [
                # Dot 1 → MoveAlongPath 1 (mobject), Curve 1 → MoveAlongPath 1 (path)
                {"id": "e1", "source": "dot_b624a068-6095-4a84-842e-84d619bb3c3c", "target": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "sourceHandle": "dot", "targetHandle": "mobject"},
                {"id": "e2", "source": "node-2", "target": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "sourceHandle": "shape", "targetHandle": "path"},
                # Dot 2 → MoveAlongPath 2 (mobject), Curve 2 → MoveAlongPath 2 (path)
                {"id": "e3", "source": "dot_5e1ed778-d42b-4e9e-9a0d-3d5aa7b804dc", "target": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "sourceHandle": "dot", "targetHandle": "mobject"},
                {"id": "e4", "source": "node-3", "target": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "sourceHandle": "shape", "targetHandle": "path"},
                # MoveAlongPaths → AnimationGroup
                {"id": "e5", "source": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "target": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e6", "source": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "target": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "sourceHandle": "animation", "targetHandle": "anim10"},
                # All phases → Sequence
                {"id": "e10", "source": "node-44aa6d55-7ccb-45d7-a906-b209e4d4f91e", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e11", "source": "node-3fb978b1-398c-40d4-b93a-965489d9cc07", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e8", "source": "node-2", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim4"},
                {"id": "e9", "source": "node-3", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim7"},
                {"id": "e7", "source": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim10"},
            ],
            "settings": {},
        },
    },
    {
        "id": "parametric3d",
        "name": "3D Parametric Curves",
        "description": "3D parametric sine and cosine curves with animated dots",
        "graph": {
            "id": "example-parametric3d",
            "name": "3D Parametric Sine & Cosine Curves",
            "nodes": [
                # ═══════════════════════════════════════════════════
                # FRAMES
                # ═══════════════════════════════════════════════════
                {"id": "frame-setup", "type": "__groupFrame", "position": {"x": -500, "y": -400},
                 "style": {"width": 500, "height": 400}, "zIndex": -1,
                 "data": {"label": "1 - Camera & Scene", "width": 500, "height": 400}},
                {"id": "frame-curves", "type": "__groupFrame", "position": {"x": -500, "y": 30},
                 "style": {"width": 400, "height": 260}, "zIndex": -1,
                 "data": {"label": "2 - Parametric Curves", "width": 400, "height": 260}},
                {"id": "frame-dots", "type": "__groupFrame", "position": {"x": -500, "y": 320},
                 "style": {"width": 800, "height": 260}, "zIndex": -1,
                 "data": {"label": "3 - Dot Animations", "width": 800, "height": 260}},

                # ═══════════════════════════════════════════════════
                # FRAME 1: Camera & Scene
                # ═══════════════════════════════════════════════════
                {"id": "node-44aa6d55-7ccb-45d7-a906-b209e4d4f91e",
                 "type": "ZoomCamera", "position": {"x": 20, "y": 40},
                 "data": {"type": "ZoomCamera", "name": "zoomcamera_1", "order": 2, "scale": "1.25", "run_time": ".1"},
                 "parentNode": "frame-setup"},
                {"id": "node-c8b2e4bb-fad6-436f-bdb6-67f438385997",
                 "type": "Axes3D", "position": {"x": 20, "y": 100},
                 "data": {"type": "Axes3D", "name": "axes3d_1", "order": 3,
                          "x_range": "[-5, 5, 1]", "y_range": "[-5, 5, 1]", "z_range": "[-5, 5, 1]",
                          "x_length": "10.0", "y_length": "10.0", "z_length": "6.0",
                          "position": "[0, 0, 0]", "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-setup"},
                {"id": "node-7a6760c3-02f2-4d28-9f83-a60a0466b65e",
                 "type": "NumberPlane", "position": {"x": 200, "y": 100},
                 "data": {"type": "NumberPlane", "name": "numberplane_1", "order": 5,
                          "x_range_min": "-10.0", "x_range_max": "10.0",
                          "y_range_min": "-10.0", "y_range_max": "10.0",
                          "x_step": "1.0", "y_step": "1.0", "faded_line_ratio": "4",
                          "major_line_opacity": "0.3", "minor_line_opacity": "0.1",
                          "z_index": "0", "position": "[0, 0, 0]",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-setup"},
                {"id": "node-18d5eb08-6440-44a4-9c8c-888b1f1c22b2",
                 "type": "SetCameraOrientation", "position": {"x": 200, "y": 200},
                 "data": {"type": "SetCameraOrientation", "name": "setcameraorientation_1", "order": 4,
                          "phi": "75.0", "theta": "-45.0", "gamma": "0.0", "run_time": "1.0"},
                 "parentNode": "frame-setup"},

                # ═══════════════════════════════════════════════════
                # FRAME 2: Parametric Curves
                # ═══════════════════════════════════════════════════
                {"id": "node-2",
                 "type": "ParametricFunction", "position": {"x": 20, "y": 40},
                 "data": {"type": "ParametricFunction",
                          "code": "import numpy as np\nx = t\ny = t*np.sin(2*t)\nz = np.cos(t)\nreturn [x, y, z]",
                          "t_range_min": "-4", "t_range_max": "4",
                          "color": "#58C4DD", "stroke_width": "5.0",
                          "position": "[0, 0, 0]", "present": "write"},
                 "parentNode": "frame-curves"},
                {"id": "node-3",
                 "type": "ParametricFunction", "position": {"x": 20, "y": 150},
                 "data": {"type": "ParametricFunction",
                          "code": "import numpy as np\nx = t\ny = np.cos(t-np.pi) - t\nz = t\nreturn [x, y, z]",
                          "t_range_min": "-4", "t_range_max": "4",
                          "color": "#FC6255", "stroke_width": "5.0",
                          "position": "[0, 0, 0]", "present": "write"},
                 "parentNode": "frame-curves"},

                # ═══════════════════════════════════════════════════
                # FRAME 3: Dot Animations
                # ═══════════════════════════════════════════════════
                {"id": "dot_b624a068-6095-4a84-842e-84d619bb3c3c",
                 "type": "Dot", "position": {"x": 20, "y": 40},
                 "data": {"type": "Dot", "name": "dot_1", "order": 0,
                          "position": "[0, 0, 0]", "radius": "0.08",
                          "color": "#FFFFFF", "z_index": "0",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-dots"},
                {"id": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22",
                 "type": "MoveAlongPath", "position": {"x": 280, "y": 40},
                 "data": {"type": "MoveAlongPath", "name": "movealongpath_1",
                          "copy": False, "run_time": "4.0"},
                 "parentNode": "frame-dots"},
                {"id": "dot_5e1ed778-d42b-4e9e-9a0d-3d5aa7b804dc",
                 "type": "Dot", "position": {"x": 20, "y": 150},
                 "data": {"type": "Dot", "name": "dot_2", "order": 0,
                          "position": "[0, 0, 0]", "radius": "0.08",
                          "color": "#FFFFFF", "z_index": "0",
                          "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-dots"},
                {"id": "node-c2961991-f792-40d6-8e7e-a3a94df670ec",
                 "type": "MoveAlongPath", "position": {"x": 280, "y": 150},
                 "data": {"type": "MoveAlongPath", "name": "movealongpath_1_copy",
                          "copy": False, "run_time": "4.0"},
                 "parentNode": "frame-dots"},
                {"id": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2",
                 "type": "AnimationGroup", "position": {"x": 560, "y": 90},
                 "data": {"type": "AnimationGroup", "name": "animationgroup_1",
                          "run_time": "4.0", "lag_ratio": "0.0"},
                 "parentNode": "frame-dots"},

                # ═══════════════════════════════════════════════════
                # SEQUENCE (outside frames)
                # ═══════════════════════════════════════════════════
                {"id": "node-7",
                 "type": "Sequence", "position": {"x": 450, "y": -100},
                 "data": {"type": "Sequence", "wait_time": "0.5"}},
            ],
            "edges": [
                # Dot 1 → MoveAlongPath 1 (mobject), Curve 1 → MoveAlongPath 1 (path)
                {"id": "e1", "source": "dot_b624a068-6095-4a84-842e-84d619bb3c3c", "target": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "sourceHandle": "dot", "targetHandle": "mobject"},
                {"id": "e2", "source": "node-2", "target": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "sourceHandle": "shape", "targetHandle": "path"},
                # Dot 2 → MoveAlongPath 2 (mobject), Curve 2 → MoveAlongPath 2 (path)
                {"id": "e3", "source": "dot_5e1ed778-d42b-4e9e-9a0d-3d5aa7b804dc", "target": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "sourceHandle": "dot", "targetHandle": "mobject"},
                {"id": "e4", "source": "node-3", "target": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "sourceHandle": "shape", "targetHandle": "path"},
                # MoveAlongPaths → AnimationGroup
                {"id": "e5", "source": "movealongpath_5ce72188-7821-41e4-9358-dda946b2ff22", "target": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e6", "source": "node-c2961991-f792-40d6-8e7e-a3a94df670ec", "target": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "sourceHandle": "animation", "targetHandle": "anim10"},
                # All phases → Sequence
                {"id": "e10", "source": "node-44aa6d55-7ccb-45d7-a906-b209e4d4f91e", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e11", "source": "node-c8b2e4bb-fad6-436f-bdb6-67f438385997", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e12", "source": "node-7a6760c3-02f2-4d28-9f83-a60a0466b65e", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "e13", "source": "node-18d5eb08-6440-44a4-9c8c-888b1f1c22b2", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim4"},
                {"id": "e8", "source": "node-2", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim6"},
                {"id": "e9", "source": "node-3", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim7"},
                {"id": "e7", "source": "animationgroup_ac9793cd-1ffa-409f-ad83-3cd4bf0cf1a2", "target": "node-7", "sourceHandle": "animation", "targetHandle": "anim10"},
            ],
            "settings": {},
        },
    },
    {
        "id": "lorenz",
        "name": "Lorenz Attractor",
        "description": "3D live plotting of the Lorenz strange attractor",
        "graph": {
            "id": "example-lorenz",
            "name": "Lorenz Attractor",
            "nodes": [
                # ═══════════════════════════════════════════════════
                # FRAMES
                # ═══════════════════════════════════════════════════
                {"id": "frame-setup", "type": "__groupFrame", "position": {"x": -390, "y": -255},
                 "style": {"width": 465, "height": 270}, "zIndex": -1,
                 "data": {"label": "1 - Camera & Scene", "width": 465, "height": 270}},
                {"id": "frame-curve", "type": "__groupFrame", "position": {"x": -390, "y": 45},
                 "style": {"width": 405, "height": 165}, "zIndex": -1,
                 "data": {"label": "2 - Lorenz Attractor", "width": 405, "height": 165}},
                # ═══════════════════════════════════════════════════
                # FRAME 1: Camera & Scene
                # ═══════════════════════════════════════════════════
                {"id": "zoom", "type": "ZoomCamera", "position": {"x": 15, "y": 45},
                 "data": {"type": "ZoomCamera", "name": "zoom", "order": 1, "scale": "1.0", "run_time": ".1"},
                 "parentNode": "frame-setup"},
                {"id": "axes", "type": "Axes3D", "position": {"x": 15, "y": 150},
                 "data": {"type": "Axes3D", "name": "axes", "order": 2,
                          "x_range": "[-4, 4, 2]", "y_range": "[-4, 4, 2]", "z_range": "[-4, 4, 2]",
                          "x_length": "8.0", "y_length": "8.0", "z_length": "8.0",
                          "position": "[0, 0, 0]", "present": "create", "present_run_time": "1.0"},
                 "parentNode": "frame-setup"},
                {"id": "cam", "type": "SetCameraOrientation", "position": {"x": 240, "y": 45},
                 "data": {"type": "SetCameraOrientation", "name": "cam", "order": 3,
                          "phi": "75.0", "theta": "-45.0", "gamma": "0.0", "run_time": "0"},
                 "parentNode": "frame-setup"},
                {"id": "cam2", "type": "SetCameraOrientation", "position": {"x": 240, "y": 145},
                 "data": {"type": "SetCameraOrientation", "name": "cam_copy", "order": 3,
                          "phi": "75.0", "theta": "135", "gamma": "0.0", "run_time": "3"},
                 "parentNode": "frame-setup"},

                # ═══════════════════════════════════════════════════
                # FRAME 2: Lorenz Attractor
                # ═══════════════════════════════════════════════════
                {"id": "lorenz", "type": "ParametricFunction", "position": {"x": 15, "y": 45},
                 "data": {"type": "ParametricFunction", "name": "lorenz",
                          "code": "import numpy as np\n_k = '_lorenz'\nif not hasattr(np, _k):\n    s, r, b = 10, 28, 8/3\n    dt, N = 0.005, 5000\n    p = np.empty((N, 3))\n    x, y, z = 1.0, 1.0, 1.0\n    for i in range(N):\n        p[i] = [x, y, z]\n        dx = s*(y-x)*dt\n        dy = (x*(r-z)-y)*dt\n        dz = (x*y-b*z)*dt\n        x, y, z = x+dx, y+dy, z+dz\n    setattr(np, _k, p)\np = getattr(np, _k)\nsc = 0.12\nidx = int(t/25*(len(p)-1))\nidx = max(0, min(idx, len(p)-1))\nv = p[idx]\nreturn [v[0]*sc, v[1]*sc, (v[2]-25)*sc]",
                          "t_range_min": "0", "t_range_max": "25",
                          "color": "#58C4DD", "stroke_width": "2.0",
                          "position": "[0, 0, 0]", "present": "write", "present_run_time": "6.0"},
                 "parentNode": "frame-curve"},

                # ═══════════════════════════════════════════════════
                # SEQUENCE (outside frames)
                # ═══════════════════════════════════════════════════
                {"id": "seq", "type": "Sequence", "position": {"x": 250, "y": -50},
                 "data": {"type": "Sequence", "name": "sequence", "wait_time": "0.5"}},
            ],
            "edges": [
                # All phases → Sequence
                {"id": "e3", "source": "zoom", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e4", "source": "cam", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e5", "source": "axes", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "e6", "source": "lorenz", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim5"},
                {"id": "e9", "source": "cam2", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim10"},
            ],
            "settings": {},
        },
    },
    {
        "id": "sqrt2",
        "name": "√2 Construction",
        "description": "Euclidean construction of √2 as the diagonal of a unit square",
        "graph": {
            "id": "example-sqrt2",
            "name": "√2 Construction",
            "nodes": [
                # ── Title ──
                {"id": "title", "type": "MathTex", "position": {"x": 100, "y": 50},
                 "data": {"type": "MathTex", "name": "title", "tex": "\\text{Construction of }\\sqrt{2}", "font_size": "56.0", "color": "#FFFFFF", "position": "[0, 3.5, 0]", "present": "none"}},
                {"id": "write-title", "type": "Write", "position": {"x": 400, "y": 50},
                 "data": {"type": "Write", "name": "write_title", "run_time": "1.0"}},

                # ── Unit square ──
                {"id": "square", "type": "Square", "position": {"x": 100, "y": 200},
                 "data": {"type": "Square", "name": "unit_square", "side_length": "3.0", "color": "#58C4DD", "fill_opacity": "0.08", "stroke_width": "3.0", "position": "[0, 0.5, 0]", "present": "none"}},
                {"id": "create-sq", "type": "Create", "position": {"x": 400, "y": 200},
                 "data": {"type": "Create", "name": "create_sq", "run_time": "1.5"}},

                # ── Side labels "1" ──
                {"id": "lbl-bot", "type": "MathTex", "position": {"x": 100, "y": 400},
                 "data": {"type": "MathTex", "name": "lbl_bot", "tex": "1", "font_size": "56.0", "color": "#58C4DD", "position": "[0, -1.5, 0]", "present": "none"}},
                {"id": "lbl-right", "type": "MathTex", "position": {"x": 100, "y": 530},
                 "data": {"type": "MathTex", "name": "lbl_right", "tex": "1", "font_size": "56.0", "color": "#58C4DD", "position": "[2.0, 0.5, 0]", "present": "none"}},
                {"id": "write-bot", "type": "Write", "position": {"x": 350, "y": 400},
                 "data": {"type": "Write", "name": "write_bot", "run_time": "0.6"}},
                {"id": "write-right", "type": "Write", "position": {"x": 350, "y": 530},
                 "data": {"type": "Write", "name": "write_right", "run_time": "0.6"}},
                {"id": "grp-labels", "type": "AnimationGroup", "position": {"x": 600, "y": 460},
                 "data": {"type": "AnimationGroup", "name": "grp_labels", "run_time": "0.8", "lag_ratio": "0.0"}},

                # ── Diagonal ──
                {"id": "diag", "type": "Line", "position": {"x": 100, "y": 680},
                 "data": {"type": "Line", "name": "diagonal", "start": "[-1.5, -1.0, 0]", "end": "[1.5, 2.0, 0]", "color": "#FFFF00", "stroke_width": "4.0", "present": "none"}},
                {"id": "create-diag", "type": "Create", "position": {"x": 400, "y": 680},
                 "data": {"type": "Create", "name": "create_diag", "run_time": "1.0"}},

                # ── √2 label ──
                {"id": "lbl-diag", "type": "MathTex", "position": {"x": 100, "y": 830},
                 "data": {"type": "MathTex", "name": "lbl_diag", "tex": "\\sqrt{2}", "font_size": "56.0", "color": "#FFFF00", "position": "[-0.4, 0.9, 0]", "present": "none"}},
                {"id": "write-diag", "type": "Write", "position": {"x": 400, "y": 830},
                 "data": {"type": "Write", "name": "write_diag", "run_time": "0.8"}},

                # ── Right angle marker at bottom-left corner ──
                {"id": "angle", "type": "Polyline", "position": {"x": 100, "y": 980},
                 "data": {"type": "Polyline", "name": "angle_mark", "points": "[[-0.2, 0.2, 0], [0.2, 0.2, 0], [0.2, -0.2, 0]]", "closed": "false", "color": "#FFFFFF", "stroke_width": "2.0", "fill_opacity": "0.0", "position": "[-1.3, -0.8, 0]", "present": "none"}},
                {"id": "fadein-angle", "type": "FadeIn", "position": {"x": 400, "y": 980},
                 "data": {"type": "FadeIn", "name": "fadein_angle", "run_time": "0.5", "shift": "[0, 0, 0]"}},

                # ── Pythagorean equation ──
                {"id": "equation", "type": "MathTex", "position": {"x": 100, "y": 1130},
                 "data": {"type": "MathTex", "name": "equation", "tex": "1^2 + 1^2 = (\\sqrt{2})^2", "font_size": "56.0", "color": "#FFFFFF", "position": "[0, -2.5, 0]", "present": "none"}},
                {"id": "write-eq", "type": "Write", "position": {"x": 400, "y": 1130},
                 "data": {"type": "Write", "name": "write_eq", "run_time": "1.5"}},

                # ── Decimal approximation ──
                {"id": "approx", "type": "MathTex", "position": {"x": 100, "y": 1280},
                 "data": {"type": "MathTex", "name": "approx", "tex": "\\sqrt{2} \\approx 1.41421\\ldots", "font_size": "48.0", "color": "#83C167", "position": "[0, -3.5, 0]", "present": "none"}},
                {"id": "write-approx", "type": "Write", "position": {"x": 400, "y": 1280},
                 "data": {"type": "Write", "name": "write_approx", "run_time": "1.0"}},

                # ── Sequence ──
                {"id": "seq", "type": "Sequence", "position": {"x": 850, "y": 680},
                 "data": {"type": "Sequence", "name": "sequence", "wait_time": "0.5"}},
            ],
            "edges": [
                # Title → Write
                {"id": "e1", "source": "title", "target": "write-title", "sourceHandle": "tex", "targetHandle": "mobject"},
                # Square → Create
                {"id": "e2", "source": "square", "target": "create-sq", "sourceHandle": "shape", "targetHandle": "mobject"},
                # Side labels → Write → AnimationGroup
                {"id": "e3", "source": "lbl-bot", "target": "write-bot", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e4", "source": "lbl-right", "target": "write-right", "sourceHandle": "tex", "targetHandle": "mobject"},
                {"id": "e5", "source": "write-bot", "target": "grp-labels", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e6", "source": "write-right", "target": "grp-labels", "sourceHandle": "animation", "targetHandle": "anim2"},
                # Diagonal → Create
                {"id": "e7", "source": "diag", "target": "create-diag", "sourceHandle": "shape", "targetHandle": "mobject"},
                # √2 label → Write
                {"id": "e8", "source": "lbl-diag", "target": "write-diag", "sourceHandle": "tex", "targetHandle": "mobject"},
                # Angle marker → FadeIn
                {"id": "e9", "source": "angle", "target": "fadein-angle", "sourceHandle": "shape", "targetHandle": "mobject"},
                # Equation → Write
                {"id": "e10", "source": "equation", "target": "write-eq", "sourceHandle": "tex", "targetHandle": "mobject"},
                # Approximation → Write
                {"id": "e11", "source": "approx", "target": "write-approx", "sourceHandle": "tex", "targetHandle": "mobject"},
                # All phases → Sequence
                {"id": "e12", "source": "write-title", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim1"},
                {"id": "e13", "source": "create-sq", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim2"},
                {"id": "e14", "source": "grp-labels", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim3"},
                {"id": "e15", "source": "create-diag", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim4"},
                {"id": "e16", "source": "write-diag", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim5"},
                {"id": "e17", "source": "fadein-angle", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim6"},
                {"id": "e18", "source": "write-eq", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim7"},
                {"id": "e19", "source": "write-approx", "target": "seq", "sourceHandle": "animation", "targetHandle": "anim8"},
            ],
            "settings": {},
        },
    },
]


def get_example_list():
    return [{"id": e["id"], "name": e["name"], "description": e["description"]} for e in EXAMPLES]


def get_example_by_id(example_id: str):
    for e in EXAMPLES:
        if e["id"] == example_id:
            return e
    return None
