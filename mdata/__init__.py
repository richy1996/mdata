import os

_CONFIG_KEY_PATH = os.path.expanduser("~/.config/mdata/key")

def auth_colab():
    """
    Fetches MASSIVE_API_KEY from Colab secrets and stores it for CLI use.
    """
    try:
        from google.colab import userdata
        key = userdata.get("MASSIVE_API_KEY")
    except Exception as exc:
        raise RuntimeError("google.colab.userdata not available in this environment") from exc

    if not key:
        raise RuntimeError("MASSIVE_API_KEY not found in Colab secrets")

    os.makedirs(os.path.dirname(_CONFIG_KEY_PATH), exist_ok=True)
    with open(_CONFIG_KEY_PATH, "w") as f:
        f.write(key.strip())

    try:
        os.chmod(_CONFIG_KEY_PATH, 0o600)
    except OSError:
        # Best-effort on platforms that don't support chmod.
        pass

    return _CONFIG_KEY_PATH

__all__ = ["auth_colab"]
