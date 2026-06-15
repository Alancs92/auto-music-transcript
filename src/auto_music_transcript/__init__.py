"""auto-music-transcript: score in, separated SATB audio out.

This package is organised around the pipeline described in the project README:

    ingest -> recognize -> separate voices -> synthesize -> output

Each stage lives in its own module so it can be developed and tested in
isolation. At the skeleton stage most stages are stubs that raise
``NotImplementedError``; they describe their intended input/output contract.
"""

__version__ = "0.0.1"

__all__ = ["__version__"]
