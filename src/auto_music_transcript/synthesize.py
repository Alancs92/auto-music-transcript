"""Synthesize stage: SATB notation -> audio/MIDI output files.

Renders each separated voice to its own file plus a combined mix. The first
target is MIDI export (pure Python via music21 — no system audio tooling
needed). Audio rendering (WAV/MP3) comes later via FluidSynth + a SoundFont,
with pydub/ffmpeg for mixing.

Stub stage: signatures and the output contract are defined here.
"""

from __future__ import annotations

from pathlib import Path

from .voices import SeparatedVoices


def render_midi(voices: SeparatedVoices, out_dir: str | Path) -> dict[str, Path]:
    """Render each SATB voice to a per-part MIDI file plus a combined mix.

    Args:
        voices: The separated SATB streams.
        out_dir: Directory to write the MIDI files into.

    Returns:
        Mapping of output label (e.g. ``"soprano"``, ``"mix"``) to file path.
    """
    raise NotImplementedError(
        "MIDI rendering is not implemented yet. Planned: write one .mid per "
        "voice via music21, plus a combined 4-track mix."
    )


def render_audio(voices: SeparatedVoices, out_dir: str | Path) -> dict[str, Path]:
    """Render each SATB voice to audio (WAV) plus a combined mix.

    Requires system FluidSynth and a SoundFont (the ``audio`` extra). Deferred
    until the MIDI path is solid.

    Args:
        voices: The separated SATB streams.
        out_dir: Directory to write the audio files into.

    Returns:
        Mapping of output label to file path.
    """
    raise NotImplementedError(
        "Audio rendering is not implemented yet. Planned: FluidSynth + "
        "SoundFont per part, mixed with pydub/ffmpeg."
    )
