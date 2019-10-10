import os
import datetime
import pandas as pd
from plaid_services import get_five_days_ago_transactions, get_some_transactions
from dataframe_services import convert_to_df, filter_df
from gsheets_services import insert2gsheet, get_google_sheet_id, get_gsheet_length

# get transaction data from 5 days ago
transaction_data = get_five_days_ago_transactions()
# convert data to a dataframe
transaction_df = convert_to_df(transaction_data)
# filter dataframe based on specific columns
filtered_transactions = filter_df(transaction_df)
# get google sheet id
sheet_id = get_google_sheet_id('transactions')
# get current sheet length for row insert
length = get_gsheet_length()
# insert data into google sheet
done = insert2gsheet(filtered_transactions, sheet_id, length)
# add response for insert2gsheet that returns successful or not
# if return successful, nothing, if unsuccessful, send email?
print('Done')
