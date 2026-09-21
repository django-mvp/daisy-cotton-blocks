"""The package installs and exposes what a consuming project needs from it."""

from pathlib import Path

from django.apps import apps

import daisy_cotton_blocks


class TestPackagedApp:
    """What a host project gets after installing and adding it to INSTALLED_APPS."""

    def test_app_is_installed(self) -> None:
        assert apps.is_installed("daisy_cotton_blocks")

    def test_component_directory_is_where_cotton_looks_for_it(self) -> None:
        """Cotton resolves `<c-hero.centred>` to `cotton/hero/centred.html`.

        Blocks sit at the top of `cotton/` rather than under a directory of
        their own, so a tag reads `<c-hero.centred>` and not
        `<c-daisy-cotton-blocks.hero.centred>`. Moving them breaks every tag at
        once, and does so silently — a component Cotton cannot find renders as
        empty output rather than raising.
        """
        components = Path(daisy_cotton_blocks.__file__).parent / "templates" / "cotton"
        assert components.is_dir()

    def test_stylesheet_is_packaged(self) -> None:
        """Shipped as a built file so that installing this package needs no Node."""
        stylesheet = (
            Path(daisy_cotton_blocks.__file__).parent
            / "static"
            / "css"
            / "daisy-cotton-blocks.css"
        )
        assert stylesheet.is_file()
