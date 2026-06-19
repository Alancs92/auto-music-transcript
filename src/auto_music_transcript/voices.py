"""Voice separation: structured notation -> four SATB parts.

Takes a parsed ``music21.stream.Score`` and produces four independent parts —
Soprano, Alto, Tenor, Bass. Two common layouts are handled:

* **Open score** — four separate parts, one voice each. Mapped to SATB by part
  name when the names are recognisable, otherwise by descending average pitch.
* **Closed score** — two parts that each carry two voices on a shared staff
  (e.g. S/A on the upper staff, T/B on the lower). Each staff is split into its
  upper/lower voice by pitch, preserving the staff grouping.

A generic fallback sorts all detected voice lines by average pitch. Inputs that
don't resolve to exactly four voice lines raise :class:`VoiceSeparationError`.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from enum import Enum


class Voice(str, Enum):
    """The four SATB voice parts, highest to lowest."""

    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"


class VoiceSeparationError(ValueError):
    """Raised when a score can't be resolved into four SATB voices."""


@dataclass
class SeparatedVoices:
    """Result of voice separation: one notation stream per SATB part.

    Each value is a ``music21.stream.Part``.
    """

    soprano: object
    alto: object
    tenor: object
    bass: object

    def as_dict(self) -> dict[Voice, object]:
        return {
            Voice.SOPRANO: self.soprano,
            Voice.ALTO: self.alto,
            Voice.TENOR: self.tenor,
            Voice.BASS: self.bass,
        }


# Keywords used to recognise a part's intended voice from its name.
_NAME_HINTS: dict[Voice, tuple[str, ...]] = {
    Voice.SOPRANO: ("soprano", "sop", "descant"),
    Voice.ALTO: ("alto", "contralto"),
    Voice.TENOR: ("tenor",),
    Voice.BASS: ("bass", "baritone"),
}


def _avg_pitch(line) -> float:
    """Average MIDI pitch of the notes in a stream (0.0 if it has none)."""
    pitches = [n.pitch.midi for n in line.flatten().notes if n.isNote]
    # Chords contribute their highest pitch (the sung/leading line).
    for ch in line.flatten().notes:
        if ch.isChord:
            pitches.append(max(p.midi for p in ch.pitches))
    return sum(pitches) / len(pitches) if pitches else 0.0


def _extract_lines(part) -> list[object]:
    """Split a part into independent voice lines as flat ``Part`` streams.

    If the part contains ``Voice`` elements (a shared staff), each distinct voice
    id becomes its own line, with notes placed at their absolute offsets. A part
    with no explicit voices yields a single line.
    """
    from music21 import stream

    voices = list(part.recurse().getElementsByClass(stream.Voice))
    if not voices:
        line = stream.Part()
        for el in part.flatten().notesAndRests:
            line.insert(el.offset, copy.deepcopy(el))
        return [line]

    # Group voices by id, preserving first-seen order, across all measures.
    grouped: dict[str, object] = {}
    for measure in part.getElementsByClass(stream.Measure):
        m_offset = measure.offset
        for v in measure.getElementsByClass(stream.Voice):
            vid = str(v.id)
            line = grouped.get(vid)
            if line is None:
                line = stream.Part()
                grouped[vid] = line
            for el in v.notesAndRests:
                line.insert(m_offset + el.offset, copy.deepcopy(el))
    return list(grouped.values())


def _label_line(line, voice: Voice):
    """Tag a line's part name/id with its assigned voice (nicer MIDI tracks)."""
    line.partName = voice.value.capitalize()
    line.id = voice.value
    return line


def _match_by_name(parts) -> dict[Voice, object] | None:
    """Map four single-voice parts to SATB by name, or None if names don't fit."""
    assigned: dict[Voice, object] = {}
    used: set[int] = set()
    for voice, hints in _NAME_HINTS.items():
        for i, part in enumerate(parts):
            if i in used:
                continue
            name = (getattr(part, "partName", None) or "").lower()
            if any(h in name for h in hints):
                assigned[voice] = _extract_lines(part)[0]
                used.add(i)
                break
    return assigned if len(assigned) == 4 else None


def _assign_by_pitch(lines) -> dict[Voice, object]:
    """Assign four voice lines to SATB by descending average pitch."""
    ordered = sorted(lines, key=_avg_pitch, reverse=True)
    return dict(zip((Voice.SOPRANO, Voice.ALTO, Voice.TENOR, Voice.BASS), ordered))


def separate(score) -> SeparatedVoices:
    """Split a parsed score into four SATB voice streams.

    Args:
        score: A parsed ``music21.stream.Score``.

    Returns:
        A :class:`SeparatedVoices` with one ``Part`` per voice.

    Raises:
        VoiceSeparationError: If the score doesn't resolve to four voices.
    """
    parts = list(getattr(score, "parts", []))
    if not parts:
        raise VoiceSeparationError("Score contains no parts to separate.")

    lines_per_part = [_extract_lines(p) for p in parts]
    total = sum(len(lp) for lp in lines_per_part)
    if total != 4:
        raise VoiceSeparationError(
            f"Expected 4 voice lines for SATB, found {total} "
            f"across {len(parts)} part(s). Layouts supported: 4 separate parts, "
            f"or 2 parts with 2 voices each."
        )

    assigned: dict[Voice, object]
    if len(parts) == 4 and all(len(lp) == 1 for lp in lines_per_part):
        # Open score: prefer names, fall back to pitch ordering.
        assigned = _match_by_name(parts) or _assign_by_pitch(
            [lp[0] for lp in lines_per_part]
        )
    elif len(parts) == 2 and all(len(lp) == 2 for lp in lines_per_part):
        # Closed score: top staff -> S/A, bottom staff -> T/B (by pitch within).
        top = sorted(lines_per_part[0], key=_avg_pitch, reverse=True)
        bottom = sorted(lines_per_part[1], key=_avg_pitch, reverse=True)
        assigned = {
            Voice.SOPRANO: top[0],
            Voice.ALTO: top[1],
            Voice.TENOR: bottom[0],
            Voice.BASS: bottom[1],
        }
    else:
        # Mixed layout: best-effort global pitch ordering.
        all_lines = [ln for lp in lines_per_part for ln in lp]
        assigned = _assign_by_pitch(all_lines)

    for voice, line in assigned.items():
        _label_line(line, voice)

    return SeparatedVoices(
        soprano=assigned[Voice.SOPRANO],
        alto=assigned[Voice.ALTO],
        tenor=assigned[Voice.TENOR],
        bass=assigned[Voice.BASS],
    )
