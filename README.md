# auto-music-transcript

Turn a written music score into singable **SATB** (Soprano, Alto, Tenor, Bass) audio — automatically.

## The idea

Give the tool a score in whatever form it exists — a scanned **PDF**, an image, a **MusicXML** export from notation software (Sibelius, MuseScore, Finale), or another machine-readable format — and have it produce **separate audio tracks for each voice part** (soprano, alto, tenor, bass), plus a combined mix.

The goal is a practice aid: a singer can play their own part, mute the others, slow it down, and learn it by ear. It won't be perfect at first — OCR of printed music is hard and expressive nuance is lost — but a roughly-correct, part-separated playback is already useful.

## How it could work (pipeline)

1. **Ingest** — accept PDF / image / MusicXML / MIDI / other input.
2. **Recognize** — if the input isn't already symbolic, run Optical Music Recognition (OMR) to convert the page into structured notation (MusicXML / MEI). For MusicXML/MIDI input, skip straight to parsing.
3. **Parse & separate voices** — read the notation and split it into the four SATB parts (handling shared staves, divisi, and lyrics where present).
4. **Synthesize** — render each part to audio (MIDI synthesis, sampled voices, or a singing-voice synthesizer for lyrics).
5. **Output** — export per-part tracks (S, A, T, B) and a full mix; expose tempo and per-part volume/mute controls.

## Candidate building blocks

- **OMR:** Audiveris, oemer, or a hosted OMR service.
- **Notation parsing:** music21, partitura.
- **Synthesis:** FluidSynth + a SoundFont for instrument-style playback; a singing-voice synth (e.g. Sinsy / NNSVS-style) for lyrics.
- **Audio I/O:** pydub / ffmpeg for mixing and export.

## Status

Early scaffold. The Python package skeleton and CLI are in place; pipeline
stages are stubs with defined input/output contracts. Next up: the MusicXML →
4-part voice-separation prototype.

## Project layout

```
src/auto_music_transcript/
  ingest.py       # detect & classify input (MusicXML / MIDI / PDF / image)
  recognize.py    # OMR for rendered scores (stub)
  parse.py        # symbolic notation -> score object (stub)
  voices.py       # score -> Soprano/Alto/Tenor/Bass streams (stub)
  synthesize.py   # SATB -> per-part + mix MIDI/audio (stub)
  pipeline.py     # wires the stages together
  cli.py          # `amt` command-line entry point
tests/            # unit tests for the stages that work today
```

## Development

```bash
# Editable install with dev + (optional) audio extras
python -m pip install -e ".[dev]"

# Run the test suite
pytest

# Try the CLI (classifies input and reports routing; stages are stubs)
amt path/to/score.musicxml -o output/
amt --version
```

## Known hard parts

- OMR accuracy on scanned or handwritten scores.
- Correctly assigning notes to the right voice when parts share a staff.
- Aligning lyrics to notes for sung output.

## Roadmap (rough)

- [x] Project skeleton: package layout, CLI stub, dependency declarations, tests.
- [x] Decide primary input format to support first (MusicXML — easiest, skips OMR).
- [ ] Voice-separation prototype from MusicXML → 4 MIDI tracks.
- [ ] Per-part audio rendering + combined mix.
- [ ] Add PDF/image input via OMR.
- [ ] Add lyric-aware singing synthesis.

## License

TBD.
