"""Voice separation: structured notation -> four SATB parts.

This is the heart of the project's first real milestone. The job is to take
parsed notation (a ``music21.stream.Score``) and produce four independent
streams — Soprano, Alto, Tenor, Bass — handling the common cases where two
voices share a single staff (e.g. S/A on the treble staff, T/B on the bass
staff) as well as one-part-per-staff layouts.

Stub stage: the contract is defined here; the implementation lands in the
voice-separation prototype milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Voice(str, Enum):
    """The four SATB voice parts, highest to lowest."""

    SOPRANO = "soprano"
    ALTO = "alto"
    TENOR = "tenor"
    BASS = "bass"


@dataclass
class SeparatedVoices:
    """Result of voice separation: one notation stream per SATB part.

    Each value is intended to be a ``music21.stream.Part`` (or ``Score``), but
    is left untyped here so the skeleton has no hard dependency on music21 at
    import time.
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


def separate(score: object) -> SeparatedVoices:
    """Split a parsed score into four SATB voice streams.

    Args:
        score: A parsed notation object (expected: ``music21.stream.Score``).

    Returns:
        A :class:`SeparatedVoices` with one stream per voice part.
    """
    raise NotImplementedError(
        "Voice separation is not implemented yet. This is the first prototype "
        "milestone: map staves/voices in the score to Soprano/Alto/Tenor/Bass."
    )
