import pandas as pd

# convert json response to dataframe
def convert_to_df(data):
   df = pd.DataFrame.from_records(data)
   return df

def filter_df(data):
    column_list = ['amount', 'category', 'date', 'name', 'transaction_id']
    filtered_df = data[column_list]
    print(filtered_df)
    return filtered_df