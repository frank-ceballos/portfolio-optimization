import pandas as pd

# To grab stock data
import yfinance as fyf
from pandas_datareader import data as pdr
fyf.pdr_override() # <-- Here is the fix

# To create datetime objects 
import datetime
from datetime import date, timedelta

# Import SPIndex object
from data.data import SPIndex


def get_data():
    # Get index
    spindex = SPIndex()
    
    # Get ticker labels
    stocks = spindex.tickers
    
    # Yahoo Finance
    # Set start and end dates
    start = datetime.datetime(2010, 1, 1)
    end   = date.today() - timedelta(days=1)
    
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
    df.to_csv('stock_data.csv')

# Create database. Run this file to recreate the whole database
get_data()
