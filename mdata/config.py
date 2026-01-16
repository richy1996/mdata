import sys
import os

_CONFIG_KEY_PATH = os.path.expanduser("~/.config/mdata/key")

def _read_key_file():
    try:
        with open(_CONFIG_KEY_PATH, "r") as f:
            key = f.read().strip()
            return key if key else None
    except FileNotFoundError:
        return None
    except OSError:
        return None

def get_api_key():
    """
    Retrieves the Massive API key.
    Priority:
    1. Environment Variable (Required for CLI usage !mdata)
    2. Config file written by mdata.auth_colab()
    3. Google Colab Secrets (Works only if imported/run within kernel)
    """
    # 1. Try Environment Variable first
    key = os.environ.get("MASSIVE_API_KEY")
    if key:
        return key

    # 2. Try config file
    key = _read_key_file()
    if key:
        return key

    # 3. Try Colab Secrets (will fail if running as subprocess !mdata)
    try:
        from google.colab import userdata
        key = userdata.get("MASSIVE_API_KEY")
        if key:
            return key
    except Exception:
        # Fails with AttributeError if no kernel (CLI mode)
        pass

    # 3. Fail
    print("Error: MASSIVE_API_KEY not found.", file=sys.stderr)
    print("Fix: In Colab, run this once before using !mdata:", file=sys.stderr)
    print("   import mdata; mdata.auth_colab()", file=sys.stderr)
    sys.exit(1)
