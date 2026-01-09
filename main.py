#!/usr/bin/env python3
"""
CoinTrack - Main Entry Point
Live cryptocurrency price tracker for the top 20 cryptocurrencies.
"""

import argparse
from crypto_tracker import CryptoTracker


def main():
    """Main function to run the CoinTrack application."""
    parser = argparse.ArgumentParser(
        description='CoinTrack - Live cryptocurrency price tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-r', '--refresh',
        type=int,
        default=60,
        help='Refresh interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '-o', '--once',
        action='store_true',
        help='Fetch data once and exit (no live tracking)'
    )
    
    args = parser.parse_args()
    
    tracker = CryptoTracker()
    
    if args.once:
        # Fetch and display once, then exit
        print("Fetching cryptocurrency data...\n")
        cryptos = tracker.fetch_top_cryptos()
        if cryptos:
            tracker.display_cryptos(cryptos)
        else:
            print("Failed to fetch data.")
    else:
        # Run live tracker with auto-refresh
        tracker.run_live_tracker(refresh_interval=args.refresh)


if __name__ == "__main__":
    main()
