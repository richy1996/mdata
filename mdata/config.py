import sys

def get_api_key():
    """
    Retrieves the Massive API key from Google Colab secrets.
    """
    try:
        from google.colab import userdata
        key = userdata.get("MASSIVE_API_KEY")
        if not key:
            print("Error: MASSIVE_API_KEY not found in Google Colab secrets.", file=sys.stderr)
            sys.exit(1)
        return key
    except ImportError:
        # Fallback for local testing if not in Colab
        import os
        key = os.environ.get("MASSIVE_API_KEY")
        if not key:
            print("Error: Not in Colab and MASSIVE_API_KEY env var not set.", file=sys.stderr)
            sys.exit(1)
        return key
