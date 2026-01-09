"""
CoinTrack - Cryptocurrency Price Tracker
This module provides functionality to fetch and display live cryptocurrency data.
"""

import requests
import time
from datetime import datetime


class CryptoTracker:
    """Tracks cryptocurrency prices and statistics."""
    
    def __init__(self):
        self.api_base_url = "https://api.coingecko.com/api/v3"
        
    def fetch_top_cryptos(self, limit=20):
        """
        Fetch top cryptocurrencies by market cap.
        
        Args:
            limit: Number of cryptocurrencies to fetch (default: 20)
            
        Returns:
            List of cryptocurrency data dictionaries or None if error
        """
        try:
            endpoint = f"{self.api_base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def format_number(self, num):
        """Format large numbers with appropriate suffixes."""
        if num is None:
            return "N/A"
        
        if num >= 1_000_000_000_000:
            return f"${num/1_000_000_000_000:.2f}T"
        elif num >= 1_000_000_000:
            return f"${num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"${num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"${num/1_000:.2f}K"
        else:
            return f"${num:.2f}"
    
    def format_price(self, price):
        """Format cryptocurrency price."""
        if price is None:
            return "N/A"
        
        if price >= 1:
            return f"${price:,.2f}"
        else:
            return f"${price:.6f}"
    
    def format_percentage(self, percentage):
        """Format percentage change with color indicator."""
        if percentage is None:
            return "N/A"
        
        sign = "+" if percentage >= 0 else ""
        return f"{sign}{percentage:.2f}%"
    
    def display_cryptos(self, cryptos):
        """
        Display cryptocurrency data in a formatted table.
        
        Args:
            cryptos: List of cryptocurrency data dictionaries
        """
        if not cryptos:
            print("No data available.")
            return
        
        # Clear screen and print header
        print("\n" + "=" * 120)
        print(f"CoinTrack - Top 20 Cryptocurrencies (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print("=" * 120)
        
        # Print table header
        header = f"{'Rank':<6} {'Name':<20} {'Symbol':<8} {'Price':<15} {'24h Change':<12} {'Market Cap':<15} {'24h Volume':<15}"
        print(header)
        print("-" * 120)
        
        # Print each cryptocurrency
        for crypto in cryptos:
            rank = crypto.get('market_cap_rank', 'N/A')
            name = crypto.get('name', 'Unknown')[:18]
            symbol = crypto.get('symbol', 'N/A').upper()
            price = self.format_price(crypto.get('current_price'))
            change_24h = self.format_percentage(crypto.get('price_change_percentage_24h'))
            market_cap = self.format_number(crypto.get('market_cap'))
            volume_24h = self.format_number(crypto.get('total_volume'))
            
            row = f"{str(rank):<6} {name:<20} {symbol:<8} {price:<15} {change_24h:<12} {market_cap:<15} {volume_24h:<15}"
            print(row)
        
        print("=" * 120)
    
    def run_live_tracker(self, refresh_interval=60):
        """
        Run the live cryptocurrency tracker with auto-refresh.
        
        Args:
            refresh_interval: Time in seconds between refreshes (default: 60)
        """
        print("Starting CoinTrack Live Tracker...")
        print(f"Press Ctrl+C to stop.\n")
        
        try:
            while True:
                cryptos = self.fetch_top_cryptos()
                if cryptos:
                    self.display_cryptos(cryptos)
                    print(f"\nNext update in {refresh_interval} seconds...")
                else:
                    print("Failed to fetch data. Retrying...")
                
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n\nTracker stopped by user. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
