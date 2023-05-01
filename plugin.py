import importlib.util
import pathlib
import sys
import traceback


class PluginBase():
    """Plugins derive from this class. Then put the plugin into the ./plugins directory."""
    def __init__(self, SOURCE_PATH: pathlib.Path, WWW_PATH: pathlib.Path, WWW_MEDIA_PATH: pathlib.Path):
        self.SOURCE_PATH = SOURCE_PATH
        self.WWW_PATH = WWW_PATH
        self.WWW_MEDIA_PATH = WWW_MEDIA_PATH

    def pre_put_source_file(self, name: str, data: str) -> tuple[str, str]:
        """Called before source files are written or processed."""
        return name, data

    def post_put_source_file(self, source_file_path: pathlib.Path, www_file_path: pathlib.Path) -> None:
        """Called after source files have been written and processed."""


plugins: list[PluginBase] = []


def load(PLUGIN_PATH: pathlib.Path, SOURCE_PATH: pathlib.Path, WWW_PATH: pathlib.Path, WWW_MEDIA_PATH: pathlib.Path) -> None:
    try:
        plugin_paths = PLUGIN_PATH.glob("*.py")

        for plugin_path in plugin_paths:
            import_spec = importlib.util.spec_from_file_location(plugin_path.stem, str(plugin_path.resolve()))
            plugin_module = importlib.util.module_from_spec(import_spec)
            import_spec.loader.exec_module(plugin_module)

            plugin = plugin_module.Plugin(SOURCE_PATH, WWW_MEDIA_PATH, WWW_MEDIA_PATH)
            plugins.append(plugin)
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)


def pre_put_source_file(name: str, data: str) -> tuple[str, str]:
    """Invoke function for all plugins."""
    try:
        for plugin in plugins:
            name, data = plugin.pre_put_source_file(name, data)
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)

    return name, data


def post_put_source_file(source_file_path: pathlib.Path, www_file_path: pathlib.Path) -> None:
    """Invoke function for all plugins."""
    try:
        for plugin in plugins:
            plugin.post_put_source_file(source_file_path, www_file_path)
    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
