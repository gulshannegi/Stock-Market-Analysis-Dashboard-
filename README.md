Stock Market Analysis Dashboard (Python + Power BI)

**Overview**

This project is an end-to-end stock market analysis pipeline where I collected financial data, performed analysis using Python, and built an interactive Power BI dashboard.

It combines price data, technical indicators, risk metrics (volatility, Sharpe ratio), volume patterns, and news data to provide a complete view of stock performance and market behavior.

What I Did  

Extracted stock data using yfinance
Collected data for:
6 Stocks: SBIN, ICICI Bank, HDFC Bank, TCS, Infosys, HCL Tech
Indices & Commodities: NIFTY, BANK NIFTY, Gold, Silver
Cleaned and transformed data using pandas
Created key metrics: Daily Returns, Moving Averages (20 & 50), Volatility, Sharpe Ratio
Volume Spike Detection
Pulled top 5 news per stock
Extracted Top Gainers & Losers (BSE)
Generated hourly-level data for intraday analysis
Loaded all processed data into Power BI

**Dashboard**

The Power BI dashboard consists of the following pages:

KPI Overview-
  Last Day Close Price
  Average Volatility (Last 30 Days)
  Sharpe Ratio (20 Days)

Price Trend Analysis-
Moving Averages (20 & 50 Day)
Heatmap of Volume Spike Days 
Heatmap of Bullish Days Count (based on MA crossover)

News & Market Movers-
  Top 5 Latest News (Stocks, Indices, Commodities)
  Top Gainers and Losers

Intraday Analysis-
  Hourly Returns
  Hourly Volatility
  Volume Change Across Trading Hours

**Key Insights**

The project provides insights into volume behavior and volatility patterns across selected stocks (SBIN, ICICI Bank, HDFC Bank, TCS, Infosys, HCL Tech) and indices/commodities (NIFTY, BANK NIFTY, Gold, Silver).

Heatmaps help visualize the number of bullish days (MA20 > MA50) and volume spike days, making it easier to compare stock behavior across different years.

KPI metrics highlight important indicators such as:
Last 30-day price range
Volatility
Sharpe Ratio (risk-adjusted return measure: higher is better, negative indicates returns lower than risk-free rate)

News integration provides context behind price movements, while top gainers and losers help identify short-term momentum opportunities in the market.

Intraday analysis shows that:
Volume is typically higher near market close due to institutional activity and position squaring
Volatility is higher during opening hours, then stabilizes as the market progresses
Some IT stocks (TCS, Infosys, HCL Tech) show lower or negative Sharpe ratios, which may indicate:
Lower returns during the selected period
Higher relative volatility
Sector-specific underperformance in certain phases

Dashboard Preview
---

**Conclusion**
This project demonstrates how data from multiple financial sources can be combined into a single analytical pipeline. By integrating price data, technical indicators, volume patterns, and news, it provides a structured way to analyze market behavior and support data-driven decision making.
