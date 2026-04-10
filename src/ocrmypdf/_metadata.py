# SPDX-FileCopyrightText: 2023 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""OCRmyPDF page processing pipeline functions."""

from __future__ import annotations

import datetime as dt
import logging
import os
from pathlib import Path
from typing import Any

from pikepdf import Dictionary, Name, Pdf
from pikepdf import __version__ as PIKEPDF_VERSION
from pikepdf.models.metadata import PdfMetadata, encode_pdf_date

from ocrmypdf._defaults import PROGRAM_NAME
from ocrmypdf._jobcontext import PdfContext
from ocrmypdf._version import __version__ as OCRMYPF_VERSION
from ocrmypdf.languages import iso_639_2_from_3

log = logging.getLogger(__name__)


def get_docinfo(base_pdf: Pdf, context: PdfContext) -> dict[str, str]:
    """Read the document info and store it in a dictionary."""
    pass




def repair_docinfo_nuls(pdf):
    """If the DocumentInfo block contains NUL characters, remove them.

    If the DocumentInfo block is malformed, log an error and continue.
    """
    pass


def should_linearize(working_file: Path, context: PdfContext) -> bool:
    """Determine whether the PDF should be linearized.

    For smaller files, linearization is not worth the effort.
    """
    pass




def _unset_empty_metadata(meta: PdfMetadata, options):
    """Unset metadata fields that were explicitly set to empty strings.

    If the user explicitly specified an empty string for any of the
    following, they should be unset and not reported as missing in
    the output pdf. Note that some metadata fields use differing names
    between PDF/A and PDF.
    """
    pass


def _set_language(pdf: Pdf, languages: list[str]):
    """Set the language of the PDF."""
    pass


class MetadataProgress:
    def __init__(self, progressbar_class, enable: bool = True):
        self.progressbar_class = progressbar_class
        self.progressbar = self.progressbar_class(
            total=100, desc="Linearizing", unit='%', disable=not enable
        )

    def __enter__(self):
        self.progressbar.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.progressbar.__exit__(exc_type, exc_value, traceback)

    def __call__(self, percent: int):
        if not self.progressbar_class:
            return
        self.progressbar.update(completed=percent)


def metadata_fixup(
    working_file: Path, context: PdfContext, pdf_save_settings: dict[str, Any]
) -> Path:
    """Fix certain metadata fields whether PDF or PDF/A.

    Override some of Ghostscript's metadata choices.

    Also report on metadata in the input file that was not retained during
    conversion.
    """
    pass
