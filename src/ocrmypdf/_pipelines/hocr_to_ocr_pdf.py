# SPDX-FileCopyrightText: 2019-2023 James R. Barlow
# SPDX-FileCopyrightText: 2019 Martin Wind
# SPDX-License-Identifier: MPL-2.0

"""Implements the concurrent and page synchronous parts of the pipeline."""

from __future__ import annotations

import logging
import logging.handlers
from collections.abc import Sequence
from functools import partial

import PIL

from ocrmypdf._concurrent import Executor
from ocrmypdf._graft import OcrGrafter
from ocrmypdf._jobcontext import PageContext, PdfContext
from ocrmypdf._options import OcrOptions
from ocrmypdf._pipeline import copy_final
from ocrmypdf._pipelines._common import (
    HOCRResult,
    do_get_pdfinfo,
    manage_work_folder,
    postprocess,
    report_output_pdf,
    set_thread_pageno,
    setup_pipeline,
    worker_init,
)
from ocrmypdf._plugin_manager import OcrmypdfPluginManager
from ocrmypdf._progressbar import ProgressBar
from ocrmypdf.exceptions import ExitCode
from ocrmypdf.helpers import available_cpu_count

log = logging.getLogger(__name__)


def _exec_hocrtransform_sync(page_context: PageContext) -> HOCRResult:
    """Process each page."""
    pass


def exec_hocr_to_ocr_pdf(context: PdfContext, executor: Executor) -> Sequence[str]:
    """Convert hOCR files to OCR PDF."""
    pass


def run_hocr_to_ocr_pdf_pipeline(
    options: OcrOptions,
    *,
    plugin_manager: OcrmypdfPluginManager,
) -> ExitCode:
    """Run pipeline to convert hOCR to final output PDF."""
    pass
