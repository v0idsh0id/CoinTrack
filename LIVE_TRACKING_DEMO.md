# CoinTrack Live Tracking Confirmation

## Yes, CoinTrack DOES Live Track Cryptocurrency Data! ✅

### CLI Mode - Live Tracking

**Default behavior** (without `--once` flag):
```bash
python main.py
```

This will:
1. Fetch the top 20 cryptocurrencies from CoinGecko API
2. Display the data in a formatted table
3. Wait 60 seconds (default refresh interval)
4. **Automatically fetch fresh data again**
5. **Repeat steps 2-4 indefinitely** until you press Ctrl+C

**Custom refresh interval:**
```bash
python main.py -r 30    # Updates every 30 seconds
python main.py -r 120   # Updates every 2 minutes
```

**Example output:**
```
Starting CoinTrack Live Tracker...
Press Ctrl+C to stop.

========================================================================================================================
CoinTrack - Top 20 Cryptocurrencies (Updated: 2026-01-09 11:50:00)
========================================================================================================================
Rank   Name                 Symbol   Price           24h Change   Market Cap      24h Volume     
------------------------------------------------------------------------------------------------------------------------
1      Bitcoin              BTC      $45,000.50      +2.50%       $880.00B        $28.00B        
2      Ethereum             ETH      $2,800.75       -1.20%       $340.00B        $15.00B        
...
========================================================================================================================

Next update in 60 seconds...

[After 60 seconds, automatically refreshes and displays updated prices]

========================================================================================================================
CoinTrack - Top 20 Cryptocurrencies (Updated: 2026-01-09 11:51:00)
========================================================================================================================
Rank   Name                 Symbol   Price           24h Change   Market Cap      24h Volume     
------------------------------------------------------------------------------------------------------------------------
1      Bitcoin              BTC      $45,125.30      +2.75%       $882.00B        $28.50B        
2      Ethereum             ETH      $2,815.40       -0.95%       $341.00B        $15.20B        
...
========================================================================================================================

Next update in 60 seconds...
```

### GUI Mode - Live Tracking

**Launch GUI:**
```bash
python main.py --gui
```

**How live tracking works in GUI:**

1. **Set refresh interval** - Enter desired seconds (e.g., 60, 30, 120)
2. **Click "Start Tracking"** button (turns RED when active)
3. **Watch live updates** - The table automatically refreshes at your specified interval
4. **Real-time status** - "Last Updated" timestamp shows when data was fetched
5. **Stop anytime** - Click "Stop Tracking" button (turns GREEN when stopped)

**GUI Live Tracking Features:**
- ✅ Background thread continuously fetches data
- ✅ Non-blocking UI - interact while tracking
- ✅ Color-coded changes update in real-time (green/red)
- ✅ Status label shows "Running" during live tracking
- ✅ Timestamp updates with each refresh
- ✅ "Refresh Once" button for manual updates

### Code Implementation

**CLI Live Tracking** (`crypto_tracker.py` lines 115-138):
```python
def run_live_tracker(self, refresh_interval=60):
    """Run the live cryptocurrency tracker with auto-refresh."""
    print("Starting CoinTrack Live Tracker...")
    print(f"Press Ctrl+C to stop.\n")
    
    try:
        while True:  # ← INFINITE LOOP for continuous tracking
            cryptos = self.fetch_top_cryptos()  # Fetch fresh data
            if cryptos:
                self.display_cryptos(cryptos)  # Display updated data
                print(f"\nNext update in {refresh_interval} seconds...")
            else:
                print("Failed to fetch data. Retrying...")
            
            time.sleep(refresh_interval)  # Wait before next update
    except KeyboardInterrupt:
        print("\n\nTracker stopped by user. Goodbye!")
```

**GUI Live Tracking** (`gui.py` lines 189-196):
```python
def live_update_loop(self):
    """Background loop for live updates."""
    while self.is_running:  # ← Runs continuously while tracking
        self.fetch_and_display()  # Fetch and update display
        
        # Wait for refresh interval with responsive shutdown
        if self.stop_event.wait(self.refresh_interval):
            break
```

## Summary

**YES**, CoinTrack provides **true live tracking** of cryptocurrency prices:

✅ **CLI Mode**: Automatically refreshes every 60 seconds (or custom interval)  
✅ **GUI Mode**: Start/Stop live tracking with configurable intervals  
✅ **Continuous Updates**: Fetches fresh data from CoinGecko API in a loop  
✅ **Real-time Display**: Shows updated prices, market cap, volume, and 24h changes  
✅ **Always Current**: Keeps running until you manually stop it  

The only non-live option is `python main.py --once` which fetches data just once and exits.
