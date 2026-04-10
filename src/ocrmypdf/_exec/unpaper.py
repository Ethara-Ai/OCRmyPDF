# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Interface to unpaper executable."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from subprocess import PIPE, STDOUT
from tempfile import TemporaryDirectory

from packaging.version import Version
from PIL import Image

from ocrmypdf.exceptions import SubprocessOutputError
from ocrmypdf.subprocess import get_version, run

# unpaper documentation:
# https://github.com/Flameeyes/unpaper/blob/main/doc/basic-concepts.md


UNPAPER_IMAGE_PIXEL_LIMIT = 256 * 1024 * 1024

DecFloat = Decimal | float

log = logging.getLogger(__name__)


class UnpaperImageTooLargeError(Exception):
    """To capture details when an image is too large for unpaper."""

    def __init__(
        self,
        w,
        h,
        message="Image with size {}x{} is too large for cleaning with 'unpaper'.",
    ):
        self.w = w
        self.h = h
        self.message = message.format(w, h)
        super().__init__(self.message)


def version() -> Version:
    return Version(get_version('unpaper', regex=r'(?m).*?(\d+(\.\d+)(\.\d+)?)'))






