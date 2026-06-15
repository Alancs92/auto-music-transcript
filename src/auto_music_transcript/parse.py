"""Parse stage: load symbolic notation into an in-memory score.

For MusicXML/MIDI input this reads the file into a ``music21.stream.Score``.
Kept as a thin, swappable wrapper so the rest of the pipeline never imports a
notation library directly.

Stub stage: the music21-backed implementation lands with the voice-separation
prototype.
"""

from __future__ import annotations

from pathlib import Path


def parse(path: str | Path) -> object:
    """Parse a symbolic score file (MusicXML/MIDI) into a score object.

    Args:
        path: Path to a MusicXML or MIDI file.

    Returns:
        A parsed notation object (expected: ``music21.stream.Score``).
    """
    raise NotImplementedError(
        "Symbolic parsing is not implemented yet. Planned: "
        "music21.converter.parse(path)."
    )
