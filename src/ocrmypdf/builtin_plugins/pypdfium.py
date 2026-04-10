# SPDX-FileCopyrightText: 2025 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""Built-in plugin to implement PDF page rasterization using pypdfium2."""

from __future__ import annotations

import logging
import threading
from contextlib import closing
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import pypdfium2 as pdfium
else:
    try:
        import pypdfium2 as pdfium
    except ImportError:
        pdfium = None
from PIL import Image

from ocrmypdf import hookimpl
from ocrmypdf.exceptions import MissingDependencyError
from ocrmypdf.helpers import Resolution

log = logging.getLogger(__name__)

# pypdfium2/PDFium is not thread-safe. All calls to the library must be serialized.
# See: https://pypdfium2.readthedocs.io/en/stable/python_api.html#incompatibility-with-threading
# When using process-based parallelism (use_threads=False), each process has its own
# pdfium instance, so locking is not needed across processes.
_pdfium_lock = threading.Lock()


@hookimpl
def check_options(options):
    """Check that pypdfium2 is available if explicitly requested."""
    if options.rasterizer == 'pypdfium' and pdfium is None:
        raise MissingDependencyError(
            "The --rasterizer pypdfium option requires the pypdfium2 package. "
            "Install it with: pip install pypdfium2"
        )


def _open_pdf_document(input_file: Path):
    """Open a PDF document using pypdfium2."""
    pass


def _calculate_mediabox_crop(page) -> tuple[float, float, float, float]:
    """Calculate crop values to expand rendering from CropBox to MediaBox.

    By default pypdfium2 renders to the CropBox. To render the full MediaBox,
    we need negative crop values to expand the rendering area.

    Returns:
        Tuple of (left, bottom, right, top) crop values. Negative values
        expand the rendering area beyond the CropBox to the MediaBox.
    """
    pass


def _render_page_to_bitmap(
    page: pdfium.PdfPage,
    raster_device: str,
    raster_dpi: Resolution,
    rotation: int | None,
    use_cropbox: bool,
) -> tuple[pdfium.PdfBitmap, int, int]:
    """Render a PDF page to a bitmap."""
    pass


def _process_image_for_output(
    pil_image: Image.Image,
    raster_device: str,
    raster_dpi: Resolution,
    page_dpi: Resolution | None,
    stop_on_soft_error: bool,
    expected_width: int | None = None,
    expected_height: int | None = None,
) -> tuple[Image.Image, Literal['PNG', 'TIFF', 'JPEG']]:
    """Process PIL image for output format and set DPI metadata."""
    pass


def _save_image(pil_image: Image.Image, output_file: Path, format_name: str) -> None:
    """Save PIL image to file with appropriate DPI metadata."""
    pass


@hookimpl
def rasterize_pdf_page(
    input_file: Path,
    output_file: Path,
    raster_device: str,
    raster_dpi: Resolution,
    pageno: int,
    page_dpi: Resolution | None,
    rotation: int | None,
    filter_vector: bool,
    stop_on_soft_error: bool,
    options,
    use_cropbox: bool,
) -> Path | None:
    """Rasterize a single page of a PDF file using pypdfium2.

    Returns None if pypdfium2 is not available or if the user has selected
    a different rasterizer, allowing Ghostscript to be used.
    """
    pass
