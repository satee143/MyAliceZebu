import datetime

import openpyxl
import pandas as pd

f_list = []
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + 'bn.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
df = df['LTP'].resample('30min', base=15).ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print((df))
if (float(df.iloc[[1]]['close']) < float(df.iloc[[1]]['open']) and
      float(df.iloc[[2]]['close']) < float(df.iloc[[2]]['open']) and
      float(df.iloc[[2]]['low']) < float(df.iloc[[1]]['low'])):
    print('Bank Nifty Future Sell Recommanded Price is  :', float(df.iloc[[2]]['low'] - 2))
    points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    print('Bank Nifty Future buy target is :', float(df.iloc[[2]]['low']) - points)
    print('Bank Nifty Future stoploss is :', float(df.iloc[[2]]['high']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('SELL')
    f_list.append(float(df.iloc[[2]]['low'] - 2))
    f_list.append(float(float(df.iloc[[2]]['low']) - points))
    f_list.append(float(df.iloc[[2]]['high']))

elif (float(df.iloc[[1]]['close']) > float(df.iloc[[1]]['open']) and
      float(df.iloc[[2]]['close']) > float(df.iloc[[2]]['open']) and
      float(df.iloc[[2]]['high']) > float(df.iloc[[1]]['high'])):
    print('Bank Nifty Future Buy Recommanded Price is  :', float(df.iloc[[2]]['high'] + 2))
    points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    print('Bank Nifty Future sell target is :', float(df.iloc[[2]]['low']) + points)
    print('bank Nifty Future stoploss is :', float(df.iloc[[2]]['low']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('BUY')
    f_list.append(float(df.iloc[[2]]['high'] + 2))
    f_list.append(float(float(df.iloc[[2]]['high']) + points))
    f_list.append(float(df.iloc[[2]]['low']))

book = openpyxl.load_workbook('bank_results.xlsx')
sheet = book.active

sheet.append(f_list)
book.save('bank_results.xlsx')
