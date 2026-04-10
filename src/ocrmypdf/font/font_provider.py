# SPDX-FileCopyrightText: 2025 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

"""Font provider protocol and implementations for PDF rendering."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

from ocrmypdf.font.font_manager import FontManager

log = logging.getLogger(__name__)


class FontProvider(Protocol):
    """Protocol for providing fonts to MultiFontManager.

    Implementations are responsible for knowing where fonts are located
    and loading them. MultiFontManager asks for fonts by name and uses
    them for glyph coverage checking.
    """

    def get_font(self, font_name: str) -> FontManager | None:
        """Get a FontManager for the named font.

        Args:
            font_name: Logical font name (e.g., 'NotoSans-Regular')

        Returns:
            FontManager if font is available, None otherwise
        """
        ...

    def get_available_fonts(self) -> list[str]:
        """Get list of available font names.

        Returns:
            List of font names that can be retrieved with get_font()
        """
        ...

    def get_fallback_font(self) -> FontManager:
        """Get the glyphless fallback font.

        This font must always be available and handles any codepoint.

        Returns:
            FontManager for the glyphless fallback font (Occulta.ttf)
        """
        ...


class BuiltinFontProvider:
    """Font provider using builtin fonts from ocrmypdf/data directory."""

    # Mapping of logical font names to filenames
    # Only Latin (NotoSans) and the glyphless fallback (Occulta.ttf) are bundled.
    # All other scripts (Arabic, Devanagari, CJK, etc.) are discovered from
    # system fonts by SystemFontProvider to reduce package size.
    FONT_FILES = {
        'NotoSans-Regular': 'NotoSans-Regular.ttf',
        'Occulta': 'Occulta.ttf',
    }

    def __init__(self, font_dir: Path | None = None):
        """Initialize builtin font provider.

        Args:
            font_dir: Directory containing font files. If None, uses
                      the default ocrmypdf/data directory.
        """
        if font_dir is None:
            font_dir = Path(__file__).parent.parent / "data"
        self.font_dir = font_dir
        self._fonts: dict[str, FontManager] = {}
        self._load_fonts()

    def _load_fonts(self) -> None:
        """Load available fonts, logging warnings for missing ones."""
        pass

    def get_font(self, font_name: str) -> FontManager | None:
        """Get a FontManager for the named font."""
        return self._fonts.get(font_name)

    def get_available_fonts(self) -> list[str]:
        """Get list of available font names."""
        pass

    def get_fallback_font(self) -> FontManager:
        """Get the glyphless fallback font."""
        return self._fonts['Occulta']


class ChainedFontProvider:
    """Font provider that tries multiple providers in order.

    This allows combining builtin fonts with system fonts, trying
    the builtin provider first and falling back to system fonts
    for fonts not bundled with the package.
    """

    def __init__(self, providers: list[FontProvider]):
        """Initialize chained font provider.

        Args:
            providers: List of font providers to try in order.
                       The first provider that returns a font wins.
        """
        if not providers:
            raise ValueError("At least one provider is required")
        self.providers = providers

    def get_font(self, font_name: str) -> FontManager | None:
        """Get a FontManager for the named font.

        Tries each provider in order until one returns a font.

        Args:
            font_name: Logical font name (e.g., 'NotoSans-Regular')

        Returns:
            FontManager if any provider has the font, None otherwise
        """
        for provider in self.providers:
            if font := provider.get_font(font_name):
                return font
        return None

    def get_available_fonts(self) -> list[str]:
        """Get list of available font names from all providers.

        Returns:
            Combined list of font names (deduplicated, order preserved)
        """
        pass

    def get_fallback_font(self) -> FontManager:
        """Get the glyphless fallback font.

        Tries each provider until one provides a fallback font.

        Returns:
            FontManager for the fallback font

        Raises:
            RuntimeError: If no provider can provide a fallback font
        """
        for provider in self.providers:
            try:
                return provider.get_fallback_font()
            except (NotImplementedError, AttributeError, KeyError):
                continue
        raise RuntimeError("No fallback font available from any provider")
