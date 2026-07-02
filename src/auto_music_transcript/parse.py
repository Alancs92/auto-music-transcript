"""Parse stage: load symbolic notation into an in-memory score.

For MusicXML/MIDI input this reads the file into a ``music21.stream.Score``.
Kept as a thin, swappable wrapper so the rest of the pipeline never imports a
notation library directly.
"""

from __future__ import annotations

from pathlib import Path


def parse(path: str | Path):
    """Parse a symbolic score file (MusicXML/MIDI) into a score object.

    Args:
        path: Path to a MusicXML or MIDI file.

    Returns:
        A parsed ``music21.stream.Score``.

    Raises:
        ValueError: If the file cannot be parsed as notation.
    """
    from music21 import converter

    try:
        return converter.parse(str(path))
    except Exception as exc:  # music21 raises a variety of types on bad input
        raise ValueError(f"Could not parse score: {path} ({exc})") from exc
