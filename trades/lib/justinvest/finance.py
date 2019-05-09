# Standard library imports
from datetime import date, timedelta

# Third party imports
import pandas as pd
from pandas_datareader.data import DataReader


def is_ticker_existing(ticker):
    """
    Returns :
        - True if the given ticker is found on yahoo finance
        - False otherwise
    """
    try:
        DataReader(ticker, 'yahoo', start=date(2019,1,1))
        return True
    except:
        return False

def index_to_unix(row):
    row.unix = row.unix.value // 10**6
    return row

def get_ohlc_quote(ticker, start_year=2017):
    """
    Returns a list of quotes (Date, Open, High, Low, Close) values
    with a date in unix timestamp format.
    """
    start_date = date(start_year,1,1)
    stock_data_df = DataReader(ticker, 'yahoo', start=start_date)
    # add a column in unix timestamp format
    stock_data_df['unix'] = stock_data_df.index
    stock_data_df = stock_data_df.apply(index_to_unix, axis='columns')
    values_list = stock_data_df.loc[:,['unix', 'Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
    return values_list

def get_last_close(ticker):
    start_date = date.today() - timedelta(4)
    stock_data = DataReader(ticker, 'yahoo', start=start_date)
    last_close = float(stock_data.tail(1)['Close'])
    return last_close
