import datetime
import os
from datetime import timedelta

import nsepy
import plotly.graph_objects as go

global df, buy_list
global updates
buy_list = []
updates = []

data = 'INFY'
buy = []
date_y = datetime.date.today() - timedelta(days=60)
df = nsepy.get_history(symbol='ONGC', start=date_y, end=datetime.date.today())
df.reset_index('Date', inplace=True)
df['Date'] = df['Date'].astype(str)
df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
df.set_index('Date', inplace=True)
ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}

df = df.resample('M', how=ohlc_dict).dropna(how='any')
cols = ['Open', 'High', 'Low', 'Close']
df = df[cols]

# df = df['Close'].resample('1M').ohlc()
df.reset_index('Date', inplace=True)
print(df)

df['HA_Close'] = ((df['Open'] + df['High'] + df['Low'] + df['Close']) / 4)

df['HA_Open'] = (df['Open'].shift(1) + df['Open'].shift(1)) / 2
df.iloc[0, df.columns.get_loc("HA_Open")] = (df.iloc[0]['Open'] + df.iloc[0]['Close']) / 2
df['HA_High'] = df[['High', 'Low', 'HA_Open', 'HA_Close']].max(axis=1)
df['HA_Low'] = ((df[['High', 'Low', 'HA_Open', 'HA_Close']].min(axis=1)))

print(df[['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']])
# df.reset_index('Date', inplace=True)
# fig = go.Figure(data=[go.Ohlc(x=df['Date'], Open=df['Open'],High=df['High'], Low=df['Low'], Close=df['Close'])])

fig = go.Figure(
    data=[go.Candlestick(x=df['Date'], open=df['HA_Open'], high=df['HA_High'], low=df['HA_Low'], close=df['HA_Close'])])

if (float(df.iloc[[-1]]['HA_High']) <= float(df.iloc[[-1]]['HA_Open'])):
    if (float(df.iloc[[-1]]['HA_Low']) <= float(df.iloc[[-1]]['HA_Close'])):
        print('Sell Recommanded Price for ' + data + ' :', round(float(df.iloc[[-1]]['HA_Low']) * 98 / 100, 2))
elif (float(df.iloc[[-1]]['HA_Low']) >= float(df.iloc[[-1]]['HA_Open'])):
    if ((float(df.iloc[[-1]]['HA_High']) >= float(df.iloc[[-1]]['HA_Close']))):
        buy.append(data)
        buy.append(round(float(df.iloc[[-1]]['HA_High']) * 102 / 100, 2))
        print('Buy Recommanded Price for ' + data + ':', round(float(df.iloc[[-1]]['HA_High']) * 102 / 100, 2))
    os.chdir('/storage/emulated/0/recom')
    df[['Date', 'HA_Open', 'HA_High', 'HA_Low', 'HA_Close']].to_excel(data + '.xlsx')
    df.to_excel('ab.xlsx')
    fig.write_html(data + '.html')
