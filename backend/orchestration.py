"""Utilities for orchestration policies and artifact management."""

import os
import shutil
from pathlib import Path
from typing import Any, Optional


class GuardrailPolicy:
    """Simple guardrail checks for incoming plans or runs."""

    def validate_plan(self, plan: str) -> None:
        """Validate that a plan is safe to execute."""

        if not plan:
            raise ValueError("Plan must not be empty")
        # Extremely small example guardrail to demonstrate policy hooks
        if "DROP TABLE" in plan.upper():
            raise ValueError("Plan contains disallowed content")


class ReviewGate:
    """Placeholder for review approval logic."""

    def approve(self, run: Any) -> bool:
        """Approve a run. In real scenarios this might contact human reviewers."""

        return True


class ArtifactStorage:
    """Store artifacts for runs locally and optionally in object storage."""

    def __init__(
        self,
        base_dir: str = "artifacts",
        bucket: Optional[str] = None,
    ) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.bucket = bucket or os.getenv("OBJECT_STORAGE_BUCKET")
        self.endpoint = os.getenv("OBJECT_STORAGE_ENDPOINT")
        self._s3 = None
        if self.bucket:
            import boto3

            self._s3 = boto3.client("s3", endpoint_url=self.endpoint)

    def _upload(self, path: Path, key: str) -> None:
        if self._s3:
            try:
                self._s3.upload_file(str(path), self.bucket, key)
            except Exception:  # pragma: no cover - upload failures shouldn't crash
                pass

    def save_text(self, run_id: int, name: str, content: str) -> str:
        """Persist a text artifact for a run and return its path."""

        run_dir = self.base_dir / str(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / name
        path.write_text(content)
        self._upload(path, f"{run_id}/{name}")
        return str(path)

    def save_file(self, run_id: int, src: str, name: Optional[str] = None) -> str:
        """Copy an existing file into the artifact store and upload."""

        run_dir = self.base_dir / str(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        dest = run_dir / (name or Path(src).name)
        shutil.copy(src, dest)
        self._upload(dest, f"{run_id}/{dest.name}")
        return str(dest)

