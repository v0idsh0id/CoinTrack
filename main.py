#!/usr/bin/env python3
"""
CoinTrack - Main Entry Point
Live cryptocurrency price tracker for the top 20 cryptocurrencies.
"""

import argparse
import sys
from crypto_tracker import CryptoTracker


def main():
    """Main function to run the CoinTrack application."""
    parser = argparse.ArgumentParser(
        description='CoinTrack - Live cryptocurrency price tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-g', '--gui',
        action='store_true',
        help='Launch GUI mode (default: CLI mode)'
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
        help='Fetch data once and exit (no live tracking, CLI only)'
    )
    
    args = parser.parse_args()
    
    if args.gui:
        # Launch GUI mode
        try:
            from gui import run_gui
            run_gui()
        except ImportError as e:
            print("Error: GUI mode requires tkinter, which is not available.")
            print(f"Details: {e}")
            print("\nPlease ensure tkinter is installed:")
            print("  - On Debian/Ubuntu: sudo apt-get install python3-tk")
            print("  - On Fedora: sudo dnf install python3-tkinter")
            print("  - On macOS: tkinter should be included with Python")
            sys.exit(1)
    else:
        # Run CLI mode
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
