"""Tests for input classification and routing."""

import pytest

from auto_music_transcript.ingest import InputKind, classify, needs_omr


@pytest.mark.parametrize(
    "name,expected",
    [
        ("score.musicxml", InputKind.MUSICXML),
        ("score.xml", InputKind.MUSICXML),
        ("score.mxl", InputKind.MUSICXML),
        ("tune.MID", InputKind.MIDI),  # case-insensitive
        ("tune.midi", InputKind.MIDI),
        ("scan.pdf", InputKind.PDF),
        ("page.PNG", InputKind.IMAGE),
        ("page.jpeg", InputKind.IMAGE),
        ("notes.txt", InputKind.UNKNOWN),
        ("noextension", InputKind.UNKNOWN),
    ],
)
def test_classify(name, expected):
    assert classify(name) == expected


@pytest.mark.parametrize(
    "kind,expected",
    [
        (InputKind.PDF, True),
        (InputKind.IMAGE, True),
        (InputKind.MUSICXML, False),
        (InputKind.MIDI, False),
        (InputKind.UNKNOWN, False),
    ],
)
def test_needs_omr(kind, expected):
    assert needs_omr(kind) is expected
