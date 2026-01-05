from __future__ import annotations

from virtualenv.activation.via_template import ViaTemplateActivator


class XonshActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.xsh"

    @staticmethod
    def quote(string: str) -> str:
        return repr(string)


__all__ = ["XonshActivator"]
