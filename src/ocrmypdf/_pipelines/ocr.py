# SPDX-FileCopyrightText: 2019-2023 James R. Barlow
# SPDX-FileCopyrightText: 2019 Martin Wind
# SPDX-License-Identifier: MPL-2.0

"""Implements the concurrent and page synchronous parts of the pipeline."""

from __future__ import annotations

import logging
import logging.handlers
from collections.abc import Sequence
from functools import partial
from pathlib import Path
from tempfile import mkdtemp

import PIL

from ocrmypdf._concurrent import Executor
from ocrmypdf._graft import OcrGrafter
from ocrmypdf._jobcontext import PageContext, PdfContext
from ocrmypdf._options import OcrOptions
from ocrmypdf._pipeline import (
    copy_final,
    is_ocr_required,
    merge_sidecars,
    ocr_engine_direct,
    ocr_engine_hocr,
    ocr_engine_textonly_pdf,
    triage,
    validate_pdfinfo_options,
)
from ocrmypdf._pipelines._common import (
    PageResult,
    cli_exception_handler,
    do_get_pdfinfo,
    manage_debug_log_handler,
    manage_work_folder,
    postprocess,
    process_page,
    report_output_pdf,
    set_thread_pageno,
    setup_pipeline,
    worker_init,
)
from ocrmypdf._plugin_manager import OcrmypdfPluginManager
from ocrmypdf._progressbar import ProgressBar
from ocrmypdf._validation import (
    check_requested_output_file,
    create_input_file,
)
from ocrmypdf.exceptions import ExitCode
from ocrmypdf.helpers import available_cpu_count
from ocrmypdf.models.ocr_element import OcrElement

log = logging.getLogger(__name__)


def _image_to_ocr_text(
    page_context: PageContext, ocr_image_out: Path
) -> tuple[Path | None, Path, OcrElement | None]:
    """Run OCR engine on image to create OCR PDF and text file."""
    pass


def _exec_page_sync(page_context: PageContext) -> PageResult:
    """Execute a pipeline for a single page synchronously."""
    pass


def exec_concurrent(context: PdfContext, executor: Executor) -> Sequence[str]:
    """Execute the OCR pipeline concurrently."""
    pass




def run_pipeline_cli(
    options: OcrOptions,
    *,
    plugin_manager: OcrmypdfPluginManager,
) -> ExitCode:
    """Run the OCR pipeline with command line exception handling.

    Args:
        options: The parsed OCR options.
        plugin_manager: The plugin manager to use. If not provided, one will be
            created.
    """
    return cli_exception_handler(_run_pipeline, options, plugin_manager)


def run_pipeline(
    options: OcrOptions,
    *,
    plugin_manager: OcrmypdfPluginManager,
) -> ExitCode:
    """Run the OCR pipeline without command line exception handling.

    Args:
        options: The parsed OCR options.
        plugin_manager: The plugin manager to use. If not provided, one will be
            created.
    """
    pass
