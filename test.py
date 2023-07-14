import yfinance as yf

ticker = yf.Ticker('GOOGL').info
print(ticker)
market_price = ticker['currentPrice']
previous_close_price = ticker['regularMarketPreviousClose']
print('Ticker: GOOGL')
print('Market Price:', market_price)
print('Previous Close Price:', previous_close_price)