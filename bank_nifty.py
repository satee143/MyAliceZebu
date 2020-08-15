import datetime

import openpyxl
import pandas as pd

## Creating list to add excel
f_list = []

# Converting the ticks into candlesticks
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + 'bn.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
df = df['LTP'].resample('30min', base=15).ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print((df))

## Checking the condition  first candle low  lessthan the first candle open
## second candle low lessthan second candle open
## second candle low lessthan first candle low
## first candle close lessthan first candle open
## second candle close lessthan second candle open
if (float(df.iloc[[2]]['low']) < float(df.iloc[[2]]['open']) and
        float(df.iloc[[3]]['low']) < float(df.iloc[[3]]['open']) and float(df.iloc[[3]]['low']) < float(
            df.iloc[[2]]['low']) and float(df.iloc[[2]]['close']) < float(df.iloc[[2]]['open']) and float(
            df.iloc[[3]]['close']) < float(df.iloc[[3]]['open'])):
    print('Bank Nifty Future Sell Recommanded Price is  :', float(df.iloc[[3]]['low'] - 5))
    points = float(df.iloc[[3]]['high'] - df.iloc[[3]]['low'])
    print('Bank Nifty Future buy target is :', float(df.iloc[[3]]['low']) - points)
    print('Bank Nifty Future stoploss is :', float(df.iloc[[3]]['high']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('SELL')
    f_list.append(float(df.iloc[[3]]['low'] - 5))
    f_list.append(float(float(df.iloc[[3]]['low']) - points))
    f_list.append(float(df.iloc[[3]]['high'] + 5))



## Checking the condition  first candle high  greaterthan the first candle open
## second candle high greaterthan second candle open
## second candle high greaterthan first candle high
## first candle close greaterthan first candle open
## second candle close greaterthan second candle open
elif (float(df.iloc[[2]]['high']) > float(df.iloc[[2]]['open']) and
      float(df.iloc[[3]]['high']) > float(df.iloc[[3]]['open']) and float(df.iloc[[3]]['high']) > float(
            df.iloc[[2]]['high']) and float(df.iloc[[2]]['close']) > float(df.iloc[[2]]['open']) and float(
            df.iloc[[3]]['close']) > float(df.iloc[[3]]['open'])):
    print('Bank Nifty Future Buy Recommanded Price is  :', float(df.iloc[[3]]['high'] + 5))
    points = float(df.iloc[[3]]['high'] - df.iloc[[3]]['low'])
    print('Bank Nifty Future sell target is :', float(df.iloc[[3]]['low']) + points)
    print('bank Nifty Future stoploss is :', float(df.iloc[[3]]['low']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('BUY')
    f_list.append(float(df.iloc[[3]]['high'] + 5))
    f_list.append(float(float(df.iloc[[3]]['high']) + points))
    f_list.append(float(df.iloc[[3]]['low'] + 5))

book = openpyxl.Workbook()
sheet = book.active
sheet.append(f_list)
book.save('bank_results.xlsx')
