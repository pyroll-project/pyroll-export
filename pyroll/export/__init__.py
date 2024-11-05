import importlib.util

from .export import to_dict, to_pandas, to_json, to_yaml
from pyroll.export.pluggy import plugin_manager

from . import hookspecs

plugin_manager.add_hookspecs(hookspecs)

from . import convert

plugin_manager.register(convert)

CLI_INSTALLED = bool(importlib.util.find_spec("pyroll.cli"))

if CLI_INSTALLED:
    from . import cli

VERSION = "2.2.1"
