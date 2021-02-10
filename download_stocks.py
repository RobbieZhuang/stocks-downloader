import yfinance as yf
import csv

# Specify a maximum and minimum price for the stocks you want to look at
MAX_PRICE = 10
MIN_PRICE = 5

# Specify when you want to see stocks from the current date
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
PERIOD = '1mo'

# Specify the granularity
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
INTERVAL = "5m"

# Save pre-market and post-market hours data
DOWNLOAD_PREPOST = True

# List of files to obtain ticker names from
# Where to download updated ticker data
# TODO: Automate this
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=nyse&letter=0&render=download
# https://www.nasdaq.com/market-activity/stocks/screener?exchange=amex&letter=0&render=download
TICKER_FILES = ['ticker_data/' + s for s in ['AMEX.csv', 'NASDAQ.csv', 'NYSE.csv']]


# Downloads the data for a given stock and saves it into a csv file
def save_stock_data(tickers_list: list[str]) -> None:

  # Create a new csv for every ticker
  for ticker in tickers_list:
    data = yf.download(tickers=ticker, period=PERIOD, interval=INTERVAL, group_by='ticker', prepost=DOWNLOAD_PREPOST, threads=True)

    if data.empty:
      # Print an error message if the data is not found
      print(f'{ticker} was not downloaded.')
    else:
      filename = f'data/${ticker}-{PERIOD}-{INTERVAL}.csv'
      data.to_csv(filename)

# Returns a list of stocks which are within a given price range at present time
def get_stock_tickers(max: int, min: int = 0) -> list():
  tickers = set()
  for ticker_file in TICKER_FILES:
    with open(ticker_file) as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      idx = 0
      for row in csv_reader:
        if idx > 0:
          price = float(row['Last Sale'][1:])
          if price >= min and price <= max:
            tickers.add(row['Symbol'])
        idx += 1

  return tickers


if __name__ == '__main__':
    tickers = get_stock_tickers(MAX_PRICE, MIN_PRICE)
    save_stock_data(tickers)
