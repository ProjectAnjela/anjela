import os
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile


RUNTIME_CONTEXT_FILES = {
    "anjela/context/archive-index.md",
    "anjela/context/boot.md",
    "anjela/context/memory.md",
    "anjela/context/personality.md",
    "anjela/context/project-history.md",
}


def test_wheel_contains_context_and_loads_default(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    source = tmp_path / "source"
    wheel_dir = tmp_path / "wheel"
    extracted = tmp_path / "extracted"
    shutil.copytree(
        repository,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".pytest_cache",
            ".superpowers",
            ".venv",
            "__pycache__",
            "*.egg-info",
            "build",
        ),
    )
    wheel_dir.mkdir()

    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            ".",
            "--no-deps",
            "--wheel-dir",
            str(wheel_dir),
        ],
        cwd=source,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1
    with ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())
        assert RUNTIME_CONTEXT_FILES <= names
        wheel.extractall(extracted)

    environment = os.environ.copy()
    environment.pop("ANJELA_CONTEXT_DIR", None)
    smoke_test = subprocess.run(
        [
            sys.executable,
            "-S",
            "-c",
            (
                "from anjela.context_loader import load_context; "
                "bundle = load_context(); "
                "assert 'boot.md' in bundle.instructions; "
                "assert 'personality.md' in bundle.instructions; "
                "assert bundle.reference_context; "
                "print('packaged-context-ok')"
            ),
        ],
        cwd=extracted,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert smoke_test.returncode == 0, smoke_test.stdout + smoke_test.stderr
    assert smoke_test.stdout.strip() == "packaged-context-ok"
