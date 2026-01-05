# This file must be used with "source bin/activate.xsh" *from xonsh*.
# You cannot run it directly.

def _deactivate(args):
    # 1. Aliases
    if "pydoc" in aliases:
        del aliases["pydoc"]

    # 2. Restore Path
    if "_OLD_VIRTUAL_PATH" in ${...}:
        $PATH = $_OLD_VIRTUAL_PATH
        del $_OLD_VIRTUAL_PATH

    # 3. Restore Pythonhome
    if "_OLD_VIRTUAL_PYTHONHOME" in ${...}:
        $PYTHONHOME = $_OLD_VIRTUAL_PYTHONHOME
        del $_OLD_VIRTUAL_PYTHONHOME
    elif "PYTHONHOME" in ${...}:
        del $PYTHONHOME

    # 4. Restore Prompt
    if "_OLD_XONSH_PROMPT" in ${...}:
        $PROMPT = $_OLD_XONSH_PROMPT
        del $_OLD_XONSH_PROMPT

    # 5. Restore TCL/TK
    if "_OLD_TCL_LIBRARY" in ${...}:
        $TCL_LIBRARY = $_OLD_TCL_LIBRARY
        del $_OLD_TCL_LIBRARY
    elif "TCL_LIBRARY" in ${...}:
        del $TCL_LIBRARY

    if "_OLD_TK_LIBRARY" in ${...}:
        $TK_LIBRARY = $_OLD_TK_LIBRARY
        del $_OLD_TK_LIBRARY
    elif "TK_LIBRARY" in ${...}:
        del $TK_LIBRARY

    # 6. Clean up venv variables
    if "VIRTUAL_ENV" in ${...}:
        del $VIRTUAL_ENV

    if "VIRTUAL_ENV_PROMPT" in ${...}:
        del $VIRTUAL_ENV_PROMPT

    if "nondestructive" not in args:
        del aliases["deactivate"]

_deactivate(["nondestructive"])

$VIRTUAL_ENV = __VIRTUAL_ENV__
$VIRTUAL_ENV_PROMPT = __VIRTUAL_NAME__

# --- TCL/TK Library ---
if "TCL_LIBRARY" in ${...}:
    $_OLD_TCL_LIBRARY = $TCL_LIBRARY
$TCL_LIBRARY = __TCL_LIBRARY__

if "TK_LIBRARY" in ${...}:
    $_OLD_TK_LIBRARY = $TK_LIBRARY
$TK_LIBRARY = __TK_LIBRARY__

# --- PATH ---
$_OLD_VIRTUAL_PATH = $PATH[:]
_new_bin = $VIRTUAL_ENV + "/" + __BIN_NAME__
$PATH.add(_new_bin, front=True, replace=True)

# --- PROMPT ---
# TODO

# --- PYTHONHOME ---
if "PYTHONHOME" in ${...}:
    $_OLD_VIRTUAL_PYTHONHOME = $PYTHONHOME
    del $PYTHONHOME

aliases["deactivate"] = _deactivate
aliases["pydoc"] = ["python", "-m", "pydoc"]