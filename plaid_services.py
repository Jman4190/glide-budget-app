import os
from dotenv import load_dotenv
load_dotenv()
import math
import datetime
from plaid import Client as PlaidClient

PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
PLAID_ENV = os.getenv('PLAID_ENV')
BOFA_ACCESS_TOKEN=os.getenv('BOFA_ACCESS_TOKEN')
CHASE_ACCESS_TOKEN=os.getenv('CHASE_ACCESS_TOKEN')
#VENMO_ACCESS_TOKEN=os.getenv('VENMO_ACCESS_TOKEN')

plaid_client = PlaidClient(client_id=PLAID_CLIENT_ID, 
                    secret=PLAID_SECRET, 
                    public_key=PLAID_PUBLIC_KEY, 
                    environment=PLAID_ENV)


# https://plaid.com/docs/api/#transactions
MAX_TRANSACTIONS_PER_PAGE = 500
OMIT_CATEGORIES = ["Transfer", "Credit Card", "Deposit"]
#OMIT_CATEGORIES = ["Transfer", "Credit Card", "Deposit", "Payment"]
OMIT_ACCOUNT_SUBTYPES = ['cd', 'savings']

def get_some_transactions(access_token, start_date, end_date):
    account_ids = [account['account_id'] for account in plaid_client.Accounts.get(access_token)['accounts']
                   #if account['subtype'] not in ['cd', 'savings']]
                   if account['subtype'] not in OMIT_ACCOUNT_SUBTYPES]
    
    num_available_transactions = plaid_client.Transactions.get(access_token, start_date, end_date,
                                                               account_ids=account_ids)['total_transactions']
    num_pages = math.ceil(num_available_transactions / MAX_TRANSACTIONS_PER_PAGE)
    transactions = []

    for page_num in range(num_pages):
        transactions += [transaction
                         for transaction in plaid_client.Transactions.get(access_token, start_date, end_date,
                                                                          account_ids=account_ids,
                                                                          offset=page_num * MAX_TRANSACTIONS_PER_PAGE,
                                                                          count=MAX_TRANSACTIONS_PER_PAGE)['transactions']
                         if transaction['pending'] is False and
                            (transaction['category'] is None
                            or not any(category in OMIT_CATEGORIES
                                        for category in transaction['category']))]
                                    

    return transactions

# get five days ago so we don't deal with pending costs
def get_five_days_ago_transactions():
    five_days_ago = (datetime.date.today() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    print(five_days_ago)
    transactions = []

    for access_id in [os.getenv('CHASE_ACCESS_TOKEN'), os.getenv('BOFA_ACCESS_TOKEN')]:
        #transactions += get_transactions_from_multiple_accounts(access_id, yesterday, yesterday)
        transactions += get_some_transactions(access_id, five_days_ago, five_days_ago)
        
    return transactions
