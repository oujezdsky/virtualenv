env = __xonsh__.env
aliases = __xonsh__.aliases


@aliases.register
def deactivate(args=None):
    if args is None:
        args = []

    # 1. Aliases
    if "pydoc" in aliases:
        del aliases["pydoc"]

    # 2. Restore Path
    if "_OLD_VIRTUAL_PATH" in env:
        $PATH = env["_OLD_VIRTUAL_PATH"]
        env.pop("_OLD_VIRTUAL_PATH", None)

    # 3. Restore Pythonhome
    if "_OLD_VIRTUAL_PYTHONHOME" in env:
        $PYTHONHOME = env["_OLD_VIRTUAL_PYTHONHOME"]
        env.pop("_OLD_VIRTUAL_PYTHONHOME", None)
    elif "PYTHONHOME" in env:
        env.pop("PYTHONHOME", None)

    # 4. Restore Prompt
    if "_OLD_XONSH_PROMPT" in env:
        $PROMPT = env["_OLD_XONSH_PROMPT"]
        env.pop("_OLD_XONSH_PROMPT", None)

    # 5. Restore TCL/TK
    if "_OLD_TCL_LIBRARY" in env:
        $TCL_LIBRARY = env["_OLD_TCL_LIBRARY"]
        env.pop("_OLD_TCL_LIBRARY", None)
    elif "TCL_LIBRARY" in env:
        env.pop("TCL_LIBRARY", None)

    if "_OLD_TK_LIBRARY" in env:
        $TK_LIBRARY = env["_OLD_TK_LIBRARY"]
        env.pop("_OLD_TK_LIBRARY", None)
    elif "TK_LIBRARY" in env:
        env.pop("TK_LIBRARY", None)

    # 6. Clean up venv variables
    env.pop("VIRTUAL_ENV", None)
    env.pop("VIRTUAL_ENV_PROMPT", None)

    if "nondestructive" not in args:
        aliases.pop("deactivate", None)

    return 0


# keep your current "reset previous venv" behavior
deactivate(["nondestructive"])


$VIRTUAL_ENV = __VIRTUAL_ENV__
$VIRTUAL_ENV_PROMPT = __VIRTUAL_NAME__

# --- TCL/TK Library ---
if __TCL_LIBRARY__ != '':
    if "TCL_LIBRARY" in env:
        $_OLD_TCL_LIBRARY = $TCL_LIBRARY
    $TCL_LIBRARY = __TCL_LIBRARY__

if __TK_LIBRARY__ != '':
    if "TK_LIBRARY" in env:
        $_OLD_TK_LIBRARY = $TK_LIBRARY
    $TK_LIBRARY = __TK_LIBRARY__

# --- PATH ---
$_OLD_VIRTUAL_PATH = $PATH[:]
_new_bin = $VIRTUAL_ENV + __PATH_SEP__ + __BIN_NAME__
$PATH.add(_new_bin, front=True, replace=True)

# --- PROMPT ---
if "VIRTUAL_ENV_PROMPT" in env:
    $_OLD_VIRTUAL_ENV_PROMPT = $VIRTUAL_ENV_PROMPT
$VIRTUAL_ENV_PROMPT = __VIRTUAL_NAME__

# --- PYTHONHOME ---
if "PYTHONHOME" in env:
    $_OLD_VIRTUAL_PYTHONHOME = $PYTHONHOME
    env.pop("PYTHONHOME", None)

aliases["pydoc"] = ["python", "-m", "pydoc"]
