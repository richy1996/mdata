from datetime import datetime

def format_date_str(date_str):
    """
    Converts YYYYMMDD string to YYYY-MM-DD.
    """
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        # If it's already in a different format, or invalid, let the API or caller handle it
        # But for this specific requirement, we assume valid input or basic error handling
        return date_str
