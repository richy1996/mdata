import sys
import os

def get_api_key():
    """
    Retrieves the Massive API key.
    Priority:
    1. Environment Variable (Required for CLI usage !mdata)
    2. Google Colab Secrets (Works only if imported/run within kernel)
    """
    # 1. Try Environment Variable first
    key = os.environ.get("MASSIVE_API_KEY")
    if key:
        return key

    # 2. Try Colab Secrets (will fail if running as subprocess !mdata)
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
    print("   import os; from google.colab import userdata", file=sys.stderr)
    print("   os.environ['MASSIVE_API_KEY'] = userdata.get('MASSIVE_API_KEY')", file=sys.stderr)
    sys.exit(1)

