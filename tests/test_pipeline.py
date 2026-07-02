"""End-to-end pipeline tests: MusicXML -> per-part + mix MIDI."""

from auto_music_transcript import pipeline
from auto_music_transcript.ingest import InputKind

EXPECTED_OUTPUTS = {"soprano", "alto", "tenor", "bass", "mix"}


def test_run_open_score_to_midi(satb_open_path, tmp_path):
    out = tmp_path / "out"
    result = pipeline.run(satb_open_path, out)

    assert result.input_kind is InputKind.MUSICXML
    assert set(result.outputs) == EXPECTED_OUTPUTS
    for path in result.outputs.values():
        assert path.exists() and path.stat().st_size > 0


def test_rendered_midi_is_reparseable(satb_open_path, tmp_path):
    # The soprano MIDI should round-trip back to 4 notes.
    from music21 import converter

    result = pipeline.run(satb_open_path, tmp_path / "out")
    soprano = converter.parse(str(result.outputs["soprano"]))
    assert len(soprano.flatten().notes) == 4


def test_run_closed_score_to_midi(satb_closed_path, tmp_path):
    result = pipeline.run(satb_closed_path, tmp_path / "out")
    assert set(result.outputs) == EXPECTED_OUTPUTS
    for path in result.outputs.values():
        assert path.exists() and path.stat().st_size > 0
