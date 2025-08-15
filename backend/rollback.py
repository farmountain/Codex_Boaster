"""Utility helpers for creating and restoring artifact snapshots using git tags."""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

ARTIFACT_DIR = Path(os.getenv("ARTIFACT_DIR", "artifacts"))
SNAPSHOT_DIR = Path(os.getenv("SNAPSHOT_DIR", "snapshots"))


def create_snapshot(tag: Optional[str] = None) -> str:
    """Snapshot the current artifacts and create a matching git tag."""

    tag = tag or datetime.utcnow().strftime("snapshot-%Y%m%d%H%M%S")
    dest = SNAPSHOT_DIR / tag
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"snapshot {tag} already exists")
    if ARTIFACT_DIR.exists():
        shutil.copytree(ARTIFACT_DIR, dest)
    subprocess.run(["git", "tag", tag], check=False)
    return str(dest)


def restore_snapshot(tag: str) -> str:
    """Restore artifacts from a snapshot and checkout the git tag."""

    src = SNAPSHOT_DIR / tag
    if not src.exists():
        raise FileNotFoundError(f"snapshot {tag} not found")
    if ARTIFACT_DIR.exists():
        shutil.rmtree(ARTIFACT_DIR)
    shutil.copytree(src, ARTIFACT_DIR)
    subprocess.run(["git", "checkout", tag], check=False)
    return str(ARTIFACT_DIR)


__all__ = ["create_snapshot", "restore_snapshot"]
