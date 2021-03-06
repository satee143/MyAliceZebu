import datetime

import openpyxl
import pandas as pd

from zebu_api import ZebuAPI

zebu_api = ZebuAPI()
f_list = []
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + '.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
df = df['LTP'].resample('15min').ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print(df)
if (float(df.iloc[[2]]['high']) > float(df.iloc[[1]]['high']) and
        float(df.iloc[[2]]['low']) > float(df.iloc[[1]]['low'])):
    print('Nifty Future Sell Recommended Price is  :', float(df.iloc[[2]]['low']))
    points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    print('Nifty Future buy target is :', float(df.iloc[[2]]['low']) - points)
    print('Nifty Future stoploss is :', float(df.iloc[[2]]['high']))
    f_list.append(datetime.date.today())
    f_list.append('NIFTY')
    f_list.append('SELL')
    f_list.append(float(df.iloc[[2]]['low']))
    f_list.append(float(float(df.iloc[[2]]['low']) - points))
    f_list.append(float(df.iloc[[2]]['high']))
    # print(zebu_api.place_regular_order('NFO','NIFTY20AUGFUT','regular','SELL','DAY',float(df.iloc[[1]]['low']),'L',
    # '150'))
    # print(zebu_api.place_bracket_order('NFO',44330, 'NIFTY20AUGFUT', 'bo', 'SELL', 'DAY', float(df.iloc[[
    # 1]]['low']), 'L', '75', float(float(df.iloc[[1]]['low']) - points), float(df.iloc[[1]]['high']), 5))

elif (float(df.iloc[[2]]['low']) < float(df.iloc[[1]]['low']) and
      float(df.iloc[[2]]['high']) < float(df.iloc[[1]]['high'])):
    print('Nifty Future Buy Recommanded Price is  :', float(df.iloc[[2]]['high']))
    points = float(df.iloc[[2]]['high'] - float(df.iloc[[2]]['low']))
    print(points)
    print('Nifty Future sell target is :', float(df.iloc[[2]]['high']) + points)
    print('Nifty Future stoploss is :', float(df.iloc[[2]]['low']))
    f_list.append(str(datetime.date.today()))
    f_list.append('NIFTY')
    f_list.append('BUY')
    f_list.append(float(df.iloc[[2]]['high']))
    f_list.append(float(float(df.iloc[[2]]['high']) + points))
    f_list.append(float(df.iloc[[2]]['low']))
    # #print(zebu_api.place_bracket_order('NFO',44330, 'NIFTY20AUGFUT', 'bo', 'SELL', 'DAY', float(df.iloc[[1]][
    # 'high']), 'L', '75', float(float(df.iloc[[1]]['high']) + points), float(df.iloc[[1]]['low']), 5))

book = openpyxl.load_workbook('results.xlsx')
sheet = book.active

sheet.append(f_list)
book.save('results.xlsx')
