from __future__ import annotations

import os
from argparse import Namespace
from shutil import which

import pytest

from virtualenv.activation import XonshActivator
from virtualenv.info import IS_WIN


@pytest.mark.parametrize(
    ("tcl_lib", "tk_lib", "present"),
    [
        ("/path/to/tcl", "/path/to/tk", True),
        (None, None, False),
    ],
)
def test_xonsh_tkinter_generation(tmp_path, tcl_lib, tk_lib, present):
    class MockInterpreter:
        pass

    interpreter = MockInterpreter()
    interpreter.tcl_lib = tcl_lib
    interpreter.tk_lib = tk_lib

    quoted_tcl_path = XonshActivator.quote(interpreter.tcl_lib)
    quoted_tk_path = XonshActivator.quote(interpreter.tk_lib)

    class MockCreator:
        def __init__(self, dest):
            self.dest = dest
            self.bin_dir = dest / ("Scripts" if IS_WIN else "bin")
            self.bin_dir.mkdir()
            self.interpreter = interpreter
            self.pyenv_cfg = {}
            self.env_name = "my-env"

    creator = MockCreator(tmp_path)
    options = Namespace(prompt=None)
    activator = XonshActivator(options)

    activator.generate(creator)
    content = (creator.bin_dir / "activate.xsh").read_text(encoding="utf-8")

    if present:
        # activation section
        assert f"if {quoted_tcl_path} != '':" in content
        assert f"if {quoted_tk_path} != '':" in content

        assert f"$TCL_LIBRARY = {quoted_tcl_path}" in content
        assert f"$TK_LIBRARY = {quoted_tk_path}" in content

        # backup of previous values (if present)
        assert "$_OLD_TCL_LIBRARY = $TCL_LIBRARY" in content
        assert "$_OLD_TK_LIBRARY = $TK_LIBRARY" in content
    else:
        assert "if '' != '':" in content
        assert "$TCL_LIBRARY = ''" in content
        assert "$TK_LIBRARY = ''" in content

    # deactivate section always contains restore/cleanup logic
    assert 'if "_OLD_TCL_LIBRARY" in env:' in content
    assert '$TCL_LIBRARY = env["_OLD_TCL_LIBRARY"]' in content
    assert 'if "_OLD_TK_LIBRARY" in env:' in content
    assert '$TK_LIBRARY = env["_OLD_TK_LIBRARY"]' in content


def test_xonsh(activation_tester_class, activation_tester):
    class XonshActivatorTester(activation_tester_class):
        def __init__(self, session) -> None:
            cmd = which("xonsh") or which("xsh")

            super().__init__(
                XonshActivator,
                session,
                cmd,
                "activate.xsh",
                "xsh",
            )
            redir = "2>nul" if IS_WIN else "2>/dev/null"
            self.pydoc_call = f"{str(self._creator.exe)!r} -m pydoc -w pydoc_test {redir}"

        def env(self, tmp_path):
            env = super().env(tmp_path)
            if IS_WIN:
                env.setdefault("ALLUSERSPROFILE", r"C:\ProgramData")
            return env

        def print_prompt(self):
            return r'echo "($VIRTUAL_ENV_PROMPT) "'

        def activate_call(self, script):
            cmd = self.activate_cmd
            scr = self.quote(str(script))
            return f"{cmd} {scr}".strip()

    activation_tester(XonshActivatorTester)
