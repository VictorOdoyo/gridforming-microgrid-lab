"""Provenance for reproducible experiments; no credentials or environment variables collected."""

import hashlib
import importlib.metadata
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from .config_io import case_dict


def configuration_hash(case):
    canonical = json.dumps(case_dict(case), sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def provenance(case):
    root = Path(__file__).resolve().parents[2]

    def git(*args):
        try:
            return subprocess.check_output(
                ["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            return None

    versions = {}
    for package in ("numpy", "scipy", "matplotlib"):
        versions[package] = importlib.metadata.version(package)
    status = git("status", "--porcelain")
    return {
        "created_utc": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "dependencies": versions,
        "configuration_sha256": configuration_hash(case),
        "git_commit": git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else bool(status),
    }
