import datetime

import pandas as pd
from nsepy import get_history


class MYCUSTOMUTILS():

    def excel_to_csv(self, file_path, index_name, save_loc):
        df = pd.read_excel(file_path)
        df.reset_index()
        df.set_index(index_name, inplace=True)
        df.to_csv(save_loc)
        return "Sucessfully completed"

    def resample_csv_to_dataframe(self, file_path, resample, base=0, df_cols=['LTP', 'Times']):
        df = pd.read_csv(file_path, names=df_cols, index_col=1, parse_dates=True)
        df.reset_index(inplace=True)
        df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
        df.set_index('Times', inplace=True)
        df = df['LTP'].resample(resample, base).ohlc().dropna()
        return df

    def get_history_of_stock(self, symbol, start_date='01-01-2020', end_date='01-08-2020'):
        start_date=datetime.datetime.strptime(start_date, '%d-%m-%Y')
        start=datetime.datetime.strftime(start_date,'%Y-%m-%d')
        print(type(start))
        # end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
        # end = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        data = get_history(symbol=symbol,start='2020-01-01',end='2020-01-01')
        return data

print(datetime.date(2020, 4, 1))
a = MYCUSTOMUTILS()
print(a.get_history_of_stock('CIPLA'))

