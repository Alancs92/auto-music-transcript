"""Command-line interface for auto-music-transcript.

Usage:
    amt path/to/score.musicxml -o output/
    amt --version

The CLI is runnable today: it validates and classifies the input and reports
the planned routing. The actual stages are stubs, so a real run currently exits
with a clear "not implemented yet" message rather than producing audio.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, ingest, pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="amt",
        description="Turn a music score into separated SATB audio tracks.",
    )
    parser.add_argument("input", nargs="?", help="Score file (MusicXML/MIDI/PDF/image).")
    parser.add_argument(
        "-o",
        "--out-dir",
        default="output",
        help="Directory for rendered outputs (default: output/).",
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Render WAV audio instead of MIDI (requires the 'audio' extra).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"auto-music-transcript {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.input:
        parser.print_help()
        return 0

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 2

    kind = ingest.classify(input_path)
    if kind is ingest.InputKind.UNKNOWN:
        print(f"error: unrecognised input format: {input_path.name}", file=sys.stderr)
        return 2

    route = "OMR -> parse" if ingest.needs_omr(kind) else "parse"
    print(f"Input: {input_path}  (detected: {kind.value}; routing: {route})")

    try:
        result = pipeline.run(input_path, args.out_dir, audio=args.audio)
    except NotImplementedError as exc:
        print(f"\nPipeline stage not implemented yet:\n  {exc}", file=sys.stderr)
        return 1

    print(f"Done. Outputs written to {args.out_dir}:")
    for label, path in result.outputs.items():
        print(f"  {label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
