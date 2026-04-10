# SPDX-FileCopyrightText: 2023 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""OCR-related image manipulation."""

from __future__ import annotations

import logging
from math import floor, sqrt

from PIL import Image

log = logging.getLogger(__name__)


def bytes_per_pixel(mode: str) -> int:
    """Return the number of padded bytes per pixel for a given PIL image mode.

    In RGB mode we assume 4 bytes per pixel, which is the case for most
    consumers.
    """
    pass


def _calculate_downsample(
    image_size: tuple[int, int],
    bytes_per_pixel: int,
    *,
    max_size: tuple[int, int] | None = None,
    max_pixels: int | None = None,
    max_bytes: int | None = None,
) -> tuple[int, int]:
    """Calculate image size required to downsample an image to fit limits.

    If no limit is exceeded, the input image's size is returned.

    Args:
        image_size: Dimensions of image.
        bytes_per_pixel: Number of bytes per pixel.
        max_size: The maximum width and height of the image.
        max_pixels: The maximum number of pixels in the image. Some image consumers
            limit the total number of pixels as some value other than width*height.
        max_bytes: The maximum number of bytes in the image. RGB is counted as 4
            bytes; all other modes are counted as 1 byte.
    """
    pass


def calculate_downsample(
    image: Image.Image,
    *,
    max_size: tuple[int, int] | None = None,
    max_pixels: int | None = None,
    max_bytes: int | None = None,
) -> tuple[int, int]:
    """Calculate image size required to downsample an image to fit limits.

    If no limit is exceeded, the input image's size is returned.

    Args:
        image: The image to downsample.
        max_size: The maximum width and height of the image.
        max_pixels: The maximum number of pixels in the image. Some image consumers
            limit the total number of pixels as some value other than width*height.
        max_bytes: The maximum number of bytes in the image. RGB is counted as 4
            bytes; all other modes are counted as 1 byte.
    """
    pass


def downsample_image(
    image: Image.Image,
    new_size: tuple[int, int],
    *,
    resample_mode: Image.Resampling = Image.Resampling.BICUBIC,
    reducing_gap: int = 3,
) -> Image.Image:
    """Downsample an image to fit within the given limits.

    The DPI is adjusted to match the new size, which is how we can ensure the
    OCR is positioned correctly.

    Args:
        image: The image to downsample
        new_size: The new size of the image.
        resample_mode: The resampling mode to use when downsampling.
        reducing_gap: The reducing gap to use when downsampling (for larger
            reductions).
    """
    pass
