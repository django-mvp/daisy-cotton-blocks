"""The package installs and exposes what a consuming project needs from it."""

from pathlib import Path

from django.apps import apps

import daisy_cotton_ext


class TestPackagedApp:
    def test_app_is_installed(self) -> None:
        assert apps.is_installed("daisy_cotton_ext")

    def test_component_directory_is_where_cotton_looks_for_it(self) -> None:
        components = Path(daisy_cotton_ext.__file__).parent / "templates" / "cotton"
        assert components.is_dir()

    def test_stylesheet_is_packaged(self) -> None:
        stylesheet = (
            Path(daisy_cotton_ext.__file__).parent
            / "static"
            / "css"
            / "daisy-cotton-ext.css"
        )
        assert stylesheet.is_file()
