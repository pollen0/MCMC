import yfinance as yf
import pandas as pd

# Download data from Yahoo Finance
data = yf.download("QQQ", start="2024-01-01", end="2024-08-01")
data = data.drop(columns=["Volume", "Adj Close", "High", "Low"])

# Same day percent change within trading hours
sd_pc = (data["Close"] / data["Open"]) - 1
data["SD Percent Change"] = sd_pc

# Percent change from overnight
ovn_pc = ((data["Open"].shift(-1) / data["Close"]) - 1).shift(1) * 100
data["Overnight PC"] = ovn_pc

# Create ranges to divide the percentage changes into 8 even groups
data["Quantile"] = pd.qcut(data["Overnight PC"], 8, labels=False)
quantile_ranges = data.groupby("Quantile")["Overnight PC"].agg(["min", "max"]).reset_index()

# Classify each of the data groups
def classify(value, quantile_ranges):
    for _, row in quantile_ranges.iterrows():
        if row['min'] <= value <= row['max']:
            return f"Quantile {int(row['Quantile']) + 1}"  # +1 to make it 1-based instead of 0-based
    return "Out of Range"

# Apply the classify function to each value in "Overnight PC"
data["Classify"] = data["Overnight PC"].apply(classify, args=(quantile_ranges,))

# Display the updated DataFrame
print(data.head())
