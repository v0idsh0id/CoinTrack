// ===========================
// Configuration & Constants
// ===========================
const CONFIG = {
    API_URL: 'https://api.coingecko.com/api/v3/coins/markets',
    REFRESH_INTERVAL: 60000, // 60 seconds
    PARAMS: {
        vs_currency: 'usd',
        order: 'market_cap_desc',
        per_page: 20,
        page: 1,
        sparkline: false,
        price_change_percentage: '7d'
    }
};

// ===========================
// State Management
// ===========================
let cryptoData = [];
let filteredData = [];
let currentSort = { field: 'market_cap_rank', direction: 'asc' };
let refreshInterval = null;

// ===========================
// DOM Elements
// ===========================
const elements = {
    loading: document.getElementById('loading'),
    error: document.getElementById('error-message'),
    container: document.getElementById('crypto-container'),
    tableBody: document.getElementById('crypto-table-body'),
    cards: document.getElementById('crypto-cards'),
    searchInput: document.getElementById('search-input'),
    lastUpdate: document.getElementById('last-update'),
    refreshBtn: document.getElementById('refresh-btn'),
    themeToggle: document.getElementById('theme-toggle'),
    offlineBanner: document.getElementById('offline-banner')
};

// ===========================
// Utility Functions
// ===========================

/**
 * Format number as currency (USD)
 */
function formatCurrency(value) {
    if (value === null || value === undefined) return 'N/A';
    
    if (value >= 1000000000) {
        return '$' + (value / 1000000000).toFixed(2) + 'B';
    } else if (value >= 1000000) {
        return '$' + (value / 1000000).toFixed(2) + 'M';
    } else if (value >= 1000) {
        return '$' + value.toLocaleString('en-US', { maximumFractionDigits: 2 });
    } else if (value >= 1) {
        return '$' + value.toFixed(2);
    } else {
        return '$' + value.toFixed(6);
    }
}

/**
 * Format large numbers with abbreviations
 */
function formatNumber(value) {
    if (value === null || value === undefined) return 'N/A';
    
    if (value >= 1000000000) {
        return (value / 1000000000).toFixed(2) + 'B';
    } else if (value >= 1000000) {
        return (value / 1000000).toFixed(2) + 'M';
    } else if (value >= 1000) {
        return value.toLocaleString('en-US', { maximumFractionDigits: 0 });
    }
    return value.toFixed(2);
}

/**
 * Format percentage with color coding
 */
function formatPercentage(value) {
    if (value === null || value === undefined) return 'N/A';
    
    const formatted = value.toFixed(2) + '%';
    const className = value >= 0 ? 'positive' : 'negative';
    const arrow = value >= 0 ? '▲' : '▼';
    
    return `<span class="${className}">${arrow} ${formatted}</span>`;
}

/**
 * Format timestamp to readable format
 */
function formatTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Show error message
 */
