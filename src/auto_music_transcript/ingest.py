"""Ingest stage: accept and classify an input score file.

Detects what kind of input we were handed so the pipeline can route it:
symbolic formats (MusicXML, MIDI) go straight to parsing, while rendered
formats (PDF, image) must first pass through Optical Music Recognition.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path


class InputKind(str, Enum):
    """Recognised input categories."""

    MUSICXML = "musicxml"  # symbolic; parse directly
    MIDI = "midi"          # symbolic; parse directly
    PDF = "pdf"            # rendered; needs OMR
    IMAGE = "image"        # rendered; needs OMR
    UNKNOWN = "unknown"


# Extension -> kind. Lower-cased suffixes (including the leading dot).
_EXTENSION_MAP: dict[str, InputKind] = {
    ".xml": InputKind.MUSICXML,
    ".musicxml": InputKind.MUSICXML,
    ".mxl": InputKind.MUSICXML,
    ".mid": InputKind.MIDI,
    ".midi": InputKind.MIDI,
    ".pdf": InputKind.PDF,
    ".png": InputKind.IMAGE,
    ".jpg": InputKind.IMAGE,
    ".jpeg": InputKind.IMAGE,
    ".tif": InputKind.IMAGE,
    ".tiff": InputKind.IMAGE,
}


def classify(path: str | Path) -> InputKind:
    """Classify an input file by its extension.

    Args:
        path: Path to the input score file.

    Returns:
        The detected :class:`InputKind` (``UNKNOWN`` if unrecognised).
    """
    suffix = Path(path).suffix.lower()
    return _EXTENSION_MAP.get(suffix, InputKind.UNKNOWN)


def needs_omr(kind: InputKind) -> bool:
    """Whether an input kind must pass through Optical Music Recognition."""
    return kind in (InputKind.PDF, InputKind.IMAGE)
