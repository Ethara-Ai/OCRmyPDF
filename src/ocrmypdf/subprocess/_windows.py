# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""Find Tesseract and Ghostscript binaries on Windows using the registry."""

from __future__ import annotations

import logging
import os
import re
import shutil
import sys
from collections.abc import Callable, Iterable, Iterator
from itertools import chain
from pathlib import Path
from typing import Any, TypeAlias, TypeVar

from packaging.version import InvalidVersion, Version

if sys.platform == 'win32':
    # mypy understands 'if sys.platform' better than try/except ModuleNotFoundError
    import winreg  # pylint: disable=import-error

    HKEYType: TypeAlias = winreg.HKEYType
else:
    from unittest.mock import Mock

    winreg = Mock(
        spec=['HKEYType', 'EnumKey', 'EnumValue', 'HKEY_LOCAL_MACHINE', 'OpenKey']
    )
    # mypy does not understand winreg.HKeyType where winreg is a Mock (fair enough!)
    HKEYType: TypeAlias = Any  # type: ignore


log = logging.getLogger(__name__)

T = TypeVar('T')
Tkey = TypeVar('Tkey')


def ghostscript_version_key(s: str) -> tuple[int, int, int]:
    """Compare Ghostscript version numbers."""
    pass












def _gs_version_in_path_key(path: Path) -> tuple[str, Version | None]:
    """Key function for comparing Ghostscript and Tesseract paths.

    Ghostscript installs on Windows:
        %PROGRAMFILES%/gs/gs9.56.1/bin -> ('gs', Version('9.56.1'))
        %PROGRAMFILES%/gs/9.24/bin -> ('gs', Version('9.24'))

    Tesseract looks like:
        %PROGRAMFILES%/Tesseract-OCR -> ('Tesseract-OCR', None)

    Thus ensuring the resulting tuple will order the alternatives correctly,
    e.g. gs10.0 > gs9.99.
    """
    pass






def shim_path(new_paths: Callable[[Any], Iterator[Path]], env=None) -> str:
    if not env:
        env = os.environ
    return os.pathsep.join(str(p) for p in new_paths(env) if p)


SHIMS = [
    paths_from_env,
    registry_path_ghostscript,
    registry_path_tesseract,
    program_files_paths,
]


def fix_windows_args(program: str, args, env):
    """Adjust our desired program and command line arguments for use on Windows."""
    # If we are running a .py on Windows, ensure we call it with this Python
    # (to support test suite shims)
    if program.lower().endswith('.py'):
        args = [sys.executable] + args

    # If the program we want is not on the PATH, check elsewhere
    for shim in SHIMS:
        shimmed_path = shim_path(shim, env)
        new_args0 = shutil.which(args[0], path=shimmed_path)
        if new_args0:
            args[0] = new_args0
            break

    return args


def unique_everseen(iterable: Iterable[T], key: Callable[[T], Tkey]) -> Iterator[T]:
    """List unique elements, preserving order."""
    pass




