import os
import json

from trame.html import AbstractElement

serve_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "serve"))

serve = {"__parflow": serve_path}
scripts = ["/__parflow/parflow.umd.min.js"]
styles = ["/__parflow/parflow.css"]
vue_use = ["widgets"]


class FileDatabase(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("file-database", children, **kwargs)
        self._attr_names += ["files", "db_update"]


class NavigationDropDown(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("navigation-drop-down", children, **kwargs)
        self._attr_names += ["views"]
