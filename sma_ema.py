import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare data
df = pd.read_csv("RELI Historical Data.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values('Date').reset_index(drop=True)

# Clean Price (remove commas, convert to float)
df['Price'] = df['Price'].str.replace(',', '').astype(float)

# Compute SMA and EMA
df['SMA_5'] = df['Price'].rolling(window=5).mean()  # 5-day SMA
df['EMA_5'] = df['Price'].ewm(span=5, adjust=False).mean()  # 5-day EMA
df['SMA_10'] = df['Price'].rolling(window=10).mean()  # 10-day SMA
df['EMA_10'] = df['Price'].ewm(span=10, adjust=False).mean()  # 10-day EMA 
# Generate signals based on EMA crossover
df['Signal'] = 'Hold'
df.loc[df['EMA_5'] > df['EMA_10'], 'Signal'] = 'Buy'  # Golden cross (bullish)
df.loc[df['EMA_5'] < df['EMA_10'], 'Signal'] = 'Sell'  # Death cross (bearish)

# Display results
print(df[['Date', 'Price', 'SMA_5', 'EMA_5', 'SMA_10', 'EMA_10', 'Signal']])


# Visualize the results
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Price'], label='Closing Price', color='blue')
plt.plot(df['Date'], df['SMA_5'], label='5-day SMA', color='green', linestyle='--')
plt.plot(df['Date'], df['EMA_5'], label='5-day EMA', color='lime')
plt.plot(df['Date'], df['SMA_10'], label='10-day SMA', color='red', linestyle='--')
plt.plot(df['Date'], df['EMA_10'], label='10-day EMA', color='orange')
plt.title('Reliance Stock: Price with SMA and EMA (Aug-Sep 2025)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()