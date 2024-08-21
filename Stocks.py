import yfinance as yf
import pandas as pd


data = yf.download("QQQ", start = "2024-07-01", end = "2024-08-01")
data = data.drop(columns = ["Volume", "Adj Close", "High", "Low"])

#Same day percent change within trading hours
sd_percent_change = (data["Close"] / data["Open"]) - 1
data["SD Percent Change"] = sd_percent_change


#Percent change from overnight
pd_percent_change = (data["Open"][1:] / data["Close"][:-1]) - 1
pd_percent_change.add(0,0)


data["PD Percent Change"] = pd_percent_change


new_df = pd.DataFrame(data = {"Open": data["Open"][1:], "Close": data["Close"][:-1].shift(1)})


print(new_df.head(22))


