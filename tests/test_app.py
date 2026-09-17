"""The package installs and exposes what a consuming project needs from it."""

from pathlib import Path

from django.apps import apps

import mvp_bits


class TestPackagedApp:
    """What a host project gets after installing and adding it to INSTALLED_APPS."""

    def test_app_is_installed(self) -> None:
        assert apps.is_installed("mvp_bits")

    def test_component_directory_is_where_cotton_looks_for_it(self) -> None:
        """Cotton resolves `<c-mvp-bits.thing>` to `cotton/mvp_bits/thing.html`.

        It maps hyphens in a tag name onto underscores on disk, so the directory
        name is not a free choice: renaming it breaks every component tag at
        once, and does so silently — a missing component renders as empty output
        rather than raising.
        """
        components = (
            Path(mvp_bits.__file__).parent / "templates" / "cotton" / "mvp_bits"
        )
        assert components.is_dir()

    def test_stylesheet_is_packaged(self) -> None:
        """Shipped as a built file so that installing this package needs no Node."""
        stylesheet = Path(mvp_bits.__file__).parent / "static" / "css" / "mvp-bits.css"
        assert stylesheet.is_file()
