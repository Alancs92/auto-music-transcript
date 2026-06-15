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


def test_known_format_routes_then_reports_unimplemented(tmp_path, capsys):
    # A recognised input should classify and route, then exit 1 because the
    # pipeline stages are still stubs.
    f = tmp_path / "score.musicxml"
    f.write_text("<score/>")
    assert main([str(f), "-o", str(tmp_path / "out")]) == 1
    captured = capsys.readouterr()
    assert "musicxml" in captured.out.lower()
    assert "not implemented" in captured.err.lower()
