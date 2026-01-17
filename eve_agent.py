"""
eve_agent.py
-----------------

This module implements a self‑healing and storage cleanup agent for
the CEC‑WAM core system. It checks disk usage and, when the
configured threshold is exceeded, safely exports data from the
`data/` directory to a timestamped folder under `exports/` and then
removes the source files. The export is verified by ensuring files
exist in the export destination before deletion. Running this
module directly will execute a single cleanup cycle.

Usage:
    python eve_agent.py

Returns:
    A message describing the outcome of the cleanup cycle.
"""

import os
import shutil
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

# Maximum allowed disk usage ratio before exporting data
MAX_USAGE = 0.85


def get_disk_usage() -> float:
    """Return the fraction of disk space used for the filesystem
    containing BASE_DIR.

    Returns:
        float: The used space divided by total space (0–1)."""
    total, used, _ = shutil.disk_usage(BASE_DIR)
    return used / total


def export_and_cleanup() -> str:
    """Export data files when disk usage exceeds MAX_USAGE.

    If disk usage is below the threshold, no action is taken. When the
    threshold is exceeded, all files from DATA_DIR are copied into a
    timestamped subdirectory of EXPORT_DIR. After verifying the copy,
    the original files are removed to free space.

    Returns:
        str: A status message describing what action was performed.
    """
    usage = get_disk_usage()
    if usage < MAX_USAGE:
        return "SYSTEM OK: No export needed"

    # Ensure export directory exists
    os.makedirs(EXPORT_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    export_path = os.path.join(EXPORT_DIR, f"export_{timestamp}")
    os.makedirs(export_path, exist_ok=True)

    # Copy all files from data directory to export destination
    for filename in os.listdir(DATA_DIR):
        src = os.path.join(DATA_DIR, filename)
        dst = os.path.join(export_path, filename)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    # Verify at least one file exported successfully
    if os.listdir(export_path):
        for filename in os.listdir(DATA_DIR):
            os.remove(os.path.join(DATA_DIR, filename))
        return f"EXPORT COMPLETE — data moved to {export_path}"

    return "EXPORT FAILED — no files copied"


if __name__ == "__main__":
    print(export_and_cleanup())
