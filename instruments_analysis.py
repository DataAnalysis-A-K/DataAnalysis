import pandas as pd

data = pd.read_csv('data/new_instruments_data.csv')

df = pd.read_csv('data/instruments_data.csv')

top_etfs = ["SPY", "QQQ", "DIA", "IWM", "VOO", "VTI", "EEM", "GLD"]

df.info()
print()

df = df[df['assetType'] == 'ETF']
df = df[df['symbol'].isin(top_etfs)]

print(df.to_string() + "\n")


labels = ['symbol', 'name', 'exchange', 'asset_type', 'ipo_date', 'delisting_date', 'status']

df.columns = labels

df.to_csv('data/new_instruments_data.csv', index=False, header=False)