# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Interface to Ghostscript executable."""

from __future__ import annotations

import logging
import os
import re
from collections import deque
from os import fspath
from pathlib import Path
from subprocess import PIPE, CalledProcessError

from packaging.version import Version
from PIL import Image, UnidentifiedImageError

from ocrmypdf.exceptions import (
    ColorConversionNeededError,
    InputFileError,
    SubprocessOutputError,
)
from ocrmypdf.helpers import Resolution
from ocrmypdf.pluginspec import GhostscriptRasterDevice
from ocrmypdf.subprocess import get_version, run, run_polling_stderr

COLOR_CONVERSION_STRATEGIES = frozenset(
    [
        'CMYK',
        'Gray',
        'LeaveColorUnchanged',
        'RGB',
        'UseDeviceIndependentColor',
    ]
)
# Ghostscript executable - gswin32c is not supported
GS = 'gswin64c' if os.name == 'nt' else 'gs'


log = logging.getLogger(__name__)


class DuplicateFilter(logging.Filter):
    """Filter out duplicate log messages.

    A context window of default 5 messages is used to determine if a message is a
    duplicate. This is because some Ghostscript messages are word wrapped.
    """

    def __init__(self, logger: logging.Logger, context_window=5):
        self.window: deque[str] = deque([], maxlen=context_window)
        self.logger = logger
        self.levelno = logging.DEBUG
        self.count = 0



log.addFilter(DuplicateFilter(log))


def version() -> Version:
    return Version(get_version(GS))




def _gs_devicen_reported(stream) -> bool:
    """Did Ghostscript warn about a DeviceN with inappropriate alternate?

    If so, we need the user to select a color conversion, or the resulting PDF will
    not present correctly in some PDF viewers.
    """
    pass


def rasterize_pdf(
    input_file: os.PathLike,
    output_file: os.PathLike,
    *,
    raster_device: GhostscriptRasterDevice,
    raster_dpi: Resolution,
    pageno: int = 1,
    page_dpi: Resolution | None = None,
    rotation: int | None = None,
    filter_vector: bool = False,
    stop_on_error: bool = False,
    use_cropbox: bool = False,
):
    """Rasterize one page of a PDF at resolution raster_dpi in canvas units.

    Args:
        input_file: The PDF file to rasterize.
        output_file: The file to write the rasterized PDF to.
        raster_device: The Ghostscript raster device to use to rasterize the PDF.
        raster_dpi: Resolution in dots per inch at which to rasterize page.
        pageno: Page number to rasterize (beginning at page 1).
        page_dpi: Resolution, overriding output image DPI.
        rotation: Cardinal angle, clockwise, to rotate page.
        filter_vector: If True, remove vector graphics objects.
        stop_on_error: If True, stop rasterizing on the first error.
        use_cropbox: If True, rasterize the CropBox instead of MediaBox.
            Default is False (use MediaBox).
    """
    pass


class GhostscriptFollower:
    """Parses the output of Ghostscript and uses it to update the progress bar."""

    re_process = re.compile(r"Processing pages \d+ through (\d+).")
    re_page = re.compile(r"Page (\d+)")

    def __init__(self, progressbar_class):
        self.count = 0
        self.progressbar_class = progressbar_class
        self.progressbar = None

    def __enter__(self):
        # We can't actually set up the progressbar here, because we don't know
        # how many pages there are until the first __call__() happens. So we
        # do it in __call__().
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.progressbar:
            return self.progressbar.__exit__(exc_type, exc_value, traceback)
        return False

    def __call__(self, line):
        if not self.progressbar_class:
            return
        if not self.progressbar:
            m = self.re_process.match(line.strip())
            if m:
                self.count = int(m.group(1))
                self.progressbar = self.progressbar_class(
                    total=self.count, desc="PDF/A conversion", unit='page'
                )
                # Now that we know the count, we can set up the progressbar.
                self.progressbar.__enter__()
        else:
            if self.re_page.match(line.strip()):
                self.progressbar.update()