function showError(message) {
    elements.error.textContent = message;
    elements.error.classList.remove('hidden');
    elements.loading.classList.add('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    elements.error.classList.add('hidden');
}

// ===========================
// API Functions
// ===========================

/**
 * Build API URL with parameters
 */
function buildApiUrl() {
    const url = new URL(CONFIG.API_URL);
    Object.entries(CONFIG.PARAMS).forEach(([key, value]) => {
        url.searchParams.append(key, value);
    });
    return url.toString();
}

/**
 * Fetch cryptocurrency data from CoinGecko API
 */
async function fetchCryptoData() {
    try {
        hideError();
        
        const response = await fetch(buildApiUrl(), {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        if (!Array.isArray(data) || data.length === 0) {
            throw new Error('No data received from API');
        }

        return data;
    } catch (error) {
        console.error('Error fetching crypto data:', error);
        throw error;
    }
}

/**
 * Load and display cryptocurrency data
 */
async function loadCryptoData() {
    try {
        elements.loading.classList.remove('hidden');
        elements.container.classList.add('hidden');
        
        const data = await fetchCryptoData();
        cryptoData = data;
        filteredData = [...cryptoData];
        
        applySorting();
        renderCryptoData();
        updateLastUpdateTime();
        
        elements.loading.classList.add('hidden');
        elements.container.classList.remove('hidden');
    } catch (error) {
        showError('Failed to load cryptocurrency data. Please try again later.');
        console.error(error);
    }
}

// ===========================
// Rendering Functions
// ===========================

/**
 * Render cryptocurrency data in table and cards
 */
function renderCryptoData() {
    renderTable();
    renderCards();
}

/**
 * Render table view (desktop)
 */
function renderTable() {
    elements.tableBody.innerHTML = '';
    
    filteredData.forEach(coin => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${coin.market_cap_rank || 'N/A'}</td>
            <td>
                <div class="coin-info">
                    <img src="${coin.image}" alt="${coin.name}" class="coin-icon">
                    <div class="coin-name">
                        <strong>${coin.name}</strong>
                        <span class="coin-symbol">${coin.symbol}</span>
                    </div>
                </div>
            </td>
            <td>${formatCurrency(coin.current_price)}</td>
            <td>${formatPercentage(coin.price_change_percentage_24h)}</td>
            <td>${formatCurrency(coin.price_change_24h)}</td>
            <td>${formatPercentage(coin.price_change_percentage_7d_in_currency)}</td>
            <td>${formatCurrency(coin.market_cap)}</td>
            <td>${formatCurrency(coin.total_volume)}</td>
            <td>${formatNumber(coin.circulating_supply)} ${coin.symbol.toUpperCase()}</td>
        `;
        elements.tableBody.appendChild(row);
    });
}

/**
 * Render card view (mobile)
 */
function renderCards() {
    elements.cards.innerHTML = '';
    
    filteredData.forEach(coin => {
        const card = document.createElement('div');
        card.className = 'crypto-card';
        card.innerHTML = `
            <div class="card-header">
                <div class="card-coin-info">
                    <img src="${coin.image}" alt="${coin.name}" class="coin-icon">
                    <div class="coin-name">
                        <strong>${coin.name}</strong>
                        <span class="coin-symbol">${coin.symbol}</span>
                    </div>
                </div>
                <span class="card-rank">#${coin.market_cap_rank || 'N/A'}</span>
            </div>
            <div class="card-price">${formatCurrency(coin.current_price)}</div>
            <div class="card-details">
                <div class="card-detail">
                    <span class="card-detail-label">24h Change</span>
                    <span class="card-detail-value">${formatPercentage(coin.price_change_percentage_24h)}</span>
                </div>
                <div class="card-detail">
                    <span class="card-detail-label">7d Change</span>
                    <span class="card-detail-value">${formatPercentage(coin.price_change_percentage_7d_in_currency)}</span>
                </div>
                <div class="card-detail">
                    <span class="card-detail-label">Market Cap</span>
                    <span class="card-detail-value">${formatCurrency(coin.market_cap)}</span>
                </div>
                <div class="card-detail">
                    <span class="card-detail-label">Volume (24h)</span>
                    <span class="card-detail-value">${formatCurrency(coin.total_volume)}</span>
                </div>
                <div class="card-detail">
                    <span class="card-detail-label">Circulating Supply</span>
                    <span class="card-detail-value">${formatNumber(coin.circulating_supply)} ${coin.symbol.toUpperCase()}</span>
                </div>
            </div>
        `;
        elements.cards.appendChild(card);
    });
}

/**
 * Update last update timestamp
 */
function updateLastUpdateTime() {
    elements.lastUpdate.textContent = `Last updated: ${formatTimestamp()}`;
}

// ===========================
// Search Functionality
// ===========================

/**
 * Filter cryptocurrency data based on search query
 */
function filterData(searchQuery) {
    const query = searchQuery.toLowerCase().trim();
    
    if (!query) {
        filteredData = [...cryptoData];
    } else {
        filteredData = cryptoData.filter(coin => 
            coin.name.toLowerCase().includes(query) ||
            coin.symbol.toLowerCase().includes(query)
        );
    }
    
    applySorting();
    renderCryptoData();
}

// ===========================
// Sorting Functionality
// ===========================

/**
 * Get nested property value from object
 */
function getNestedValue(obj, path) {
    return path.split('.').reduce((current, prop) => current?.[prop], obj);
}

/**
 * Sort cryptocurrency data
 */
function applySorting() {
    filteredData.sort((a, b) => {
        const aVal = getNestedValue(a, currentSort.field);
        const bVal = getNestedValue(b, currentSort.field);
        
        // Handle null/undefined values
        if (aVal === null || aVal === undefined) return 1;
        if (bVal === null || bVal === undefined) return -1;
        
        const comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
        return currentSort.direction === 'asc' ? comparison : -comparison;
    });
}

/**
 * Handle column header click for sorting
 */
function handleSort(field) {
    if (currentSort.field === field) {
        // Toggle direction if same field
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        // New field, default to ascending
        currentSort.field = field;
        currentSort.direction = 'asc';
    }
    
    applySorting();
    renderCryptoData();
    updateSortIndicators();
}

/**
 * Update sort indicator icons
 */
function updateSortIndicators() {
    const headers = document.querySelectorAll('.crypto-table th[data-sort]');
    headers.forEach(header => {
        const indicator = header.querySelector('.sort-indicator');
        const field = header.dataset.sort;
        
        if (field === currentSort.field) {
            indicator.textContent = currentSort.direction === 'asc' ? '▲' : '▼';
            indicator.classList.add('active');
        } else {
            indicator.textContent = '⇅';
            indicator.classList.remove('active');
        }
    });
}

// ===========================
// Theme Management
// ===========================

/**
 * Initialize theme from localStorage or system preference
 */
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    setTheme(theme);
}

/**
 * Set theme and update UI
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    elements.themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
}

/**
 * Toggle between light and dark theme
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// ===========================
// Auto-refresh Management
// ===========================

/**
 * Start auto-refresh interval
 */
function startAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    
    refreshInterval = setInterval(() => {
        loadCryptoData();
    }, CONFIG.REFRESH_INTERVAL);
}

/**
 * Stop auto-refresh interval
 */
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

/**
 * Manual refresh handler
 */
async function handleRefresh() {
    elements.refreshBtn.classList.add('spinning');
    await loadCryptoData();
    
    // Remove spinning class after animation completes
    setTimeout(() => {
        elements.refreshBtn.classList.remove('spinning');
    }, 1000);
}

// ===========================
// Offline Detection
// ===========================

/**
 * Handle online/offline events
 */
function handleOnlineStatus() {
    if (navigator.onLine) {
        elements.offlineBanner.classList.add('hidden');
        startAutoRefresh();
    } else {
        elements.offlineBanner.classList.remove('hidden');
        stopAutoRefresh();
    }
}

// ===========================
// Event Listeners
// ===========================

/**
 * Initialize all event listeners
 */
function initEventListeners() {
    // Search input
    elements.searchInput.addEventListener('input', (e) => {
        filterData(e.target.value);
    });
    
    // Refresh button
    elements.refreshBtn.addEventListener('click', handleRefresh);
    
    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);
    
    // Table sorting
    const sortHeaders = document.querySelectorAll('.crypto-table th[data-sort]');
    sortHeaders.forEach(header => {
        header.addEventListener('click', () => {
            handleSort(header.dataset.sort);
        });
    });
    
    // Online/offline detection
    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOnlineStatus);
    
    // Page visibility - pause refresh when tab is hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopAutoRefresh();
        } else {
            startAutoRefresh();
        }
    });
}

// ===========================
// Initialization
// ===========================

/**
 * Initialize the application
 */
async function init() {
    try {
        // Initialize theme
        initTheme();
        
        // Check online status
        handleOnlineStatus();
        
        // Set up event listeners
        initEventListeners();
        
        // Load initial data
        await loadCryptoData();
        
        // Start auto-refresh
        startAutoRefresh();
        
        // Update sort indicators
        updateSortIndicators();
        
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to initialize the application. Please refresh the page.');
    }
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
