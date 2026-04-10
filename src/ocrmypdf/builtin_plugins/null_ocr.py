# SPDX-FileCopyrightText: 2025 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Built-in plugin implementing a null OCR engine (no OCR).

This plugin provides an OCR engine that produces no text output. It is useful
when users want OCRmyPDF's image processing, PDF/A conversion, or optimization
features without performing actual OCR.

Usage:
    ocrmypdf --ocr-engine none input.pdf output.pdf
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image

from ocrmypdf import hookimpl
from ocrmypdf.hocrtransform import BoundingBox, OcrClass, OcrElement
from ocrmypdf.pluginspec import OcrEngine, OrientationConfidence

if TYPE_CHECKING:
    from ocrmypdf._options import OcrOptions


class NullOcrEngine(OcrEngine):
    """A no-op OCR engine that produces no text output.

    Use this when you want OCRmyPDF's image processing, PDF/A conversion,
    or optimization features without performing actual OCR.
    """

    @staticmethod
    def version() -> str:
        """Return version string."""
        return "none"

    @staticmethod
    def creator_tag(options: OcrOptions) -> str:
        """Return creator tag for PDF metadata."""
        pass

    def __str__(self) -> str:
        """Return human-readable engine name."""
        return "No OCR engine"

    @staticmethod
    def languages(options: OcrOptions) -> set[str]:
        """Return supported languages (empty set for null engine)."""
        return set()

    @staticmethod
    def get_orientation(input_file: Path, options: OcrOptions) -> OrientationConfidence:
        """Return neutral orientation (no rotation detected)."""
        pass

    @staticmethod
    def get_deskew(input_file: Path, options: OcrOptions) -> float:
        """Return zero deskew angle."""
        pass

    @staticmethod
    def supports_generate_ocr() -> bool:
        """Return True - this engine supports the generate_ocr() API."""
        pass

    @staticmethod
    def generate_ocr(
        input_file: Path,
        options: OcrOptions,
        page_number: int = 0,
    ) -> tuple[OcrElement, str]:
        """Generate empty OCR results.

        Args:
            input_file: The image file (used to get dimensions).
            options: OCR options (ignored).
            page_number: Page number (stored in result).

        Returns:
            A tuple of (empty OcrElement page, empty string).
        """
        pass

    @staticmethod
    def generate_hocr(
        input_file: Path,
        output_hocr: Path,
        output_text: Path,
        options: OcrOptions,
    ) -> None:
        """Generate empty hOCR file.

        Creates minimal valid hOCR output with no text content.
        """
        pass

    @staticmethod
    def generate_pdf(
        input_file: Path,
        output_pdf: Path,
        output_text: Path,
        options: OcrOptions,
    ) -> None:
        """NullOcrEngine cannot generate PDFs directly.

        Use pdf_renderer='fpdf2' instead of 'sandwich'.
        """
        raise NotImplementedError(
            "NullOcrEngine cannot generate PDFs directly. "
            "Use --pdf-renderer fpdf2 instead of sandwich mode."
        )


@hookimpl
def get_ocr_engine(options):
    """Return NullOcrEngine when --ocr-engine none is selected."""
    if options is not None:
        ocr_engine = getattr(options, 'ocr_engine', 'auto')
        if ocr_engine != 'none':
            return None
    return NullOcrEngine()
