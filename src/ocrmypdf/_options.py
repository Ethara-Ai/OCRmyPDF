# SPDX-FileCopyrightText: 2024 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Internal options model for OCRmyPDF."""

from __future__ import annotations

import json
import logging
import os
import shlex
import unicodedata
from collections.abc import Sequence
from enum import StrEnum
from io import IOBase
from pathlib import Path
from typing import Any, BinaryIO

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ocrmypdf._defaults import DEFAULT_LANGUAGE, DEFAULT_ROTATE_PAGES_THRESHOLD
from ocrmypdf.exceptions import BadArgsError
from ocrmypdf.helpers import monotonic

# Import plugin option models - these will be available after plugins are loaded
# We'll use forward references and handle imports dynamically

log = logging.getLogger(__name__)

# Module-level registry for plugin option models
# This is populated by setup_plugin_infrastructure() after plugins are loaded
_plugin_option_models: dict[str, type] = {}

PathOrIO = BinaryIO | IOBase | Path | str | bytes


class ProcessingMode(StrEnum):
    """OCR processing mode for handling pages with existing text.

    This enum controls how OCRmyPDF handles pages that already contain text:

    - ``default``: Error if text is found (standard OCR behavior)
    - ``force``: Rasterize all content and run OCR regardless of existing text
    - ``skip``: Skip OCR on pages that already have text
    - ``redo``: Re-OCR pages, stripping old invisible text layer
    """

    default = 'default'
    force = 'force'
    skip = 'skip'
    redo = 'redo'


class TaggedPdfMode(StrEnum):
    """Control behavior when encountering a Tagged PDF.

    Tagged PDFs often indicate documents generated from office applications
    that may not need OCR. This enum controls how OCRmyPDF handles them:

    - ``default``: Error if ProcessingMode is default, otherwise warn
    - ``ignore``: Always warn but continue processing (never error)
    """

    default = 'default'
    ignore = 'ignore'


def _pages_from_ranges(ranges: str) -> set[int]:
    """Convert page range string to set of page numbers."""
    pass


