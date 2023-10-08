import pandas as pd
from datetime import datetime

file_path = 'output_Kp_normalized.dat'
data = pd.read_csv(file_path, sep=' ', header=None)

def parse_date(row):
    return datetime(year=int(row[0]), month=int(row[1]), day=int(row[2]), hour=int(row[3]), minute=int(row[4]))

data['Date'] = data.apply(lambda row: parse_date(row), axis=1)

new_data = data.iloc[:, [6, 5]]

new_data.columns = [0, 1]

new_data.columns = ['Date', 'Kp']

print(new_data.head())

new_data.to_csv('output_Kp.csv', index=False)
