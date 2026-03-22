#!pip install yfinance
#!pip install bsedata
from bsedata.bse import BSE
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date

# STOCK DATA 
tickers = ["SBIN.NS", "ICICIBANK.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "HCLTECH.NS"]
end = date.today()
start = date(2018,1,1)

data = yf.download(tickers, start=start, end=end)

# format data
df = data.stack(level=1).reset_index()
df = df.sort_values(["Ticker", "Date"])

# Daily return
df['Prev_close'] = df.groupby('Ticker')['Close'].shift(1)
df['Daily_return'] = (df['Close'] - df['Prev_close']) / df['Prev_close'] * 100

# Moving averages
df['MA_20'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).mean())
df['MA_50'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(50).mean())

# High-Low %
df['HL_pct'] = (df['High'] - df['Low']) / df['Prev_close'] * 100

# Volatility
df['Volatility_20d'] = df.groupby('Ticker')['Daily_return'].transform(lambda x: x.rolling(20).std())

# MA Signal
df["MA_Signal"] = df["MA_20"] > df["MA_50"]

# Sharpe Ratio
df["Return_DecimalW"] = df["Daily_return"] / 100
df["Rolling_Mean_20W"] = df.groupby("Ticker")["Return_DecimalW"].transform(lambda x: x.rolling(20).mean())
df["Rolling_Std_20W"] = df.groupby("Ticker")["Return_DecimalW"].transform(lambda x: x.rolling(20).std())

rf_daily = 0.07 / 252
df["Sharpe_20D"] = (df["Rolling_Mean_20W"] - rf_daily) / df["Rolling_Std_20W"] * np.sqrt(252)

# Volume spike
df['Avg_volm20W'] = df.groupby('Ticker')['Volume'].transform(lambda x: x.rolling(20).mean())
df['Volm_ratio'] = df['Volume'] / df['Avg_volm20W']
df['Volm_spiked'] = df['Volm_ratio'] > 1.4

# Clean
df = df.dropna()

# SAVE inside data folder
df.to_csv("data/stock_analysis.csv", index=False)
print("stock_analysis.csv saved successfully")

________________________________________________________________________________
# GETTING THE DATA OF GOLD SILVER AND INDEXES (BANKNIFTY & NIFTY, GOLD & SILVER)
tickers = ["^NSEBANK", "^NSEI", "GC=F", "SI=F"]  # ^ symbol for indices

end = date.today()
start = date(2018,1,1)

data2 = yf.download(tickers, start=start, end=end)

df2 = data2.stack(level=1).reset_index()
df2 = df2.sort_values(["Ticker", "Date"])

df2['Prev_close'] = df2.groupby('Ticker')['Close'].shift(1)
df2['Daily_return'] = (df2['Close']-df2['Prev_close']) / df2['Prev_close'] * 100

# 20 & 50 day MA for commodities
df2['MA_20'] = df2.groupby('Ticker')['Close'].transform(lambda x: x.rolling(20).mean())
df2['MA_50'] = df2.groupby('Ticker')['Close'].transform(lambda x: x.rolling(50).mean())
df2.to_csv("data/Gold_silver_analysis.csv", index=False)

__________________________  
#TOP GAINERS & LOSERS DATA

b = BSE()
losers = pd.DataFrame(b.topLosers())
gainers = pd.DataFrame(b.topGainers())

losers['Category'] = 'Loser'
gainers['Category'] = 'Gainer'

combined = pd.concat([losers, gainers], ignore_index=True)
combined.to_csv(r"data\gainers_losers.csv", index=False)

print("Gainers/Losers file saved")
  
____________________________________________
# TOP 5 STOCKS NEWS (BAKING AND IT SECTOR)

stock_analysis = pd.read_csv('data/stock_analysis.csv')
tickers = stock_analysis['Ticker'].unique().tolist()

all_news = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    
    try:
        news = stock.news[:5]
        
        if news:
            news_df = pd.json_normalize(news)
            
            final_df = news_df[[
                'content.title',
                'content.pubDate', 
                'content.clickThroughUrl.url',
                'content.provider.displayName'
            ]].copy()
            
            final_df.columns = ['Title', 'Date', 'Article URL', 'Provider']
            final_df['Ticker'] = ticker

            final_df = final_df[['Title', 'Ticker', 'Date', 'Provider', 'Article URL']]
            all_news.append(final_df)
            
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")

# Combine
if all_news:
    combined_news = pd.concat(all_news, ignore_index=True)
    combined_news.to_csv("data/stock_news.csv", index=False)
    print("stock_news.csv saved successfully")
else:
    print("No news found")

_________________________________-
# GOLD_SILVER TOP 5 NEWS

stock_analysis = pd.read_csv("data/Gold_silver_analysis.csv")
tickers = stock_analysis['Ticker'].unique().tolist()

all_news = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    
    try:
        news = stock.news[:5]
        
        if news:
            news_df = pd.json_normalize(news)
            
            final_df = news_df[[
                'content.title',
                'content.pubDate', 
                'content.clickThroughUrl.url',
                'content.provider.displayName'
            ]].copy()
            
            final_df.columns = ['Title', 'Date', 'Article URL', 'Provider']
            final_df['Ticker'] = ticker

            final_df = final_df[['Title', 'Ticker', 'Date', 'Provider', 'Article URL']]
            all_news.append(final_df)
            
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")

# Combine
if all_news:
    combined_news = pd.concat(all_news, ignore_index=True)
    combined_news.to_csv("data/Gold_silver_news.csv", index=False)
    print("Gold_silver_news.csv saved successfully ✅")
else:
    print("No news found ❌")

__________________________  
# HOURLY DATA OF STOCKS 

tickers = ["SBIN.NS", "ICICIBANK.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "HCLTECH.NS"]
start = "2025-01-01"
end = date.today()

try:
    # Download hourly data
    data = yf.download(tickers, start=start, end=end, interval="1h")

    df = data.stack(level=1).reset_index()
    df = df.rename(columns={"level_1": "Ticker"})
    df = df.sort_values(["Ticker", "Datetime"])

    # Convert to Indian Time
    df["Datetime"] = df["Datetime"].dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)

    df["Date"] = df["Datetime"].dt.date
    df["Hour"] = df["Datetime"].dt.hour

    # Hourly return
    df["Hourly_Return"] = df.groupby("Ticker")["Close"].pct_change()

    # Volume change %
    df["Volume_Change_%"] = df.groupby("Ticker")["Volume"].pct_change() * 100

    # Hour-wise Volatility
    df["Hourly_Volatility"] = (df.groupby(["Ticker", "Hour"])["Hourly_Return"].transform("std"))

    # Clean
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()
    
    df.to_csv("data/hourly_price_table.csv", index=False)
    print("hourly_price_table.csv saved successfully")

except Exception as e:
    print("Error occurred:", e)
