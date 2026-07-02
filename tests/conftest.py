"""Shared test fixtures: generated SATB MusicXML scores.

Building the fixtures with music21 (rather than committing binary/XML files)
keeps the repo clean and exercises the real parse path.
"""

import pytest

# Note pitches per voice — soprano highest, bass lowest, no crossing.
SOPRANO = ["C5", "D5", "E5", "F5"]
ALTO = ["E4", "F4", "G4", "A4"]
TENOR = ["C4", "D4", "E4", "F4"]
BASS = ["C3", "G3", "C3", "F3"]


@pytest.fixture
def satb_open_path(tmp_path):
    """Open score: four separate, named parts (Soprano/Alto/Tenor/Bass)."""
    from music21 import clef, note, stream

    score = stream.Score()
    layout = [
        ("Soprano", SOPRANO, clef.TrebleClef()),
        ("Alto", ALTO, clef.TrebleClef()),
        ("Tenor", TENOR, clef.Treble8vbClef()),
        ("Bass", BASS, clef.BassClef()),
    ]
    for name, pitches, clf in layout:
        part = stream.Part()
        part.partName = name
        part.append(clf)
        for p in pitches:
            part.append(note.Note(p, quarterLength=1))
        score.insert(0, part)

    fp = tmp_path / "satb_open.musicxml"
    score.write("musicxml", fp=str(fp))
    return fp


@pytest.fixture
def satb_closed_path(tmp_path):
    """Closed score: two parts, two voices each (S/A on top, T/B on bottom)."""
    from music21 import note, stream

    score = stream.Score()

    def staff(name, upper, lower):
        part = stream.Part()
        part.partName = name
        measure = stream.Measure(number=1)
        v_up = stream.Voice(id="1")
        v_lo = stream.Voice(id="2")
        for p in upper:
            v_up.append(note.Note(p, quarterLength=1))
        for p in lower:
            v_lo.append(note.Note(p, quarterLength=1))
        measure.insert(0, v_up)
        measure.insert(0, v_lo)
        part.append(measure)
        return part

    score.insert(0, staff("Women", SOPRANO, ALTO))
    score.insert(0, staff("Men", TENOR, BASS))

    fp = tmp_path / "satb_closed.musicxml"
    score.write("musicxml", fp=str(fp))
    return fp
