
""" ***************************************************************************
# * File Description:                                                         *
# * MUse to determine the optimal portfolio along its weights.                *
# * The original script was taken from a YouTuber with account name Computer  *
# * Science. You can find the link to his video on the README.                *
# *                                                                           *
# * The contents of this script are:                                          *
# * 1. Importing Libraries                                                    *
# * 2. Helper Function                                                        *
# * 3. Load Data and Shape Data                                               *
# * 4. Optimized Portfolio                                                    *
# * 5. Get Discrete Allocation                                                *
# * 6. Helper Function                                                        *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Frank Ceballos <frank.ceballos89@gmail.com>                   *
# * --------------------------------------------------------------------------*
# * DATE CREATED:January 17, 2021                                             *
# * --------------------------------------------------------------------------*
# * NOTES: None                                                               *
# * ************************************************************************"""


###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
import pandas as pd
import requests
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


###############################################################################
#                             2. Helper Function                              #
###############################################################################
def get_company_names(symbol):
    "Get company name based on symbol/ticker-label"
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+symbol+"&region=1&lang=en"
    result = requests.get(url).json()
    return result["ResultSet"]["Result"][0]["name"]       
        

###############################################################################
#                        3. Load Data and Shape Data                          #
###############################################################################

# Load data
df = pd.read_csv("stock_data.csv")

# Replace index with date
df.set_index(keys = ["Date"], drop = True, inplace = True)

# Remove columns that are not the Close price
col= list(df.columns)
selected_cols = [column for column in col if "Close" in column]
selected_cols = [column for column in selected_cols if "Adj" not in column]
df = df[selected_cols]

# Rename columns
rename_col = [column.replace(" Close", "") for column in selected_cols]
df.columns = rename_col


###############################################################################
#                           4. Optimized Portfolio                            #
###############################################################################

# Calculate the expected annualized returns and the annualized sample covariance
# Matrix of the daily asset returns

mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimize for the maximal Sharpe ratio. The Sharpe ratio describes how much
# excess return you recieve for the extra volatility you endure for holding 
# a riskier asset

ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe() # Maximize sharpe ratio and get asset weights
cleaned_weights = ef.clean_weights()

# Show portfolio performance
ef.portfolio_performance(verbose = True) # Any Sharpe ratio greater than 1 
                                         # is considered acceptable


###############################################################################
#                         5. Get Discrete Allocation                          #
###############################################################################

# Get allocation of each share per stock
portfolio_val = 10000  # Initial investment in USD
latest_prices = get_latest_prices(df)
weights = cleaned_weights
da =  DiscreteAllocation(weights, latest_prices, 
                         total_portfolio_value = portfolio_val)
allocation, leftover = da.lp_portfolio()

# Message to user
print(f"Discrete allocation: {allocation}")
print(f"Remaning Fund: ${leftover}")


###############################################################################
#                             6. Helper Function                              #
###############################################################################
# Store company names into a list
company_list = [get_company_names(symbol) for symbol in allocation]

# Get discrete allocation values
discrete_allocation_list = [allocation.get(symbol) for symbol in allocation]  

# Create a dataframe for the portfolio
portfolio_df = pd.DataFrame(columns = ["Company_Name", "Company_Ticker", 
                                       "Discrete_val_"+str(portfolio_val)])

portfolio_df["Company_Name"] = company_list
portfolio_df["Company_Ticker"] = allocation
portfolio_df["Discrete_val_"+str(portfolio_val)] = discrete_allocation_list

print(portfolio_df)
