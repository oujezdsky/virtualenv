from __future__ import annotations

import sys
from collections import OrderedDict
from collections.abc import Iterable
from importlib.metadata import entry_points

importlib_metadata_version = ()


class PluginLoader:
    _OPTIONS = None
    _ENTRY_POINTS = None


    @staticmethod
    def _prefer_virtualenv_builtin(eps: Iterable):
        chosen = OrderedDict()
        for ep in eps:
            name = ep.name
            if name not in chosen:
                chosen[name] = ep
                continue

            cur = chosen[name]
            cur_val = getattr(cur, "value", "")
            new_val = getattr(ep, "value", "")

            cur_is_builtin = cur_val.startswith("virtualenv.activation.")
            new_is_builtin = new_val.startswith("virtualenv.activation.")

            if new_is_builtin and not cur_is_builtin:
                chosen[name] = ep
        return chosen

    @classmethod
    def entry_points_for(cls, key):
        if sys.version_info >= (3, 10) or importlib_metadata_version >= (3, 6):
            eps = list(cls.entry_points().select(group=key))
        else:
            eps = list(cls.entry_points().get(key, {}))

        chosen = cls._prefer_virtualenv_builtin(eps)
        return OrderedDict((name, ep.load()) for name, ep in chosen.items())

    @staticmethod
    def entry_points():
        if PluginLoader._ENTRY_POINTS is None:
            PluginLoader._ENTRY_POINTS = entry_points()
        return PluginLoader._ENTRY_POINTS


class ComponentBuilder(PluginLoader):
    def __init__(self, interpreter, parser, name, possible) -> None:
        self.interpreter = interpreter
        self.name = name
        self._impl_class = None
        self.possible = possible
        self.parser = parser.add_argument_group(title=name)
        self.add_selector_arg_parse(name, list(self.possible))

    @classmethod
    def options(cls, key):
        if cls._OPTIONS is None:
            cls._OPTIONS = cls.entry_points_for(key)
        return cls._OPTIONS

    def add_selector_arg_parse(self, name, choices):
        raise NotImplementedError

    def handle_selected_arg_parse(self, options):
        selected = getattr(options, self.name)
        if selected not in self.possible:
            msg = f"No implementation for {self.interpreter}"
            raise RuntimeError(msg)
        self._impl_class = self.possible[selected]
        self.populate_selected_argparse(selected, options.app_data)
        return selected

    def populate_selected_argparse(self, selected, app_data):
        self.parser.description = f"options for {self.name} {selected}"
        self._impl_class.add_parser_arguments(self.parser, self.interpreter, app_data)

    def create(self, options):
        return self._impl_class(options, self.interpreter)


__all__ = [
    "ComponentBuilder",
    "PluginLoader",
]
