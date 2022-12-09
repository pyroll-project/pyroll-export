import pluggy

plugin_manager = pluggy.PluginManager("pyroll_export")
hookspec = pluggy.HookspecMarker("pyroll_export")
hookimpl = pluggy.HookimplMarker("pyroll_export")
