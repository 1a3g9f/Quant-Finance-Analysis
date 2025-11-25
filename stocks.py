import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
df_infy = pd.read_csv("INFY Historical Data.csv")
df_reli = pd.read_csv("RELI Historical Data.csv")

print(df_infy)
print(df_reli)


# Clean the data
# Convert 'Price' to numeric by removing commas
df_infy['Price'] = pd.to_numeric(df_infy['Price'].str.replace(',', ''), errors='coerce')
df_reli['Price'] = pd.to_numeric(df_reli['Price'].str.replace(',', ''), errors='coerce')
# Drop NaN values
df_infy = df_infy.dropna()
df_reli = df_reli.dropna()

# Create histogram data for INFY
n_bins = 10  # Number of bins
frequencies_infy, bins_infy, _ = plt.hist(df_infy['Price'], bins=n_bins, histtype='bar', color='#FF9999', alpha=0.7, label='INFY Histogram', edgecolor='black')

# Create histogram data for RELI
frequencies_reli, bins_reli, _ = plt.hist(df_reli['Price'], bins=n_bins, histtype='bar', color='#99FF99', alpha=0.7, label='RELI Histogram', edgecolor='black')

# Calculate bin centers for the polygon lines
bin_centers_infy = (bins_infy[:-1] + bins_infy[1:]) / 2
bin_centers_reli = (bins_reli[:-1] + bins_reli[1:]) / 2

# Plot the histogram polygons (lines over the histograms)
plt.plot(bin_centers_infy, frequencies_infy, '-o', color="#7940FF", label='INFY Polygon', linewidth=2, markersize=6)
plt.plot(bin_centers_reli, frequencies_reli, '-o', color="#FFD640", label='RELI Polygon', linewidth=2, markersize=6)

# Customize the plot
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('INFY and RELI Stock Price Histogram with Polygons')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()