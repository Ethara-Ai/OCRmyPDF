# SPDX-FileCopyrightText: 2019-2023 James R. Barlow
# SPDX-FileCopyrightText: 2019 Martin Wind
# SPDX-License-Identifier: MPL-2.0

"""Implements the concurrent and page synchronous parts of the pipeline."""

from __future__ import annotations

import logging
import logging.handlers
import shutil
from functools import partial

import PIL

from ocrmypdf._concurrent import Executor
from ocrmypdf._jobcontext import PageContext, PdfContext
from ocrmypdf._options import OcrOptions
from ocrmypdf._pipeline import (
    is_ocr_required,
    ocr_engine_hocr,
    validate_pdfinfo_options,
)
from ocrmypdf._pipelines._common import (
    HOCRResult,
    do_get_pdfinfo,
    manage_work_folder,
    process_page,
    set_thread_pageno,
    setup_pipeline,
    worker_init,
)
from ocrmypdf._plugin_manager import OcrmypdfPluginManager
from ocrmypdf.helpers import available_cpu_count

log = logging.getLogger(__name__)


def _exec_page_hocr_sync(page_context: PageContext) -> HOCRResult:
    """Execute a pipeline for a single page hOCR."""
    pass


def exec_pdf_to_hocr(context: PdfContext, executor: Executor) -> None:
    """Execute the OCR pipeline concurrently and output hOCR."""
    pass


def run_hocr_pipeline(
    options: OcrOptions,
    *,
    plugin_manager: OcrmypdfPluginManager,
) -> None:
    """Run pipeline to output hOCR."""
    pass
