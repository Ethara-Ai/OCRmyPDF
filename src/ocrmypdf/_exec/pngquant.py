# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Interface to pngquant executable."""

from __future__ import annotations

from pathlib import Path
from subprocess import PIPE

from packaging.version import Version

from ocrmypdf.exceptions import MissingDependencyError
from ocrmypdf.subprocess import get_version, run


def version() -> Version:
    return Version(get_version('pngquant', regex=r'(\d+(\.\d+)*).*'))


def available():
    try:
        version()
    except MissingDependencyError:
        return False
    return True


def quantize(input_file: Path, output_file: Path, quality_min: int, quality_max: int):
    """Quantize a PNG image using pngquant.

    Args:
        input_file: Input PNG image
        output_file: Output PNG image
        quality_min: Minimum quality to use
        quality_max: Maximum quality to use
    """
    pass
