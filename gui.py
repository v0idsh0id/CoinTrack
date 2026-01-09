"""
CoinTrack - GUI Implementation
Graphical user interface for cryptocurrency price tracking.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
from crypto_tracker import CryptoTracker


class CryptoTrackerGUI:
    """GUI for the cryptocurrency tracker."""
    
    MIN_REFRESH_INTERVAL = 10  # Minimum refresh interval in seconds
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("CoinTrack - Cryptocurrency Price Tracker")
        self.root.geometry("1200x700")
        
        self.tracker = CryptoTracker()
        self.refresh_interval = 60
        self.is_running = False
        self.update_thread = None
        self.stop_event = threading.Event()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Title frame
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="CoinTrack - Top 20 Cryptocurrencies",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()
        
        self.update_time_label = tk.Label(
            title_frame,
            text="Last Updated: Never",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.update_time_label.pack()
        
        # Control frame
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X)
        
        # Refresh interval control
        tk.Label(control_frame, text="Refresh Interval (seconds):", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.interval_var = tk.StringVar(value="60")
        interval_entry = tk.Entry(control_frame, textvariable=self.interval_var, width=10)
        interval_entry.pack(side=tk.LEFT, padx=5)
        
        # Start/Stop button
        self.start_stop_btn = tk.Button(
            control_frame,
            text="Start Tracking",
            command=self.toggle_tracking,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh once button
        refresh_btn = tk.Button(
            control_frame,
            text="Refresh Once",
            command=self.refresh_once,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            padx=20,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Status: Idle",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Table frame with scrollbar
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for cryptocurrency data
        columns = ("Rank", "Name", "Symbol", "Price", "24h Change", "Market Cap", "24h Volume")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Price", text="Price")
        self.tree.heading("24h Change", text="24h Change")
        self.tree.heading("Market Cap", text="Market Cap")
        self.tree.heading("24h Volume", text="24h Volume")
        
        self.tree.column("Rank", width=60, anchor=tk.CENTER)
        self.tree.column("Name", width=150, anchor=tk.W)
        self.tree.column("Symbol", width=80, anchor=tk.CENTER)
        self.tree.column("Price", width=120, anchor=tk.E)
        self.tree.column("24h Change", width=100, anchor=tk.E)
        self.tree.column("Market Cap", width=120, anchor=tk.E)
        self.tree.column("24h Volume", width=120, anchor=tk.E)
        
        # Style for treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom info frame
        info_frame = tk.Frame(self.root, bg="#ecf0f1", pady=5)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        info_label = tk.Label(
            info_frame,
            text="Data source: CoinGecko API",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        info_label.pack()
        
    def toggle_tracking(self):
        """Start or stop live tracking."""
        if not self.is_running:
            # Start tracking
            try:
                self.refresh_interval = int(self.interval_var.get())
                if self.refresh_interval < self.MIN_REFRESH_INTERVAL:
                    messagebox.showwarning(
                        "Warning",
                        f"Refresh interval should be at least {self.MIN_REFRESH_INTERVAL} seconds."
                    )
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for refresh interval.")
                return
            
            self.is_running = True
            self.stop_event.clear()
            self.start_stop_btn.config(text="Stop Tracking", bg="#e74c3c")
            self.status_label.config(text="Status: Running", fg="#27ae60")
            
            # Start update thread
            self.update_thread = threading.Thread(target=self.live_update_loop, daemon=True)
            self.update_thread.start()
        else:
            # Stop tracking
            self.is_running = False
            self.stop_event.set()
            self.start_stop_btn.config(text="Start Tracking", bg="#27ae60")
            self.status_label.config(text="Status: Stopped", fg="#e74c3c")
    
    def live_update_loop(self):
        """Background loop for live updates."""
        while self.is_running:
            self.fetch_and_display()
            
            # Wait for refresh interval with responsive shutdown
            if self.stop_event.wait(self.refresh_interval):
                break
    
    def refresh_once(self):
        """Refresh data once."""
        if not self.is_running:
            self.status_label.config(text="Status: Fetching...", fg="#f39c12")
            self.root.update()
            
            # Run in a thread to prevent GUI freezing
            thread = threading.Thread(target=self.fetch_and_display, daemon=True)
            thread.start()
    
    def fetch_and_display(self):
        """Fetch and display cryptocurrency data."""
        cryptos = self.tracker.fetch_top_cryptos()
        
        if cryptos:
            # Update UI in main thread
            self.root.after(0, self.update_table, cryptos)
        else:
            self.root.after(0, self.show_error)
    
    def update_table(self, cryptos):
        """Update the table with new data."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert new data
        for crypto in cryptos:
            rank = crypto.get('market_cap_rank', 'N/A')
            name = crypto.get('name', 'Unknown')
            symbol = crypto.get('symbol', 'N/A').upper()
            price = self.tracker.format_price(crypto.get('current_price'))
            change_24h = self.tracker.format_percentage(crypto.get('price_change_percentage_24h'))
            market_cap = self.tracker.format_number(crypto.get('market_cap'))
            volume_24h = self.tracker.format_number(crypto.get('total_volume'))
            
            # Add color tags for price change
            tag = "positive" if crypto.get('price_change_percentage_24h', 0) >= 0 else "negative"
            
            self.tree.insert(
                "",
                tk.END,
                values=(rank, name, symbol, price, change_24h, market_cap, volume_24h),
                tags=(tag,)
            )
        
        # Configure tags for colors
        self.tree.tag_configure("positive", foreground="#27ae60")
        self.tree.tag_configure("negative", foreground="#e74c3c")
        
        # Update timestamp
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.update_time_label.config(text=f"Last Updated: {now}")
        
        if not self.is_running:
            self.status_label.config(text="Status: Idle", fg="#7f8c8d")
    
    def show_error(self):
        """Show error message."""
        if not self.is_running:
            self.status_label.config(text="Status: Failed to fetch data", fg="#e74c3c")
            messagebox.showerror("Error", "Failed to fetch cryptocurrency data. Please check your internet connection.")
    
    def on_closing(self):
        """Handle window closing."""
        self.is_running = False
        self.stop_event.set()
        self.root.destroy()


def run_gui():
    """Run the GUI application."""
    root = tk.Tk()
    app = CryptoTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
