"""Utilities for emotion calculations (stub)."""

from typing import Dict


def compute_emotions(hormones: Dict[str, int]) -> Dict[str, float]:
    """Return emotion levels derived from hormones (placeholder)."""
    # Placeholder using simple scaling
    return {k: (v - 50) / 5 for k, v in hormones.items()}
