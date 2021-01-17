
""" ***************************************************************************
# * File Description:                                                         *
# * MUse to determine the optimal portfolio along its weights.                *
# * The original script was taken from a YouTuber with account name Computer  *
# * Science. You can find the link to his video on the README.                *
# *                                                                           *
# * The contents of this script are:                                          *
# * 1. Importing Libraries                                                    *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Frank Ceballos <frank.ceballos89@gmail.com>                   *
# * --------------------------------------------------------------------------*
# * DATE CREATED:January 17, 20221                                            *
# * --------------------------------------------------------------------------*
# * NOTES: None                                                               *
# * ************************************************************************"""


###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
import pandas as pd
import numpy as np
import requests


###############################################################################
#                        2. Load Data and Shape Data                          #
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