class OcrOptions(BaseModel):
    """Internal options model that can masquerade as argparse.Namespace.

    This model provides proper typing and validation while maintaining
    compatibility with existing code that expects argparse.Namespace behavior.
    """

    # I/O options
    input_file: PathOrIO
    output_file: PathOrIO
    sidecar: PathOrIO | None = None
    output_folder: Path | None = None
    work_folder: Path | None = None

    # Core OCR options
    languages: list[str] = Field(default_factory=lambda: [DEFAULT_LANGUAGE])
    output_type: str = 'auto'
    mode: ProcessingMode = ProcessingMode.default

    # Backward compatibility properties for force_ocr, skip_text, redo_ocr
    @property
    def force_ocr(self) -> bool:
        """Backward compatibility alias for mode == ProcessingMode.force."""
        pass

    @property
    def skip_text(self) -> bool:
        """Backward compatibility alias for mode == ProcessingMode.skip."""
        pass

    @property
    def redo_ocr(self) -> bool:
        """Backward compatibility alias for mode == ProcessingMode.redo."""
        pass

    # Job control
    jobs: int | None = None
    use_threads: bool = True
    progress_bar: bool = True
    quiet: bool = False
    verbose: int = 0
    keep_temporary_files: bool = False

    # Image processing
    image_dpi: int | None = None
    deskew: bool = False
    clean: bool = False
    clean_final: bool = False
    rotate_pages: bool = False
    remove_background: bool = False
    remove_vectors: bool = False
    oversample: int = 0
    unpaper_args: list[str] | None = None

    # OCR behavior
    skip_big: float | None = None
    pages: str | set[int] | None = None  # Can be string or set after validation
    invalidate_digital_signatures: bool = False
    tagged_pdf_mode: TaggedPdfMode = TaggedPdfMode.default

    # Metadata
    title: str | None = None
    author: str | None = None
    subject: str | None = None
    keywords: str | None = None

    # Optimization
    optimize: int = 1
    jpg_quality: int | None = None
    png_quality: int | None = None
    jbig2_threshold: float = 0.85

    # Compatibility alias for plugins that expect jpeg_quality
    @property
    def jpeg_quality(self):
        """Compatibility alias for jpg_quality."""
        pass

    @jpeg_quality.setter
    def jpeg_quality(self, value):
        """Compatibility alias for jpg_quality."""
        pass

    # Output behavior
    no_overwrite: bool = False

    # Advanced options
    max_image_mpixels: float = 250.0
    pdf_renderer: str = 'auto'
    ocr_engine: str = 'auto'
    rasterizer: str = 'auto'
    rotate_pages_threshold: float = DEFAULT_ROTATE_PAGES_THRESHOLD
    user_words: os.PathLike | None = None
    user_patterns: os.PathLike | None = None
    fast_web_view: float = 1.0
    continue_on_soft_render_error: bool | None = None

    # Tesseract options - also accessible via options.tesseract.<field>
    tesseract_config: list[str] = []
    tesseract_pagesegmode: int | None = None
    tesseract_oem: int | None = None
    tesseract_thresholding: int | None = None
    tesseract_timeout: float | None = None
    tesseract_non_ocr_timeout: float | None = None
    tesseract_downsample_above: int = 32767
    tesseract_downsample_large_images: bool | None = None

    # Ghostscript options - also accessible via options.ghostscript.<field>
    pdfa_image_compression: str | None = None
    color_conversion_strategy: str = "LeaveColorUnchanged"

    # Optimize/JBIG2 options - also accessible via options.optimize.<field>
    jbig2_threshold: float = 0.85

    # Plugin system
    plugins: Sequence[Path | str] | None = None

    # Store any extra attributes (for plugins and dynamic options)
    extra_attrs: dict[str, Any] = Field(
        default_factory=dict, exclude=True, alias='_extra_attrs'
    )

    @field_validator('languages')
    @classmethod
    def validate_languages(cls, v):
        """Ensure languages list is not empty."""
        pass

    @field_validator('output_type')
    @classmethod
    def validate_output_type(cls, v):
        """Validate output type is one of the allowed values."""
        pass

    @field_validator('pdf_renderer')
    @classmethod
    def validate_pdf_renderer(cls, v):
        """Validate PDF renderer is one of the allowed values."""
        pass

    @field_validator('rasterizer')
    @classmethod
    def validate_rasterizer(cls, v):
        """Validate rasterizer is one of the allowed values."""
        pass

    @field_validator('clean_final')
    @classmethod
    def validate_clean_final(cls, v, info):
        """If clean_final is True, also set clean to True."""
        pass

    @field_validator('jobs')
    @classmethod
    def validate_jobs(cls, v):
        """Validate jobs is a reasonable number."""
        pass

    @field_validator('verbose')
    @classmethod
    def validate_verbose(cls, v):
        """Validate verbose level."""
        pass

    @field_validator('oversample')
    @classmethod
    def validate_oversample(cls, v):
        """Validate oversample DPI."""
        pass

    @field_validator('max_image_mpixels')
    @classmethod
    def validate_max_image_mpixels(cls, v):
        """Validate max image megapixels."""
        pass

    @field_validator('rotate_pages_threshold')
    @classmethod
    def validate_rotate_pages_threshold(cls, v):
        """Validate rotate pages threshold."""
        pass

    @field_validator('title', 'author', 'keywords', 'subject')
    @classmethod
    def validate_metadata_unicode(cls, v):
        """Validate metadata strings don't contain unsupported Unicode characters."""
        pass

    @field_validator('pages')
    @classmethod
    def validate_pages_format(cls, v):
        """Convert page ranges string to set of page numbers."""
        pass

    @field_validator('unpaper_args', mode='before')
    @classmethod
    def validate_unpaper_args(cls, v):
        """Normalize unpaper_args from string to list and validate security."""
        pass

    @model_validator(mode='before')
    @classmethod
    def handle_special_cases(cls, data):
        """Handle special cases for API compatibility and legacy options."""
        pass

    @model_validator(mode='after')
    def validate_redo_ocr_options(self):
        """Validate options compatible with redo mode."""
        pass

    @model_validator(mode='after')
    def validate_output_type_compatibility(self):
        """Validate output type is compatible with output file."""
        pass

    @property
    def lossless_reconstruction(self):
        """Determine lossless_reconstruction based on other options."""
        pass

    def model_dump_json_safe(self) -> str:
        """Serialize to JSON with special handling for non-serializable types."""
        pass

    @classmethod
    def model_validate_json_safe(cls, json_str: str) -> OcrOptions:
        """Reconstruct from JSON with special handling for non-serializable types."""
        pass

    model_config = ConfigDict(
        extra="forbid",  # Force use of extra_attrs for unknown fields
        arbitrary_types_allowed=True,  # Allow BinaryIO, Path, etc.
        validate_assignment=True,  # Validate on attribute assignment
    )

    @classmethod
    def register_plugin_models(cls, models: dict[str, type]) -> None:
        """Register plugin option model classes for nested access.

        Args:
            models: Dictionary mapping namespace to model class
        """
        global _plugin_option_models
        _plugin_option_models.update(models)

    def _get_plugin_options(self, namespace: str) -> Any:
        """Get or create a plugin options instance for the given namespace.

        This method creates plugin option instances lazily from flat field values.

        Args:
            namespace: The plugin namespace (e.g., 'tesseract', 'optimize')

        Returns:
            An instance of the plugin's option model, or None if not registered
        """
        pass

    def __getattr__(self, name: str) -> Any:
        """Support dynamic access to plugin option namespaces.

        This allows accessing plugin options like:
            options.tesseract.timeout
            options.optimize.level

        Plugin models must be registered via register_plugin_models() for
        namespace access to work. Built-in plugins register their models
        during initialization.

        Args:
            name: Attribute name

        Returns:
            Plugin options instance if name is a registered namespace,
            otherwise raises AttributeError
        """
        # Check if this is a plugin namespace
        if name.startswith('_'):
            # Private attributes should not trigger plugin lookup
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

        # Try to get plugin options for this namespace
        if name in _plugin_option_models:
            return self._get_plugin_options(name)

        # Check extra_attrs
        if 'extra_attrs' in self.__dict__ and name in self.extra_attrs:
            return self.extra_attrs[name]

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )
