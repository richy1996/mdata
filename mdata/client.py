from massive import RESTClient
from .config import get_api_key

class MDataClient:
    def __init__(self):
        self.api_key = get_api_key()
        print(f"Using Massive API Key: {self.api_key}")
        self.client = RESTClient(self.api_key)

    def fetch_aggregates(self, ticker, start_date, end_date, resolution="minute"):
        """
        Fetches aggregates for the given ticker.
        """
        # Ensure ticker is uppercase
        ticker = ticker.upper()
        
        # Handle Massive API specific formatting for Indices
        # e.g. SPX -> I:SPX
        # We check against a list of common indices. 
        # If the user already provided "I:SPX", this logic preserves it.
        known_indices = ["SPX", "NDX", "DJI", "VIX", "RUT"]
        
        if ticker in known_indices:
            api_ticker = f"I:{ticker}"
        else:
            api_ticker = ticker

        # Map resolution to (multiplier, timespan)
        multiplier = 1

        timespan = resolution
        
        if resolution == "minute":
            timespan = "minute"
        elif resolution == "second":
            timespan = "second"
        elif resolution == "day":
            timespan = "day"
            
        # The user code example has `1, "minute"`.
        
        aggs = []
        results = self.client.list_aggs(
            api_ticker,
            multiplier,
            timespan,
            start_date,
            end_date,
            sort="asc",
            limit=50000 
        )
        
        for a in results:
            aggs.append(a)
            
        return aggs
