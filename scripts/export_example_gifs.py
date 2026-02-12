"""Export all built-in examples as GIF files for the README."""

import sys
import os
import subprocess
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.examples import EXAMPLES
from backend.core.code_generator import CodeGenerator
from backend.models.graph import Graph

OUTPUT_DIR = project_root / "docs" / "examples"
TEMP_DIR = Path(tempfile.mkdtemp(prefix="manim_export_"))

# Ensure TeX is on PATH
env = os.environ.copy()
tex_bin = "/Library/TeX/texbin"
if tex_bin not in env.get("PATH", ""):
    env["PATH"] = tex_bin + ":" + env.get("PATH", "")


def export_example(example: dict) -> bool:
    """Render an example to GIF. Returns True on success."""
    example_id = example["id"]
    graph_data = example["graph"]
    print(f"\n{'='*60}")
    print(f"Exporting: {example['name']} ({example_id})")
    print(f"{'='*60}")

    # Build Graph model
    graph = Graph(**graph_data)

    # Generate manim code
    try:
        gen = CodeGenerator(graph)
        code = gen.generate()
    except Exception as e:
        print(f"  Code generation failed: {e}")
        return False

    # Write to temp file
    py_file = TEMP_DIR / f"{example_id}.py"
    py_file.write_text(code)
    print(f"  Generated: {py_file}")

    # Render with manim (low quality for speed, 480p 15fps)
    mp4_pattern = TEMP_DIR / "media" / "videos" / f"{example_id}" / "480p15"
    cmd = [
        "manim", "render",
        str(py_file), "GeneratedScene",
        "-ql", "--format=mp4",
        "--frame_rate=15",
        "--disable_caching",
    ]
    print(f"  Rendering...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(TEMP_DIR), env=env)
    if result.returncode != 0:
        print(f"  Render FAILED:\n{result.stderr[-500:]}")
        return False

    # Find the rendered MP4
    mp4_files = list(mp4_pattern.glob("*.mp4"))
    if not mp4_files:
        print(f"  No MP4 found in {mp4_pattern}")
        return False
    mp4_file = mp4_files[0]
    print(f"  Rendered: {mp4_file}")

    # Convert to GIF with ffmpeg (480px wide, optimized palette)
    gif_file = OUTPUT_DIR / f"{example_id}.gif"
    gif_cmd = [
        "ffmpeg", "-y", "-i", str(mp4_file),
        "-filter_complex",
        "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        str(gif_file),
    ]
    print(f"  Converting to GIF...")
    result = subprocess.run(gif_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  GIF conversion FAILED:\n{result.stderr[-500:]}")
        return False

    size_kb = gif_file.stat().st_size / 1024
    print(f"  Done: {gif_file} ({size_kb:.0f} KB)")
    return True


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Temp directory: {TEMP_DIR}")
    print(f"Examples to export: {len(EXAMPLES)}")

    results = {}
    for example in EXAMPLES:
        success = export_example(example)
        results[example["id"]] = success

    print(f"\n{'='*60}")
    print("Results:")
    for eid, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  {eid}: {status}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
