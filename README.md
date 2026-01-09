# CoinTrack 💰

A modern, responsive cryptocurrency tracking application that displays real-time market data for the top 20 cryptocurrencies by market cap.

![CoinTrack](https://img.shields.io/badge/status-live-brightgreen)
![GitHub Pages](https://img.shields.io/badge/deployed-GitHub%20Pages-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

## 🚀 Live Demo

Visit the live application: [https://v0idsh0id.github.io/CoinTrack/](https://v0idsh0id.github.io/CoinTrack/)

## ✨ Features

### Real-Time Cryptocurrency Tracking
- **Top 20 Cryptocurrencies**: Displays the most popular coins by market cap
- **Live Price Updates**: Auto-refreshes data every 60 seconds
- **Comprehensive Data**: Shows price, market cap, volume, 24h/7d changes, and circulating supply
- **Coin Icons**: Visual identification with official cryptocurrency logos

### User Interface
- **Responsive Design**: Optimized for mobile phones, tablets, and desktops
- **Dark Mode**: Toggle between light and dark themes (saves preference)
- **Two View Modes**: 
  - Desktop: Full-featured sortable table
  - Mobile: Card-based layout for easy touch interaction
- **Search Functionality**: Filter coins by name or symbol
- **Sortable Columns**: Click column headers to sort data
- **Color-Coded Changes**: Green for gains, red for losses
- **Loading States**: Visual feedback during data fetching
- **Error Handling**: Graceful error messages for API failures
- **Offline Detection**: Banner notification when internet connection is lost

### Performance & Optimization
- **Pure Vanilla JavaScript**: No frameworks or build process required
- **Fast Loading**: Minimal dependencies, quick page loads
- **API Rate Limiting Awareness**: Respects CoinGecko API limits
- **Efficient Rendering**: Optimized DOM updates
- **Auto-Pause**: Stops refreshing when tab is hidden to save resources

## 🛠️ Technology Stack

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS variables for theming
- **Vanilla JavaScript**: Pure ES6+ JavaScript, no frameworks
- **CoinGecko API**: Free cryptocurrency data API
- **GitHub Pages**: Static site hosting

## 📦 Installation & Setup

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API data

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/v0idsh0id/CoinTrack.git
   cd CoinTrack
   ```

2. **Open the application**
   - Simply open `index.html` in your web browser
   - Or use a local web server:
     ```bash
     # Using Python 3
     python -m http.server 8000
     
     # Using Node.js (npx)
     npx serve
     
     # Using PHP
     php -S localhost:8000
     ```
   - Then visit `http://localhost:8000` in your browser

### GitHub Pages Deployment

This application is designed to be deployed on GitHub Pages with zero configuration:

1. **Fork or Clone this repository**
   - Fork the repository to your GitHub account, or
   - Push your local copy to a new GitHub repository

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Navigate to **Settings** > **Pages**
   - Under "Source", select the branch you want to deploy (usually `main` or `master`)
   - Click **Save**

3. **Access your deployed site**
   - After a few minutes, your site will be live at:
     `https://[your-username].github.io/[repository-name]/`

4. **Update the README** (optional)
   - Update the live demo link in this README to point to your deployment

## 📱 Mobile Optimization

The application is fully optimized for mobile devices:

- **Touch-Friendly**: Large tap targets and smooth scrolling
- **Responsive Layout**: Adapts to any screen size
- **Fast Loading**: Optimized for mobile networks
- **Readable Typography**: Properly sized fonts for mobile viewing
- **Card Layout**: Mobile users see an easy-to-read card interface
- **Offline Support**: Detects and notifies when offline

## 🎨 Customization

### Changing Refresh Interval

Edit the `CONFIG` object in `script.js`:

```javascript
const CONFIG = {
    REFRESH_INTERVAL: 60000, // Change to desired milliseconds (e.g., 30000 for 30 seconds)
    // ...
};
```

### Changing Number of Cryptocurrencies

Edit the `CONFIG.PARAMS` in `script.js`:

```javascript
const CONFIG = {
    // ...
    PARAMS: {
        per_page: 20, // Change to desired number (max 250)
        // ...
    }
};
```

### Styling

All styles are in `styles.css`. The application uses CSS variables for theming:

```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #212529;
    /* Modify these variables to customize colors */
}
```

## 🔌 API Information

This application uses the [CoinGecko API](https://www.coingecko.com/en/api):

- **No API Key Required**: Free tier doesn't require authentication
- **Rate Limits**: 10-50 calls/minute (free tier)
- **Endpoint Used**: `/coins/markets`
- **Documentation**: [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation)

**Note**: If you exceed rate limits, you may receive HTTP 429 errors. The app handles this gracefully with error messages.

## 📊 Data Displayed

For each cryptocurrency, the application shows:

- **Rank**: Market cap ranking
- **Name & Symbol**: Full name and ticker symbol
- **Icon**: Official cryptocurrency logo
- **Current Price**: In USD
- **24h Change**: Price change in percentage and absolute value
- **7d Change**: 7-day price change percentage
- **Market Cap**: Total market capitalization
- **Volume (24h)**: 24-hour trading volume
- **Circulating Supply**: Amount of coins in circulation

## 🐛 Troubleshooting

### Data Not Loading
- Check your internet connection
- Verify the CoinGecko API is accessible: https://api.coingecko.com/api/v3/ping
- Check browser console for error messages
- Wait a few minutes if you've hit rate limits

### Dark Mode Not Saving
- Ensure your browser allows localStorage
- Check if you're in private/incognito mode (some browsers restrict localStorage)

### Display Issues
- Clear your browser cache
- Try a different browser
- Ensure JavaScript is enabled
- Check for browser console errors

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) for providing the free cryptocurrency API
- Cryptocurrency icons provided by CoinGecko
- Inspired by various crypto tracking applications

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Disclaimer**: This application is for informational purposes only. Cryptocurrency prices are volatile and past performance does not guarantee future results. Always do your own research before making investment decisions.