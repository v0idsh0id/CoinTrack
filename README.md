# CoinTrack

A Python-based cryptocurrency price tracker that displays live prices and statistics for the top 20 most popular cryptocurrencies.

## Features

- **Dual Interface**: Both CLI and GUI modes
- Live tracking of top 20 cryptocurrencies by market cap
- Real-time price updates
- Display key statistics: price, market cap, 24h volume, and 24h price change
- Auto-refresh functionality for continuous monitoring
- Clean console-based interface (CLI) or modern graphical interface (GUI)

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

### GUI Mode (Graphical Interface)

Launch the graphical user interface:
```bash
python main.py --gui
```

Or simply:
```bash
python main.py -g
```

The GUI provides:
- Interactive table with real-time updates
- Configurable refresh interval
- Start/Stop controls for live tracking
- Color-coded price changes (green for positive, red for negative)
- One-time refresh button

### CLI Mode (Command Line Interface)

Run the live tracker in the terminal:
```bash
python main.py
```

With custom refresh interval (e.g., 30 seconds):
```bash
python main.py -r 30
```

Fetch data once without live tracking:
```bash
python main.py --once
```

## Command Line Options

- `-g`, `--gui`: Launch GUI mode (default: CLI mode)
- `-r SECONDS`, `--refresh SECONDS`: Set refresh interval in seconds (default: 60)
- `-o`, `--once`: Fetch data once and exit (CLI only)
- `-h`, `--help`: Show help message

## Data Source

This application uses the CoinGecko API to fetch cryptocurrency data.