import yfinance as yf

symbol ="BTC"
eth = yf.download(tickers = f"{symbol}-USD",period="1d",interval="1d",)

print(eth["Volume"].values[0])
