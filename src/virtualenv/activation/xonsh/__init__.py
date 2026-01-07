from __future__ import annotations

import os
from pathlib import Path

from virtualenv.activation.via_template import ViaTemplateActivator


class XonshActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate.xsh"

    @staticmethod
    def quote(value):
        if value is None:
            return "''"
        return repr(str(value))

    def replacements(self, creator, dest_folder):  # noqa: ARG002
        bin_dir = (
            creator.bin_dir.relative_to(creator.dest)
            if isinstance(creator.bin_dir, Path)
            else str(creator.bin_dir.relative_to(creator.dest))
        )
        tcl_lib = getattr(creator.interpreter, "tcl_lib", None)
        tk_lib = getattr(creator.interpreter, "tk_lib", None)

        return {
            "__VIRTUAL_PROMPT__": "" if self.flag_prompt is None else self.flag_prompt,
            "__VIRTUAL_ENV__": str(creator.dest),
            "__VIRTUAL_NAME__": creator.env_name,
            "__BIN_NAME__": bin_dir,
            "__PATH_SEP__": os.pathsep,
            "__TCL_LIBRARY__": tcl_lib or "",
            "__TK_LIBRARY__": tk_lib or "",
        }


__all__ = ["XonshActivator"]
