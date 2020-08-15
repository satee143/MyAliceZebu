import hashlib
import json

import jsonpath
import requests


class ZebuAPI:
    ''' Zebu api for python'''

    def __init__(self):
        self.baseurl = 'https://www.zebull.in/rest/MobullService/v1/'
        self.headers = {'Content-Type': 'application/json'}

        self._encryption_key = "customer/getAPIEncpkey"
        self._session_id = "customer/getUserSID"
        self._limits = "limits/getRmsLimits"
        self._search_symbol = "https://www.zebull.in/rest/MobullService/exchange/getScripForSearch"
        self._regular_order = "placeOrder/executePlaceOrder"
        self._bracket_order = "placeOrder/executePlaceOrder"
        self._order_book = "placeOrder/fetchOrderBook"
        self._trade_book = "placeOrder/fetchTradeBook"
        self._modify_order = "placeOrder/modifyOrder"
        self._cancel_order = "placeOrder/cancelOrder"
        self._order_history = "placeOrder/orderHistory"
        self._get_holdings = "positionAndHoldings/holdings"
        self._get_positions = "positionAndHoldings/positionBook"
        self._conversion_position = "positionAndHoldings/positionConvertion"
        self._square_off_position = "positionAndHoldings/sqrOofPosition"
        # 'profile': '/api/v2/profile',
        # 'master_contract': '/api/v2/contracts.json?exchanges={exchange}',
        # 'place_amo': '/api/v2/amo',
        # 'place_basket_order': '/api/v2/basketorder',
        # 'get_orders': '/api/v2/order'
        # 'get_order_info': '/api/v2/order/{order_id}',

    def get_encryption_key(self):
        url = self.baseurl + self._encryption_key
        payload = '{"userId": "DEL16035"}'
        # headers = {'Content-Type': 'application/json'}
        response = requests.post(url, payload, headers=self.headers)
        enc_key = jsonpath.jsonpath(json.loads(response.text), 'encKey')
        return enc_key[0]

    def api_to_hash(self):
        uid = 'DEL16035'
        api = 'bRY11QinkR8B5lfvW2eUR5B6UWBgCSMAczzQa2rtYuC5fuZHPyDRh5Ur09fRokOdu5TLQu9iBlZ9LrHR2SrLWXI4yPs5acd6hsUfjQFmTSpqcF2pvTuzSTjZEffVPCxz'
        str = uid + api + self.get_encryption_key()
        result = hashlib.sha256(str.encode())
        value = result.hexdigest()
        return value

    def get_session_id(self):
        ''' Get the Session id '''
        url = self.baseurl + self._session_id
        userdata = {'userId': 'DEL16035', 'userData': self.api_to_hash()}
        json_object = json.dumps(userdata)
        response = requests.post(url, json_object, headers=self.headers)
        session_id = jsonpath.jsonpath(json.loads(response.text), 'sessionID')
        return session_id[0]

    def auther_key(self):
        static_text = 'Bearer'
        user_id = 'DEL16035'
        auth_key = static_text + " " + user_id + " " + self.get_session_id()
        return auth_key

    def get_limits(self):
        url = self.baseurl + self._limits
        payload = {}
        headers = {'Authorization': self.auther_key()}
        response = requests.get(url, payload, headers=headers)
        credits = jsonpath.jsonpath(response.json()[0], 'credits')
        return credits

    def search_symbol(self, exchange, symbol):
        url = "https://www.zebull.in/rest/MobullService/exchange/getScripForSearch"
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        exchange = [exchange]
        payload = {'symbol': symbol, 'exchange': exchange}
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        token = response.json()
        # token = jsonpath.jsonpath(json.loads(response.text), 'token')
        # return int(token[0]['token'])
        return response.text

    def place_regular_order(self, exchange, symbol, complexty, order_type, validity, price, price_type, quantity,
                            discqty=0,
                            trigger_price=0,
                            product_code='mis'):
        """ placing an order, many fields are optional and are not required
                    for all order types
                """
        url = self.baseurl + self._regular_order
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}

        payload = {'complexty': complexty, 'trading_symbol': symbol, 'discqty': discqty, 'exch': exchange,
                   'transtype': order_type.upper(), 'ret': validity.upper(), 'prctyp': price_type, 'qty': quantity,
                   'symbol_id': '',
                   'price': price, 'trigPrice': trigger_price, 'pCode': product_code}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        response_status = json.loads(response.text)
        return response_status[0]['nestOrderNumber']

    def place_bracket_order(self, exchange, symbol_id, symbol, complexty, order_type, validity, price, price_type,
                            quantity, target,
                            stoploss, t_stoploss, discqty='0', trigger_price='0',
                            product_code='mis'):
        url = self.baseurl + self._bracket_order
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'complexty': complexty, 'trading_symbol': symbol, 'discqty': discqty, 'exch': exchange,
                   'transtype': order_type.upper(), 'ret': validity.upper(), 'prctyp': price_type, 'qty': quantity,
                   'symbol_id': symbol_id,
                   'price': price, 'trigPrice': trigger_price, 'pCode': product_code,
                   'target': target, 'stopLoss': stoploss, 'trailing_stop_loss': t_stoploss}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        response_status = json.loads(response.text)
        return response_status[0]['nestOrderNumber']

    def get_order_book(self):
        url = self.baseurl + self._order_book
        payload = {}
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        response = requests.get(url, payload, headers=headers)
        return response.text

    def get_trade_book(self):
        url = self.baseurl + self._trade_book
        payload = {}
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        response = requests.get(url, payload, headers=headers)
        return response.text

    def modify_order(self, exchange, nest_ref, symbol, price, price_type, quantity, discqty='0', trigger_price='0'):
        url = self.baseurl + self._modify_order
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'discqty': discqty, 'exch': exchange, 'filledQuantity': '0',
                   'nestOrderNumber': nest_ref, 'trading_symbol': symbol,
                   'prctyp': price_type, 'qty': quantity,
                   'price': price, 'trigPrice': trigger_price, }
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def cancel_order(self, exchange, symbol, nest_ref):
        url = self.baseurl + self._cancel_order
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'exch': exchange,
                   'nestOrderNumber': nest_ref, 'trading_symbol': symbol}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def nse_order_history(self, nest_ref):
        url = self.baseurl + self._order_history
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'nestOrderNumber': nest_ref}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def get_holdings(self):
        url = self.baseurl + self._get_holdings
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def get_positions(self, retention):
        url = self.baseurl + self._get_positions
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'ret': retention}
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def conversion_position(self, exchange, quantity, symbol):
        url = self.baseurl + self._conversion_position
        headers = {'Authorization': self.auther_key(), 'Content-Type': 'application/json'}
        payload = {'exch': exchange, 'productTocode': 'NRML', 'tsym': '',
                   'qty': quantity, 'transtype': 'B', 'tokenNO': '', 'type': 'DAY',
                   'pCode': 'MIS'
                   }
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)

    def square_off_position(self, exchange, symbol, quantity, token):
        url = self.baseurl + self._square_off_position
        payload = {'exchSeg': exchange, 'pCode': 'MIS', 'netQty': quantity, 'tokenNO': '', 'symbol': symbol}
        payload = [payload]
        payload = json.dumps(payload)
        response = requests.post(url, headers=self.headers, data=payload)
        print(response.text)


a = ZebuAPI()
# print(a.place_bracket_order('NFO', 44330, 'NIFTY20AUGFUT', 'bo', 'SELL', 'DAY', 11230, 'L', '75', 11400, 11005, 5))

# print(place_regular_order('NSE','ASHOKLEY-EQ','regular','BUY','DAY','100','L','1'))
# print(place_regular_order('NFO', 'NIFTY20AUGFUT', 'regular', 'BUY', 'DAY', '100', 'L','75'))
# print(place_bracket_order('NSE', 'dsfds-EQ', 'bo', 'BUY', 'DAY', 101, 'L', '1', 3, 4, 5))
# print(search_symbol('nse', 'ASHOKLEY'))
print(a.__dict__)
print(int(float(a.get_limits()[0])))
print(a.__dict__)
