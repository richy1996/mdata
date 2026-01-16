import argparse
import sys
import os
import pandas as pd
from .client import MDataClient
from .utils import format_date_str

def main():
    parser = argparse.ArgumentParser(description="MData: massive data fetcher")
    
    # Positional arguments (optional in parser, but we handle logic to allow mixing)
    parser.add_argument("pos_ticker", nargs="?", help="Ticker symbol (e.g. SPX)")
    parser.add_argument("pos_start", nargs="?", help="Start date (YYYYMMDD)")
    parser.add_argument("pos_end", nargs="?", help="End date (YYYYMMDD)")
    
    # Flags
    parser.add_argument("-t", "--ticker", help="Ticker symbol")
    parser.add_argument("-s", "--startdate", help="Start date (YYYYMMDD)")
    parser.add_argument("-e", "--enddate", help="End date (YYYYMMDD)")
    parser.add_argument("-r", "--resolution", default="minute", choices=["second", "minute", "day"], help="Resolution")
    parser.add_argument("-d", "--directory", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    # Logic to resolve mixed/positional args
    # Priority: Flag > Positional
    
    ticker = args.ticker if args.ticker else args.pos_ticker
    start_date = args.startdate if args.startdate else args.pos_start
    end_date = args.enddate if args.enddate else args.pos_end
    
    # If end_date is missing but start_date is provided as positional, and we have 3 positionals? 
    # The parser puts them in order. 
    # If input is: !mdata spx 20260115 20260115 -> ticker=spx, pos_start=20260115, pos_end=20260115.
    # If input is: !mdata spx 20260115 -> ticker=spx, pos_start=20260115, pos_end=None.
    
    if not ticker or not start_date or not end_date:
        print("Error: Usage mdata ticker start_date end_date OR mdata -t ticker -s start -e end")
        print("Example: mdata spx 20260115 20260115")
        sys.exit(1)
        
    # Format dates
    start_fmt = format_date_str(start_date)
    end_fmt = format_date_str(end_date)
    
    # Initialize Client (prints key)
    client = MDataClient()
    
    print(f"Fetching data for {ticker} from {start_fmt} to {end_fmt} ({args.resolution})...")
    
    try:
        data = client.fetch_aggregates(ticker, start_fmt, end_fmt, resolution=args.resolution)
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
        
    if not data:
        print("No data found.")
        sys.exit(0)
        
    # Create DataFrame
    df = pd.DataFrame(data)

    # Normalize columns from Massive aggregates
    if {"o", "h", "l", "c", "t"}.issubset(df.columns):
        df = df.rename(
            columns={
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "t": "timestamp",
            }
        )

    # Add date/time columns in US/Eastern
    if "timestamp" in df.columns:
        df["datetime"] = (
            pd.to_datetime(df["timestamp"], unit="ms")
            .dt.tz_localize("UTC")
            .dt.tz_convert("US/Eastern")
        )
        df["date"] = df["datetime"].dt.strftime("%Y%m%d").astype("uint32")
        if args.resolution == "second":
            df["time"] = df["datetime"].dt.strftime("%H%M%S").astype("uint32")
        elif args.resolution == "minute":
            df["time"] = df["datetime"].dt.strftime("%H%M").astype("uint32")

    df["ticker"] = ticker.lower()

    # Order columns
    base_cols = ["open", "high", "low", "close", "date"]
    if args.resolution in {"second", "minute"}:
        base_cols.append("time")
    base_cols.append("ticker")
    df = df[base_cols]
    
    # Ensure directory exists
    if args.directory != ".":
        os.makedirs(args.directory, exist_ok=True)
        
    # Filename
    # ticker_startdate_enddate.parquet (using the formatted dates? User said "ticker_startdate_enddate")
    # User input was 20260115. Formatted is 2026-01-15.
    # User example: "ticker_startdate_enddate.parquet" (ambiguous if it matched input or standard).
    # I'll use the formatted dates (ISO) for clarity in filename, or the raw input?
    # Let's use the formatted ones to be safe, replacing hyphens if needed or keeping them.
    # "ticker_startdate_enddate" implies just concatenation. 
    # Let's use ISO format but maybe sanitized. 
    # Actually, user said: "i can simply copy it and so i'd read it in like data = pd.read_parquet..."
    # I will simply use `{ticker}_{start_date}_{end_date}.parquet` (using the raw input strings if valid, or the formatted ones).
    # Using formatted (YYYY-MM-DD) is safer.
    
    start_compact = start_fmt.replace("-", "")
    end_compact = end_fmt.replace("-", "")
    resolution_suffix = {"second": "s", "minute": "m", "day": "d"}[args.resolution]
    filename = f"{ticker.lower()}_{start_compact}_{end_compact}_{resolution_suffix}.parquet"
    output_path = os.path.join(args.directory, filename)
    
    df.to_parquet(output_path)
    
    print(output_path)

if __name__ == "__main__":
    main()
