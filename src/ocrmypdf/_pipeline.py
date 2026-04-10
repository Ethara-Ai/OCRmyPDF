# SPDX-FileCopyrightText: 2018-2022 James R. Barlow
# SPDX-FileCopyrightText: 2019 Martin Wind
# SPDX-License-Identifier: MPL-2.0

"""OCRmyPDF page processing pipeline functions."""

from __future__ import annotations

import logging
import os
import re
import sys
from collections.abc import Iterable, Iterator, Sequence
from contextlib import suppress
from io import BytesIO
from pathlib import Path
from shutil import copyfileobj
from typing import TYPE_CHECKING, Any, BinaryIO, TypeVar, cast

if TYPE_CHECKING:
    from ocrmypdf.hocrtransform import OcrElement

import img2pdf
import pikepdf
from PIL import Image, ImageColor, ImageDraw

from ocrmypdf._concurrent import Executor
from ocrmypdf._exec import unpaper
from ocrmypdf._jobcontext import PageContext, PdfContext
from ocrmypdf._metadata import repair_docinfo_nuls
from ocrmypdf._options import OcrOptions, ProcessingMode, TaggedPdfMode
from ocrmypdf.exceptions import (
    DigitalSignatureError,
    DpiError,
    EncryptedPdfError,
    InputFileError,
    PriorOcrFoundError,
    TaggedPDFError,
    UnsupportedImageFormatError,
)
from ocrmypdf.helpers import IMG2PDF_KWARGS, Resolution, safe_symlink
from ocrmypdf.pdfa import (
    file_claims_pdfa,
    generate_pdfa_ps,
    speculative_pdfa_conversion,
)
from ocrmypdf.pdfinfo import Colorspace, Encoding, FloatRect, PageInfo, PdfInfo
from ocrmypdf.pluginspec import GhostscriptRasterDevice, OrientationConfidence

try:
    from pi_heif import register_heif_opener
except ImportError:

    def register_heif_opener():
        pass


T = TypeVar("T")
log = logging.getLogger(__name__)

VECTOR_PAGE_DPI = 400


register_heif_opener()


def triage_image_file(input_file: Path, output_file: Path, options: OcrOptions) -> None:
    """Triage the input image file.

    If the input file is an image, check its resolution and convert it to PDF.

    Args:
        input_file: The path to the input file.
        output_file: The path to the output file.
        options: An object containing the options passed to the OCRmyPDF command.

    Raises:
        UnsupportedImageFormatError: If the input file is not a supported image format.
        DpiError: If the input image has no resolution (DPI) in its metadata or if the
            resolution is not credible.
    """
    pass


def _pdf_guess_version(input_file: Path, search_window=1024) -> str:
    """Try to find version signature at start of file.

    Not robust enough to deal with appended files.

    Returns empty string if not found, indicating file is probably not PDF.
    """
    pass


def triage(
    original_filename: str, input_file: Path, output_file: Path, options: OcrOptions
) -> Path:
    """Triage the input file. We can handle PDFs and images."""
    pass


def get_pdfinfo(
    input_file,
    *,
    executor: Executor,
    detailed_analysis: bool = False,
    progbar: bool = False,
    max_workers: int | None = None,
    use_threads: bool = True,
    check_pages=None,
) -> PdfInfo:
    """Get the PDF info."""
    pass


def validate_pdfinfo_options(context: PdfContext) -> None:
    """Validate the PDF info options."""
    pass


def _vector_page_dpi(pageinfo: PageInfo) -> int:
    """Get a DPI to use for vector pages, if the page has vector content."""
    pass


def get_page_square_dpi(
    page_context: PageContext, image_dpi: Resolution | None = None
) -> Resolution:
    """Get the DPI when we require xres == yres, scaled to physical units.

    Page DPI includes UserUnit scaling.
    """
    pass


def get_canvas_square_dpi(
    page_context: PageContext, image_dpi: Resolution | None = None
) -> Resolution:
    """Get the DPI when we require xres == yres, in Postscript units.

    Canvas DPI is independent of PDF UserUnit scaling, which is
    used to describe situations where the PDF user space is not 1:1 with
    the physical units of the page.
    """
    pass


def is_ocr_required(page_context: PageContext) -> bool:
    """Check if the page needs to be OCR'd."""
    pass


def rasterize_preview(input_file: Path, page_context: PageContext) -> Path:
    """Generate a lower quality preview image."""
    pass


def describe_rotation(
    page_context: PageContext, orient_conf: OrientationConfidence, correction: int
) -> str:
    """Describe the page rotation we are going to perform (or not perform)."""
    pass


