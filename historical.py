import os
from datetime import date

from nsepy import get_history

data = get_history(symbol='SBIN', start=date(2020, 1, 1), end=date(2020, 4, 17))
os.chdir('/storage/emulated/0/bluetooth')
print(type(data))
data.to_excel('a.xlsx')
