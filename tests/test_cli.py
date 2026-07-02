"""Tests for the CLI surface that works at the skeleton stage."""

import pytest

from auto_music_transcript import __version__
from auto_music_transcript.cli import main


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_args_prints_help(capsys):
    assert main([]) == 0
    assert "usage" in capsys.readouterr().out.lower()


def test_missing_file_errors(capsys):
    assert main(["does-not-exist.musicxml"]) == 2
    assert "not found" in capsys.readouterr().err.lower()


def test_unknown_format_errors(tmp_path, capsys):
    f = tmp_path / "notes.txt"
    f.write_text("not a score")
    assert main([str(f)]) == 2
    assert "unrecognised" in capsys.readouterr().err.lower()


def test_musicxml_runs_end_to_end(satb_open_path, tmp_path, capsys):
    # A real MusicXML score now flows all the way to MIDI outputs.
    out = tmp_path / "out"
    assert main([str(satb_open_path), "-o", str(out)]) == 0
    captured = capsys.readouterr()
    assert "musicxml" in captured.out.lower()
    assert "soprano" in captured.out.lower()
    assert (out / "mix.mid").exists()


def test_pdf_input_reports_omr_unimplemented(tmp_path, capsys):
    # The OMR stage is still a stub, so PDF input exits 1 with a clear message.
    f = tmp_path / "scan.pdf"
    f.write_bytes(b"%PDF-1.4 fake")
    assert main([str(f), "-o", str(tmp_path / "out")]) == 1
    captured = capsys.readouterr()
    assert "omr" in captured.out.lower()  # routing line mentions OMR
    assert "not implemented" in captured.err.lower()