def get_orientation_correction(preview: Path, page_context: PageContext) -> int:
    """Work out orientation correction for each page.

    We ask Ghostscript to draw a preview page, which will rasterize with the
    current /Rotate applied, and then ask OCR which way the page is
    oriented. If the value of /Rotate is correct (e.g., a user already
    manually fixed rotation), then OCR will say the page is pointing
    up and the correction is zero. Otherwise, the orientation found by
    OCR represents the clockwise rotation, or the counterclockwise
    correction to rotation.

    When we draw the real page for OCR, we rotate it by the CCW correction,
    which points it (hopefully) upright. _graft.py takes care of the orienting
    the image and text layers.
    """
    pass


def calculate_image_dpi(page_context: PageContext) -> Resolution:
    """Calculate the DPI for the page image."""
    pass


def calculate_raster_dpi(page_context: PageContext):
    """Calculate the DPI for rasterization."""
    pass


def rasterize(
    input_file: Path,
    page_context: PageContext,
    correction: int = 0,
    output_tag: str = '',
    remove_vectors: bool | None = None,
) -> Path:
    """Rasterize a PDF page to a PNG image.

    Args:
        input_file: The input PDF file path.
        page_context: The page context object.
        correction: The orientation correction angle. Defaults to 0.
        output_tag: The output tag. Defaults to ''.
        remove_vectors: Whether to remove vectors. Defaults to None, which means
            the value from the page context options will be used. If the value
            is True or False, it will override the page context options.

    Returns:
        Path: The output PNG file path.
    """
    pass


def preprocess_remove_background(input_file: Path, page_context: PageContext) -> Path:
    """Remove the background from the input image (temporarily disabled)."""
    pass


def preprocess_deskew(input_file: Path, page_context: PageContext) -> Path:
    """Deskews the input image using the OCR engine and saves the output to a file.

    Args:
        input_file: The input image file to deskew.
        page_context: The context of the page being processed.

    Returns:
        Path: The path to the deskewed image file.
    """
    pass


def preprocess_clean(input_file: Path, page_context: PageContext) -> Path:
    """Clean the input image using unpaper."""
    pass


def create_ocr_image(image: Path, page_context: PageContext) -> Path:
    """Create the image we send for OCR.

    Might not be the same as the display image depending on preprocessing.
    This image will never be shown to the user.
    """
    pass


def ocr_engine_hocr(input_file: Path, page_context: PageContext) -> tuple[Path, Path]:
    """Run the OCR engine and generate hOCR output."""
    pass


def ocr_engine_direct(
    input_file: Path, page_context: PageContext
) -> tuple[OcrElement, Path]:
    """Run the OCR engine and return OcrElement tree directly.

    This is the modern path for OCR engines that support the generate_ocr() API.
    It bypasses hOCR file generation for better performance and richer data.

    Args:
        input_file: The image file to OCR.
        page_context: The page context with options and path utilities.

    Returns:
        A tuple of (OcrElement tree, path to text sidecar file).
    """
    pass


def should_visible_page_image_use_jpg(pageinfo: PageInfo) -> bool:
    """Determines whether the visible page image should be saved as a JPEG.

    If all images were JPEGs originally (including FlateDecode+DCTDecode),
    permit a JPEG as output.

    Args:
        pageinfo: The PageInfo object containing information about the page.

    Returns:
        A boolean indicating whether the visible page image should be saved as a JPEG.
    """
    pass


def create_visible_page_jpg(image: Path, page_context: PageContext) -> Path:
    """Create a visible page image in JPEG format.

    This is intended to be used when all images on the page were originally JPEGs.
    """
    pass


def create_pdf_page_from_image(
    image: Path, page_context: PageContext, orientation_correction: int
) -> Path:
    """Create a PDF page from a page image."""
    pass


def ocr_engine_textonly_pdf(
    input_image: Path, page_context: PageContext
) -> tuple[Path, Path]:
    """Run the OCR engine and generate a text-only PDF (will look blank)."""
    pass


def _offset_rect(rect: tuple[float, float, float, float], offset: tuple[float, float]):
    """Offset a rectangle by a given amount."""
    pass




def fix_pagepdf_boxes(
    infile: Path | BinaryIO,
    out_file: Path,
    page_context: PageContext,
    swap_axis: bool = False,
) -> Path:
    """Fix the bounding boxes in a single page PDF.

    The single page PDF is created with a normal MediaBox with its lower left corner
    at (0, 0). infile is the single page PDF. page_context.mediabox has the original
    file's mediabox, which may have a different origin. We need to adjust the other
    boxes in the single page PDF to match the effect they had on the original page.

    When correcting page rotation, we create a single page PDF that is correctly
    rotated instead of an incorrectly rotated and then setting page.Rotate on it.
    If rotation is either 90 or 270 degrees, then this function can be called
    with swap_axis to swap the X and Y coordinates of all the boxes.

    We are not concerned with solving degenerate cases where the boxes overlap or
    or express invalid rectangles. We merely pass the boxes, producing a
    transformation equivalent to the change made by constructing a new page image.
    """
    pass


