from pyupbit import *
import requests

url = "https://api.upbit.com/v1/market/all"

# 업비트에서 코인과 관련된 값들과 정보를 가져오는 클래스
# 업비트에서 가져올만한 것들 - 코인의 이름, 마켓이름, 2 현재가, 전일대비 금액, 거래대금
# 업비트 url과 연동하여 정보들을 return
class UPBIT_INFO:
    TickerUrl= "https://api.upbit.com/v1/ticker?markets="

    def __init__(self):
        # 코인 이름들을 저장
        self.KRW_tickers = get_tickers(fiat='KRW')
        self.KRW_List = []
        # 모든 원화 코인들 저장
        self.response = requests.get(url)

        for c in self.response.json():
            if c['market'][0] == 'K':
                self.KRW_List.append(c)

    def GetKRWTickers(self,i):
        return self.KRW_tickers[i]
    def GetKRWList(self,i):
        return self.KRW_List[i]
    def GetCoinInfo(self, name):
        self.response = requests.get(self.TickerUrl+name)
        return self.response.json()
    def TotalNumberofCoins(self):
        return len(self.KRW_List)

    def find_coin(self, name):
        for c in self.KRW_List:
            if c['korean_name'] == name or c['english_name'] == name or c['market'] == name:
                return True
        return False
    def get_coin(self, name):
        for c in self.KRW_List:
            if c['korean_name'] == name or c['english_name'] == name or c['market'] == name:
                return c
    def change_market_name(self, name):
        for c in self.KRW_List:
            if c['korean_name'] == name or c['english_name'] == name or c['market'] == name:
                return c['market']
    def change_korean_name(self, name):
        for c in self.KRW_List:
            if c['korean_name'] == name or c['english_name'] == name or c['market'] == name:
                return c['korean_name']
#  실제로 유저의 요청을 받는 클래스
#  현재 들고있는 코인 및 원화, 매수, 매도 및 return된 정보를 받아서 또 return
class USER_INFO:
    Coin_info = UPBIT_INFO()
    Star_List = []
    def __init__(self):
        # API KEY를 통한 자신의 계정 진입
        with open("key.txt") as f:
            access_key, secret_key = [line.strip() for line in f.readlines()]
        with open('StartList.txt') as l:
            [self.Star_List.append(line.strip()) for line in l.readlines()]

        # 업비트로 연동
        self.user = Upbit(access_key, secret_key)

    def limit_buy(self, name, price, volume):
        temp = self.Coin_info.get_coin(name)
        try:
            res = self.user.buy_limit_order(temp['market'], price, volume)
            if 'error' in res:
                return -1
        except Exception as e:
            return -1
        return 0

    def limit_sell(self, name, price, volume):
        if(self.Coin_info.find_coin(name) == False):
            return - 2
        temp = self.Coin_info.get_coin(name)
        try:
            res = self.user.sell_limit_order(temp['market'], price, volume)
            if 'error' in res:
                return -1
        except Exception as e:
            return -1
        return 0

    def market_buy(self, name, price):
        if int(price) < 5000:
            return -1
        if self.Coin_info.find_coin(name) == False:
            return -4
        temp = self.Coin_info.get_coin(name)
        try:
            print(temp['market'])
            res = self.user.buy_market_order(temp['market'], price)
            if 'error' in res:
                return -2
        except Exception as e:
            return -3
        return 0
    def market_sell(self, name, price):
        temp = self.Coin_info.get_coin(name)
        try:
            res = self.user.sell_market_order(temp['market'], price)
            if 'error' in res:
                return -1
        except Exception as e:
            return -1
        return 0

    def currentAccount(self):
        account = self.user.get_balances()
        return account

    def addStarList(self, name):
        m_name = self.Coin_info.change_market_name(name)
        if self.Star_List.count(m_name) == 0 and len(self.Star_List) < 10:
            self.Star_List.append(m_name)
            with open('StartList.txt', 'w') as f:
                for c in self.Star_List:
                    f.write(c+'\n')
            self.Star_List.clear()
            with open('StartList.txt') as l:
                [self.Star_List.append(line.strip()) for line in l.readlines()]
            return True
        else:
            return False

    def removeStarList(self, name):
        m_name = self.Coin_info.change_market_name(name)
        if self.Star_List.count(m_name) > 0:
            self.Star_List.remove(m_name)
            with open('StartList.txt', 'w') as f:
                for c in self.Star_List:
                    f.write(c+'\n')
            self.Star_List.clear()
            with open('StartList.txt') as l:
                [self.Star_List.append(line.strip()) for line in l.readlines()]
            print(self.Star_List)

            return True
        else:
            return False


# d = UPBIT_INFO()
# d.TickerUrl("KRW_BTC")