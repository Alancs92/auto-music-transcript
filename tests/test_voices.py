"""Tests for SATB voice separation."""

import pytest

from auto_music_transcript import parse
from auto_music_transcript.voices import (
    SeparatedVoices,
    Voice,
    VoiceSeparationError,
    _avg_pitch,
    separate,
)


def _check_ordering(sv: SeparatedVoices):
    """Soprano > Alto > Tenor > Bass by average pitch; each part has notes."""
    avgs = {v: _avg_pitch(part) for v, part in sv.as_dict().items()}
    assert avgs[Voice.SOPRANO] > avgs[Voice.ALTO] > avgs[Voice.TENOR] > avgs[Voice.BASS]
    for part in sv.as_dict().values():
        assert len(part.flatten().notes) == 4


def test_separate_open_score(satb_open_path):
    sv = separate(parse.parse(satb_open_path))
    _check_ordering(sv)
    # Named parts should keep their labels.
    assert sv.soprano.partName == "Soprano"
    assert sv.bass.partName == "Bass"


def test_separate_closed_score(satb_closed_path):
    sv = separate(parse.parse(satb_closed_path))
    _check_ordering(sv)


def test_open_score_falls_back_to_pitch_when_unnamed(satb_open_path, monkeypatch):
    # Strip names so the name matcher fails and pitch ordering takes over.
    score = parse.parse(satb_open_path)
    for p in score.parts:
        p.partName = None
    sv = separate(score)
    _check_ordering(sv)


def test_too_few_voices_raises():
    from music21 import note, stream

    score = stream.Score()
    for pitches in (["C5", "D5"], ["C3", "D3"]):  # only 2 parts, 1 voice each
        part = stream.Part()
        for p in pitches:
            part.append(note.Note(p, quarterLength=1))
        score.insert(0, part)

    with pytest.raises(VoiceSeparationError, match="found 2"):
        separate(score)


def test_empty_score_raises():
    from music21 import stream

    with pytest.raises(VoiceSeparationError, match="no parts"):
        separate(stream.Score())
