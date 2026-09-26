"""Run the same plotting code under two different eunoia versions.

eunoia ships a compiled extension, so two versions cannot be imported into one
process. Each version is pip-installed once into `.eunoia_versions/<version>/`
and then used by running the code in a subprocess with that directory first on
PYTHONPATH. The installs are cached, so only the first call is slow.

    from eunoia_versions import run
    print(run("0.5.0", "import eunoia; print(eunoia.__version__)"))
"""
import os
import subprocess
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".eunoia_versions"


def ensure(version):
    "pip-install eunoia==`version` into a private directory (cached); returns the path."
    target = CACHE / version
    if not list(target.glob("eunoia*")):
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--target", str(target),
                        f"eunoia=={version}"], check=True)
    return target


def run(version, code, timeout=900):
    "Execute `code` in a subprocess where `import eunoia` gives `version`; returns its stdout."
    env = dict(os.environ, PYTHONPATH=str(ensure(version)), MPLBACKEND="Agg")
    env.pop("PYTHONHOME", None)
    proc = subprocess.run([sys.executable, "-c", textwrap.dedent(code)], cwd=str(HERE),
                          env=env, capture_output=True, text=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError(f"eunoia {version} failed:\n{proc.stderr[-3000:]}")
    return proc.stdout
