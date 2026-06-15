"""Recognize stage: rendered score (PDF/image) -> structured notation.

Wraps Optical Music Recognition (OMR). Candidate backends from the README are
Audiveris and oemer. This stage is only invoked for PDF/image inputs; symbolic
inputs (MusicXML/MIDI) skip it entirely.

Stub stage: OMR is the project's hardest component and is deferred until after
the MusicXML path works end to end.
"""

from __future__ import annotations

from pathlib import Path


def recognize(path: str | Path) -> object:
    """Run OMR on a rendered score and return structured notation.

    Args:
        path: Path to a PDF or image score.

    Returns:
        A parsed notation object (expected: ``music21.stream.Score``).
    """
    raise NotImplementedError(
        "OMR is not implemented yet. Planned backends: Audiveris or oemer. "
        "The MusicXML input path is being built first (skips this stage)."
    )
