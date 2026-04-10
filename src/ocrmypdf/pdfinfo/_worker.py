# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""PDF page info worker process handling."""

from __future__ import annotations

import atexit
import logging
from collections.abc import Container, Sequence
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

from pikepdf import Pdf

from ocrmypdf._concurrent import Executor
from ocrmypdf._progressbar import ProgressBar
from ocrmypdf.exceptions import InputFileError
from ocrmypdf.helpers import available_cpu_count, pikepdf_enable_mmap

if TYPE_CHECKING:
    from ocrmypdf.pdfinfo.info import PageInfo
    from ocrmypdf.pdfinfo.layout import PdfMinerState

logger = logging.getLogger()

worker_pdf = None  # pylint: disable=invalid-name








