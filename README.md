# CoinTrack

A Python-based cryptocurrency price tracker that displays live prices and statistics for the top 20 most popular cryptocurrencies.

## Features

- Live tracking of top 20 cryptocurrencies by market cap
- Real-time price updates
- Display key statistics: price, market cap, 24h volume, and 24h price change
- Auto-refresh functionality for continuous monitoring
- Clean console-based interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/v0idsh0id/CoinTrack.git
cd CoinTrack
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the tracker:
```bash
python main.py
```

The application will display the top 20 cryptocurrencies with their current statistics and automatically refresh every 60 seconds.

## Data Source

This application uses the CoinGecko API to fetch cryptocurrency data.