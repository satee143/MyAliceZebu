import csv
import datetime
from time import sleep
import logging
logging.basicConfig(level=logging.DEBUG)
from alice_blue import *

access_token = AliceBlue.login_and_get_access_token(username='AB102865', password='sampath@1', twoFA='a',
                                                    api_secret='CW7LT01PAQRAVVUFQ0VH0PGXV1VJUG10RGWK3IAMIJGHJ1KCXYU1QBZWQJZ1FR53')
alice = AliceBlue(username='AB102865', password='sampath@1', access_token=access_token,
                  master_contracts_to_download=['NFO'])
socket_opened = True


def event_handler_quote_update(message):
    f = csv.writer(open(str(datetime.date.today()) + '.csv', 'a', newline=''))
    print(message['ltp'], message['exchange_time_stamp'])
    f.writerow([message['ltp'], message['exchange_time_stamp']])


def open_callback():
    global socket_opened
    socket_opened = True


alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)
while (socket_opened == False):
    pass
alice.subscribe(alice.get_instrument_for_fno(symbol='NIFTY', expiry_date=datetime.date(2020, 9,24), is_fut=True,
                                             strike=None, is_CE=False), LiveFeedType.MARKET_DATA)
sleep(99999)
