"""Build the notebook from the editable percent-cell Python source.

Run with --execute to verify it in a fresh kernel and export a readable HTML copy.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import nbformat

HERE = Path(__file__).resolve().parent


def make_notebook():
    cells = []
    kind, lines = None, []

    def flush():
        if kind is None:
            return
        source = "\n".join(lines).strip()
        factory = nbformat.v4.new_markdown_cell if kind == "markdown" else nbformat.v4.new_code_cell
        cell = factory(source)
        cell["id"] = hashlib.sha256(f"{len(cells)}:{source}".encode()).hexdigest()[:12]
        cells.append(cell)

    for line in (HERE / "lesson.py").read_text().splitlines():
        if line.startswith("# %%"):
            flush()
            kind = "markdown" if "[markdown]" in line else "code"
            lines = []
        elif kind == "markdown":
            lines.append(line[2:] if line.startswith("# ") else "" if line == "#" else line)
        else:
            lines.append(line)
    flush()
    notebook = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    })
    nbformat.validate(notebook)
    return notebook


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    notebook = make_notebook()
    if args.execute:
        from jupyter_client import KernelManager
        from jupyter_client.kernelspec import KernelSpecManager
        from nbclient import NotebookClient
        from nbconvert import HTMLExporter

        # Private temporary configuration; do not install or change a user's global kernel.
        with tempfile.TemporaryDirectory(prefix="episode01-kernel-") as temporary:
            runtime = Path(temporary)
            kernel = runtime / "kernels" / "python3"
            kernel.mkdir(parents=True)
            (kernel / "kernel.json").write_text(json.dumps({
                "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                "display_name": "Episode 01 verification", "language": "python",
            }))
            manager = KernelManager(kernel_name="python3",
                                    kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel.parent)]))
            environment = os.environ.copy()
            environment.update({"MPLCONFIGDIR": str(runtime / "matplotlib"),
                                "IPYTHONDIR": str(runtime / "ipython"),
                                "JUPYTER_RUNTIME_DIR": str(runtime / "jupyter")})
            # Prepare fonts before recording notebook output.
            subprocess.run([sys.executable, "-c", "import matplotlib.font_manager"],
                           env=environment, check=True, capture_output=True)
            # Save release evidence without restoring the removed reporting cell
            # to the presentation notebook.
            notebook.cells.append(nbformat.v4.new_code_cell(
                "from release_report import save_report\nsave_report(globals())"
            ))
            client = NotebookClient(notebook, km=manager, timeout=120,
                                    resources={"metadata": {"path": str(HERE)}})
            client.execute(env=environment, cleanup_kc=True)
            notebook.cells.pop()
        html, _ = HTMLExporter().from_notebook_node(notebook)
        (HERE / "episode_01.html").write_text(html)
    nbformat.write(notebook, HERE / "episode_01.ipynb")
    print(f"Built {len(notebook.cells)} cells ({sum(c.cell_type == 'code' for c in notebook.cells)} code cells).")
    print("Fresh-kernel execution and HTML export passed." if args.execute else "Outputs cleared; use --execute to regenerate them.")


if __name__ == "__main__":
    main()
