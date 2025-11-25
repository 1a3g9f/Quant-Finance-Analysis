import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize
from fredapi import Fred
from matplotlib import pyplot as plt

#define the list of tickers

tickers = ['INFY.NS', 'RELIANCE.NS']

end_date = datetime.today()

start_date = end_date - timedelta(days = 3 * 365)
print(start_date)

#create an empty DataFrame to store the adjusted close prices

adj_close_df = pd.DataFrame()

#download the close prices for each ticker

for ticker in tickers:
    data = yf.download(ticker, start = start_date , end = end_date)
    if not data.empty:  # Check if data is downloaded
        adj_close_df[ticker] = data['Close']
    else:
        print(f"No data found for {ticker}")
print(adj_close_df)
#calculate the lognormal returns for each ticker

log_returns = np.log(adj_close_df/adj_close_df.shift(1))
#drop any missing values

log_returns = log_returns.dropna()
print(log_returns)

# Calculate individual asset metrics for debugging
annual_mean = log_returns.mean() * 252
annual_std = log_returns.std() * np.sqrt(252)
print("Annual Mean Returns:\n", annual_mean)
print("Annual Std (Volatility):\n", annual_std)

#calculate the covariance matrix using annualized log returns

cov_matrix = log_returns.cov() * 252
print(cov_matrix)

#calculate the portfolio risk measuring by standard deviation

def std_dev(weights , cov_matrix):
    var = weights.T @ cov_matrix @ weights     #transpose
    return np.sqrt(var)

#calculate the expected return

def expected_return(weights,log_returns):
    return np.sum(log_returns.mean()*weights)*252

#calculate the sharpe ratio

def sp_ratio(weights , log_returns , cov_matrix, risk_free_ratio):
    return (expected_return(weights , log_returns) - risk_free_rate) / std_dev(weights,cov_matrix)

#set the risk-free rate

fred=Fred(api_key = 'f559302a905fa971442a68e1a11e1b0c')
ten_year_treasury_rate = fred.get_series_latest_release('GS10')/100

risk_free_rate = ten_year_treasury_rate.iloc[-1]
print(risk_free_rate)

def neg_sp_ratio(weights , log_returns , cov_matrix , risk_free_rate):
    return -sp_ratio(weights , log_returns , cov_matrix , risk_free_rate)


constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0.3, 0.7) for _ in range(len(tickers))]

#set the initial weights

initial_weights = np.array([1/len(tickers)]*len(tickers))
print(initial_weights)

#optimizing the weights to maximize sharpe ratio

optimized_results = minimize(neg_sp_ratio, initial_weights , args=(log_returns , cov_matrix , risk_free_rate) , method = "SLSQP" , constraints=constraints , bounds=bounds)

optimal_weights = optimized_results.x

print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

optimal_portfolio_return = expected_return(optimal_weights, log_returns)
optimal_portfolio_volatility = std_dev(optimal_weights, cov_matrix)
optimal_sharpe_ratio = sp_ratio(optimal_weights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volatility: {optimal_portfolio_volatility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")

# Create a table of returns and volatility
stats_table = pd.DataFrame({
    'Annualized Return (%)': annual_mean * 100,
    'Annualized Volatility (%)': annual_std * 100,
    'Optimal Weight (%)': optimal_weights * 100
}, index=tickers)
print("\nReturns and Volatility Table:")
print(stats_table.round(2))

# Plot daily returns
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(log_returns.index, log_returns[ticker], label=ticker)
plt.xlabel('Date')
plt.ylabel('Daily Log Returns')
plt.title('Daily Returns of Infosys and Reliance')
plt.legend()
plt.grid(True)
plt.show()

#Combined plot of optimal weights with returns as annotations
plt.figure(figsize=(10, 6))
bars = plt.bar(tickers, optimal_weights, color=['#1f77b4', '#ff7f0e'])
plt.xlabel('Assets')
plt.ylabel('Optimal Weights')
plt.title('Optimal Portfolio Weights with Returns')

# Annotate bars with annualized returns
for bar, ret in zip(bars, annual_mean * 100):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{ret:.1f}%',
             ha='center', va='bottom')

plt.ylim(0, 1)  # Ensure weights are between 0 and 1
plt.show()