def generate_postscript_stub(context: PdfContext) -> Path:
    """Generates a PostScript file stub for the given PDF context.

    Args:
        context: The PDF context to generate the PostScript file stub for.

    Returns:
        Path: The path to the generated PostScript file stub.
    """
    pass


def convert_to_pdfa(input_pdf: Path, input_ps_stub: Path, context: PdfContext) -> Path:
    """Converts the given PDF to PDF/A.

    Args:
        input_pdf: The input PDF file path (presumably not PDF/A).
        input_ps_stub: The input PostScript file path, containing instructions
            for the PDF/A generator to use.
        context: The PDF context.
    """
    pass


def try_speculative_pdfa(input_pdf: Path, context: PdfContext) -> Path | None:
    """Try speculative PDF/A conversion with verapdf validation.

    This attempts a fast PDF/A conversion by adding PDF/A structures
    directly with pikepdf, then validating with verapdf. If validation
    passes, returns the converted file. If it fails or verapdf is not
    available, returns None to signal that Ghostscript should be used.

    Args:
        input_pdf: Path to the PDF to convert
        context: The PDF context

    Returns:
        Path to valid PDF/A file, or None if speculative conversion failed
    """
    pass


def try_auto_pdfa(input_pdf: Path, context: PdfContext) -> tuple[Path, str]:
    """Best-effort PDF/A for 'auto' output type.

    This function attempts to produce PDF/A without requiring Ghostscript:
    1. If verapdf is available, tries speculative conversion with validation
    2. Without verapdf, passes through as PDF/A if safe (input already PDF/A
       or force-ocr was used)
    3. Falls back to regular PDF if neither condition is met

    Args:
        input_pdf: Path to the PDF to convert
        context: The PDF context

    Returns:
        Tuple of (output_path, actual_output_type) where actual_output_type
        is 'pdfa' if PDF/A was achieved, 'pdf' otherwise
    """
    pass


def _is_safe_pdfa(input_pdf: Path, options) -> bool:
    """Check if file can be considered PDF/A without validation.

    These are cases where our modifications don't break PDF/A compliance:
    1. Input already claims PDF/A (we just grafted OCR text onto it)
    2. We used force-ocr (we rewrote the entire PDF from scratch)

    Args:
        input_pdf: Path to the PDF to check
        options: OCR options

    Returns:
        True if file can safely be considered PDF/A
    """
    pass


def should_linearize(working_file: Path, context: PdfContext) -> bool:
    """Determine whether the PDF should be linearized.

    For smaller files, linearization is not worth the effort.
    """
    pass


def get_pdf_save_settings(output_type: str) -> dict[str, Any]:
    """Get pikepdf.Pdf.save settings for the given output type.

    Essentially, don't use features that are incompatible with a given
    PDF/A specification.
    """
    pass


def _file_size_ratio(
    input_file: Path, output_file: Path
) -> tuple[float | None, float | None]:
    """Calculate ratio of input to output file sizes and percentage savings.

    Args:
        input_file (Path): The path to the input file.
        output_file (Path): The path to the output file.

    Returns:
        tuple[float | None, float | None]: A tuple containing the file size
        ratio and the percentage savings achieved by the output file size
        compared to the input file size.
    """
    pass


def optimize_pdf(
    input_file: Path, context: PdfContext, executor: Executor
) -> tuple[Path, Sequence[str]]:
    """Optimize the given PDF file."""
    pass


def enumerate_compress_ranges(
    iterable: Iterable[T],
) -> Iterator[tuple[tuple[int, int], T | None]]:
    """Enumerate the ranges of non-empty elements in an iterable.

    Compresses consecutive ranges of length 1 into single elements.

    Args:
        iterable: An iterable of elements to enumerate.

    Yields:
        A tuple containing a range of indices and the corresponding element.
        If the element is None, the range represents a skipped range of indices.
    """
    pass


def merge_sidecars(txt_files: Iterable[Path | None], context: PdfContext) -> Path:
    """Merge the page sidecar files into a single file.

    Sidecar files are created by the OCR engine and contain the text for each
    page in the PDF. This function merges the sidecar files into a single file
    and returns the path to the merged file.
    """
    pass


def copy_final(
    input_file: Path, output_file: str | Path | BinaryIO, original_file: Path | None
) -> None:
    """Copy the final temporary file to the output destination.

    Args:
        input_file (Path): The intermediate input file to copy.
        output_file (str | Path | BinaryIO): The output file to copy to.
        original_file: The original file to copy attributes from.

    Returns:
        None
    """
    pass
