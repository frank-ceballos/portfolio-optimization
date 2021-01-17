import pandas as pd

# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# To create datetime objects 
import datetime

# Import SPIndex object
from data.data import SPIndex


def get_data():
    # Get index
    spindex = SPIndex()
    
    # Get ticker labels
    stocks = spindex.tickers
    
    # Yahoo Finance
    # Set start and end dates
    start = datetime.datetime(2000, 1, 1)
    end   = datetime.datetime(2020, 6, 8)
    
    # Grab data
    data = pdr.get_data_yahoo(stocks, start = start, end = end)
    
    # Decompose data
    values = data.values
    dates = data.index
    
    # Get columns labels
    columns = data.columns.tolist()
    columns = [column[1] + ' ' + column[0] for column in columns]
    
    # Put dataframe
    df = pd.DataFrame(values, columns = columns, index = dates)
    
    # Save file
    df.to_csv('data\\' + 'stock_data.csv')

# Create database. Run this and leave untouched unless you want to update the
# data
get_data()
