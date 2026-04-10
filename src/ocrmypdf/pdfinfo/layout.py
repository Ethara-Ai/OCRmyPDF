# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""Detailed text position and layout analysis, building on pdfminer.six."""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from math import copysign
from os import PathLike
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pdfminer
import pdfminer.encodingdb
import pdfminer.pdfdevice
import pdfminer.pdfinterp
import pdfminer.psparser
from deprecation import deprecated
from pdfminer.converter import PDFLayoutAnalyzer
from pdfminer.layout import LAParams, LTChar, LTPage, LTTextBox
from pdfminer.pdfcolor import PDFColorSpace
from pdfminer.pdfdevice import PDFTextSeq
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdffont import FontWidthDict, PDFFont, PDFSimpleFont, PDFUnicodeNotDefined
from pdfminer.pdfinterp import PDFGraphicState, PDFResourceManager, PDFTextState
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import Matrix, bbox2str, matrix2str

from ocrmypdf.exceptions import EncryptedPdfError, InputFileError

STRIP_NAME = re.compile(r'[0-9]+')


original_pdfsimplefont_init = PDFSimpleFont.__init__


def pdfsimplefont__init__(
    self,
    descriptor: Mapping[str, Any],
    widths: FontWidthDict,
    spec: Mapping[str, Any],
) -> None:
    """Monkeypatch pdfminer.six PDFSimpleFont.__init__.

    If there is no ToUnicode and no Encoding, pdfminer.six assumes that Unicode
    conversion is possible. This is incorrect, according to PDF Reference Manual
    9.10.2. This patch fixes that.
    """
    pass


PDFSimpleFont.__init__ = pdfsimplefont__init__

# Patch pdfminer.six buffer size
# The parser doesn't properly handle keyword tokens are split across the end of the
# buffer, so increase the buffer size something far larger than will ever be seen.
pdfminer.psparser.PSBaseParser.BUFSIZ = 256 * 1024 * 1024


def pdftype3font__pscript5_get_height(self):
    """Monkeypatch for PScript5.dll PDFs.

    The height of Type3 fonts is known to be incorrect in PScript5.dll
    generated PDFs. This patch attempts to correct the height by
    using the bbox height if it is available, otherwise using the
    ascent and descent.
    """
    pass


def pdftype3font__pscript5_get_descent(self):
    """Monkeypatch for PScript5.dll PDFs.

    The descent of Type3 fonts is known to be incorrect in PScript5.dll
    generated PDFs. This patch attempts to correct the descent by
    using the vscale.
    """
    pass


def pdftype3font__pscript5_get_ascent(self):
    """Monkeypatch for PScript5.dll PDFs.

    The ascent of Type3 fonts is known to be incorrect in PScript5.dll
    generated PDFs. This patch attempts to correct the ascent by
    using the vscale.
    """
    pass


def _is_undefined_char(s: str) -> bool:
    """Check if a string is an undefined character."""
    pass


class LTStateAwareChar(LTChar):
    """A subclass of LTChar that tracks text render mode at time of drawing."""

    __slots__ = (
        'rendermode',
        '_text',
        'matrix',
        'fontname',
        'adv',
        'upright',
        'size',
        'width',
        'height',
        'bbox',
        'x0',
        'x1',
        'y0',
        'y1',
    )

    def __init__(
        self,
        matrix: Matrix,
        font: PDFFont,
        fontsize: float,
        scaling: float,
        rise: float,
        text: str,
        textwidth: float,
        textdisp: float | tuple[float | None, float],
        ncs: PDFColorSpace,
        graphicstate: PDFGraphicState,
        textstate: PDFTextState,
    ) -> None:
        """Initialize."""
        super().__init__(
            matrix,
            font,
            fontsize,
            scaling,
            rise,
            text,
            textwidth,
            textdisp,
            ncs,
            graphicstate,
        )
        self.rendermode = textstate.render

    def is_compatible(self, obj: object) -> bool:
        """Check if characters can be combined into a textline.

        We consider characters compatible if:
            - the Unicode mapping is known, and both have the same render mode
            - the Unicode mapping is unknown but both are part of the same font
        """
        pass

    def get_text(self) -> str:
        """Get text from this character."""
        pass

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        return (
            f"<{self.__class__.__name__} "
            f"{bbox2str(self.bbox)} "
            f"matrix={matrix2str(self.matrix)} "
            f"rendermode={self.rendermode!r} "
            f"font={self.fontname!r} "
            f"adv={self.adv} "
            f"text={self.get_text()!r}>"
        )


class TextPositionTracker(PDFLayoutAnalyzer):
    """A page layout analyzer that pays attention to text visibility."""

    textstate: PDFTextState

    def __init__(
        self,
        rsrcmgr: PDFResourceManager,
        pageno: int = 1,
        laparams: LAParams | None = None,
    ):
        """Initialize the layout analyzer."""
        super().__init__(rsrcmgr, pageno, laparams)
        self.result: LTPage | None = None

    def begin_page(self, page: PDFPage, ctm: Matrix) -> None:
        """Begin processing of a page."""
        pass

    def end_page(self, page: PDFPage) -> None:
        """End processing of a page."""
        pass

    def render_string(
        self,
        textstate: PDFTextState,
        seq: PDFTextSeq,
        ncs: PDFColorSpace,
        graphicstate: PDFGraphicState,
    ) -> None:
        """Respond to render string event by updating text state."""
        pass

    def render_char(
        self,
        matrix: Matrix,
        font: PDFFont,
        fontsize: float,
        scaling: float,
        rise: float,
        cid: int,
        ncs: PDFColorSpace,
        graphicstate: PDFGraphicState,
    ) -> float:
        """Respond to render char event by updating text state."""
        pass

    def receive_layout(self, ltpage: LTPage) -> None:
        """Receive layout handler."""
        pass

    def get_result(self) -> LTPage | None:
        """Get the result of the analysis."""
        pass


@contextmanager
def patch_pdfminer(pscript5_mode: bool):
    """Patch pdfminer.six to work around bugs in PDFs created by PScript5."""
    pass


@deprecated(deprecated_in='16.6.0', details='Use PdfMinerState instead.')
def get_page_analysis(
    infile: PathLike, pageno: int, pscript5_mode: bool
) -> LTPage | None:
    """Get the page analysis for a given page."""
    pass


class PdfMinerState:
    """Provide a context manager for using pdfminer.six.

    This ensures that the file is closed. It also provides a cache of pages
    from the PDF so that they can be reused if needed, to improve performance.
    """

    def __init__(self, infile: Path, pscript5_mode: bool) -> None:
        """Initialize the context manager.

        Args:
            infile: The path to the PDF file to be analyzed.
            pscript5_mode: Whether the PDF was generated by PScript5.dll.
        """
        self.infile = infile
        self.rman = pdfminer.pdfinterp.PDFResourceManager(caching=True)
        self.disable_boxes_flow = None
        self.page_iter = None
        self.page_cache: list[PDFPage] = []
        self.pscript5_mode = pscript5_mode
        self.file = None

    def __enter__(self):
        """Enter the context manager."""
        self.file = Path(self.infile).open('rb')
        self.page_iter = PDFPage.get_pages(self.file)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager."""
        if self.file:
            self.file.close()
        return True

    def get_page_analysis(self, pageno: int):
        """Get the page analysis for a given page."""
        pass


def get_text_boxes(obj) -> Iterator[LTTextBox]:
    """Get the text boxes attached to the current node."""
    pass
