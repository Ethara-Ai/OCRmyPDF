#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Validate a work order from API or command line."""

from __future__ import annotations

import logging
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from shutil import copyfileobj

import pikepdf

from ocrmypdf._defaults import DEFAULT_ROTATE_PAGES_THRESHOLD
from ocrmypdf._exec import unpaper
from ocrmypdf._options import OcrOptions
from ocrmypdf._plugin_manager import OcrmypdfPluginManager
from ocrmypdf.exceptions import (
    BadArgsError,
    InputFileError,
    MissingDependencyError,
    OutputFileAccessError,
)
from ocrmypdf.helpers import (
    is_file_writable,
    running_in_docker,
    running_in_snap,
    safe_symlink,
)
from ocrmypdf.subprocess import check_external_program

log = logging.getLogger(__name__)


def check_platform() -> None:
    if sys.maxsize <= 2**32:  # pragma: no cover
        log.warning(
            "You are running OCRmyPDF in a 32-bit (x86) Python interpreter. "
            "This is not supported. 32-bit does not have enough address space "
            "to process large files. "
            "Please use a 64-bit (x86-64) version of Python."
        )


def check_options_languages(
    options: OcrOptions, ocr_engine_languages: list[str]
) -> None:
    # Check for blocked languages first, before checking if they're installed
    DENIED_LANGUAGES = {'equ', 'osd'}
    blocked = DENIED_LANGUAGES & set(options.languages)
    if blocked:
        raise BadArgsError(
            "The following languages are for Tesseract's internal use and "
            "should not be issued explicitly: "
            f"{', '.join(blocked)}\n"
            "Remove them from the -l/--language argument."
        )

    if not ocr_engine_languages:
        return

    missing_languages = set(options.languages) - set(ocr_engine_languages)
    if missing_languages:
        lang_text = '\n'.join(lang for lang in missing_languages)
        msg = (
            "OCR engine does not have language data for the following "
            "requested languages: \n"
            f"{lang_text}\n"
            "Please install the appropriate language data for your OCR engine.\n"
            "\n"
            "See the online documentation for instructions:\n"
            "    https://ocrmypdf.readthedocs.io/en/latest/languages.html\n"
            "\n"
            "Note: most languages are identified by a 3-letter ISO 639-2 Code.\n"
            "For example, English is 'eng', German is 'deu', and Spanish is 'spa'.\n"
            "Simplified Chinese is 'chi_sim' and Traditional Chinese is 'chi_tra'."
            "\n"
        )
        raise MissingDependencyError(msg)


def check_options_sidecar(options: OcrOptions) -> None:
    if options.sidecar == '\0':
        if options.output_file == '-':
            raise BadArgsError("--sidecar filename needed when output file is stdout.")
        elif options.output_file == os.devnull:
            raise BadArgsError(
                "--sidecar filename needed when output file is /dev/null or NUL."
            )
        options.sidecar = options.output_file + '.txt'
    if options.sidecar == options.input_file or options.sidecar == options.output_file:
        raise BadArgsError(
            "--sidecar file must be different from the input and output files"
        )


def check_options_preprocessing(options: OcrOptions) -> None:
    if options.clean_final:
        options.clean = True
    if options.unpaper_args and not options.clean:
        raise BadArgsError("--clean is required for --unpaper-args")
    if (
        options.rotate_pages_threshold != DEFAULT_ROTATE_PAGES_THRESHOLD
        and not options.rotate_pages
    ):
        raise BadArgsError("--rotate-pages is required for --rotate-pages-threshold")
    if options.clean:
        check_external_program(
            program='unpaper',
            package='unpaper',
            version_checker=unpaper.version,
            need_version='6.1',
            required_for="--clean, --clean-final",
        )


def _check_plugin_invariant_options(options: OcrOptions) -> None:
    check_platform()
    check_options_sidecar(options)
    check_options_preprocessing(options)


def _check_plugin_options(
    options: OcrOptions, plugin_manager: OcrmypdfPluginManager
) -> None:
    # First, let plugins check their external dependencies
    plugin_manager.check_options(options=options)

    # Then check OCR engine language support
    ocr_engine_languages = plugin_manager.get_ocr_engine(options=options).languages(
        options
    )
    check_options_languages(options, ocr_engine_languages)

    # Finally, run comprehensive validation using the coordinator
    from ocrmypdf._validation_coordinator import ValidationCoordinator

    coordinator = ValidationCoordinator(plugin_manager)
    coordinator.validate_all_options(options)


def check_options(options: OcrOptions, plugin_manager: OcrmypdfPluginManager) -> None:
    """Check options for validity and consistency.

    This function coordinates validation across the entire system:
    1. Core validation (platform, files, preprocessing)
    2. Plugin external dependency validation
    3. Plugin-specific validation (handled by plugin models)
    4. Cross-cutting validation (handled by validation coordinator)
    """
    _check_plugin_invariant_options(options)
    _check_plugin_options(options, plugin_manager)






