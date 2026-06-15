"""End-to-end pipeline orchestration.

Wires the stages together: ingest -> (recognize | parse) -> separate ->
synthesize. Each stage is a stub today; this module defines the control flow so
the shape of the program is fixed before the stages are filled in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import ingest, parse, recognize, synthesize, voices


@dataclass
class PipelineResult:
    """Outcome of a pipeline run."""

    input_path: Path
    input_kind: ingest.InputKind
    outputs: dict[str, Path] = field(default_factory=dict)


def run(input_path: str | Path, out_dir: str | Path, *, audio: bool = False) -> PipelineResult:
    """Run the full score -> SATB pipeline.

    Args:
        input_path: The score to process (MusicXML/MIDI/PDF/image).
        out_dir: Directory for the rendered per-part + mix outputs.
        audio: If True, render WAV audio; otherwise render MIDI.

    Returns:
        A :class:`PipelineResult` describing the run and its outputs.
    """
    input_path = Path(input_path)
    out_dir = Path(out_dir)

    kind = ingest.classify(input_path)
    if kind is ingest.InputKind.UNKNOWN:
        raise ValueError(f"Unrecognised input format: {input_path.name}")

    # Recognize (OMR) for rendered inputs, otherwise parse symbolic notation.
    score = recognize.recognize(input_path) if ingest.needs_omr(kind) else parse.parse(input_path)

    separated = voices.separate(score)

    out_dir.mkdir(parents=True, exist_ok=True)
    if audio:
        outputs = synthesize.render_audio(separated, out_dir)
    else:
        outputs = synthesize.render_midi(separated, out_dir)

    return PipelineResult(input_path=input_path, input_kind=kind, outputs=outputs)
