# CoinTrack GUI Features

## GUI Interface Overview

The CoinTrack GUI provides a modern, user-friendly interface for tracking cryptocurrency prices.

### Window Layout (1200x700 pixels)

#### 1. Title Bar (Top - Dark Blue Background)
- **Title**: "CoinTrack - Top 20 Cryptocurrencies" (Large, bold, white text)
- **Last Updated**: Timestamp showing when data was last refreshed

#### 2. Control Panel (Below Title)
- **Refresh Interval Input**: Text field to set custom refresh interval in seconds
- **Start/Stop Button**: 
  - Green "Start Tracking" button when idle
  - Red "Stop Tracking" button when running
- **Refresh Once Button**: Blue button for one-time data fetch
- **Status Label**: Shows current status (Idle/Running/Fetching/Error)

#### 3. Data Table (Main Area)
Scrollable table with 7 columns:
- **Rank**: Cryptocurrency ranking by market cap
- **Name**: Full name of the cryptocurrency
- **Symbol**: Ticker symbol (e.g., BTC, ETH)
- **Price**: Current price in USD
- **24h Change**: Percentage change (green for positive, red for negative)
- **Market Cap**: Total market capitalization
- **24h Volume**: 24-hour trading volume

#### 4. Footer (Bottom)
- Data source attribution: "Data source: CoinGecko API"

### Key Features

1. **Live Tracking**: Start/stop automatic updates at configurable intervals
2. **Color Coding**: Positive changes in green, negative in red
3. **Threading**: Background updates don't freeze the UI
4. **Error Handling**: User-friendly error messages for API failures
5. **Responsive**: Scrollable table for all 20 cryptocurrencies

### Usage

Launch GUI mode:
```bash
python main.py --gui
```

Or use short flag:
```bash
python main.py -g
```

The GUI will open in a new window with all controls ready to use.
