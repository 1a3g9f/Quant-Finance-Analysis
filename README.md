# Quant-Finance-Analysis

### Project Description: Stock Analysis and Portfolio Optimization for INFY.NS and RELIANCE.NS

This is a compact Python-based stock analysis project focused on two major Indian stocks listed on the NSE:

- **INFY.NS** – Infosys Ltd.  
- **RELIANCE.NS** – Reliance Industries Ltd.

The project consists of three well-structured scripts that together provide historical price visualization, technical analysis, and quantitative portfolio optimization using Modern Portfolio Theory (MPT).

#### 1. risk_metrics.py – Portfolio Optimization & Risk Analysis
This is the core quantitative script that performs the following:

- Downloads 3 years of historical adjusted closing prices using yfinance
- Calculates daily log returns
- Computes annualized expected returns, volatility, and covariance matrix
- Fetches the latest US 10-year Treasury yield as a proxy for risk-free rate (via FRED API)
- Optimizes portfolio weights to maximize the Sharpe Ratio using scipy.optimize.minimize (SLSQP method)
- Applies realistic constraints:
  - Weights must sum to 100%
  - Each stock constrained between 30% and 70% (to avoid extreme corner solutions)
- Outputs:
  - Optimal portfolio weights
  - Expected annual return, volatility, and Sharpe ratio
  - Comparative table of individual asset metrics
  - Visualizations:
    - Daily log returns over time
    - Bar chart of optimal weights with annualized returns annotated on top

This script demonstrates practical application of Markowitz’s Efficient Frontier and Sharpe ratio maximization in the Indian equity context.

#### 2. stocks.py – Price Distribution Analysis
A simple exploratory script that:

- Loads historical price data from local CSV files
- Creates overlapping histograms showing the frequency distribution of closing prices for both stocks
- Overlays polygon lines (connected bin centers) for easier visual comparison of price density
- Helps understand the typical price ranges and skewness of each stock over the observed period

Useful for quick visual inspection of how concentrated trading prices have been historically.

#### 3. sma_ema.py – Technical Analysis on Reliance
Focuses on Reliance Industries with the following features:

- Loads and cleans historical data (handles Indian date format and comma-separated prices)
- Calculates:
  - 5-day and 10-day Simple Moving Averages (SMA)
  - 5-day and 10-day Exponential Moving Averages (EMA)
- Generates trading signals based on EMA crossover strategy:
  - EMA-5 > EMA-10 → Buy (Golden Cross)
  - EMA-5 < EMA-10 → Sell (Death Cross)
- Plots price along with all four moving averages
- Clean, publication-ready chart with proper legends and formatting

Ideal for traders interested in trend-following strategies using moving average crossovers.

