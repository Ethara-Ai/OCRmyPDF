# SPDX-FileCopyrightText: 2024 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""OCRmyPDF PDF annotation cleanup."""

from __future__ import annotations

import logging

from pikepdf import Dictionary, Name, NameTree, Pdf

log = logging.getLogger(__name__)


def remove_broken_goto_annotations(pdf: Pdf) -> bool:
    """Remove broken goto annotations from a PDF.

    If a PDF contains a GoTo Action that points to a named destination that does not
    exist, Ghostscript PDF/A conversion will fail. In any event, a named destination
    that is not defined is not useful.

    Args:
        pdf: Opened PDF file.

    Returns:
        bool: True if the file was modified, False if not.
    """
    pass
