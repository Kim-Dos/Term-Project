import telepot
import time
import sys
import traceback
from UpbitParsing import *
import Gmail

coins = UPBIT_INFO()
bot = telepot.Bot('6948127546:AAFJphioOXubkrqKy0SQ8ywhacXt3r08Xgk')

my_email = Gmail.Email()

def handle(msg):
    content_type, chat_type, userID = telepot.glance(msg)
    if content_type != 'text':
        Sending('텍스트로 줘라')
        return

    text = msg['text']
    args = text.split(' ')
    if text.startswith('코인동향') and len(args) > 1:
        CoinLog(userID, args[1], args[2])
    if text.startswith('추천매매'):
        SuggestCoin(userID, args[1])
    if text.startswith('메일전송'):
        SendMail(userID, args[1], args[2], args[3])

def CoinLog(userID, coinname, logcount):
    m_name = coins.change_market_name(coinname)
    logs = get_ohlcv(ticker=m_name, count=int(logcount))
    logs.drop('volume', axis=1, inplace=True)
    logs.index = logs.index.astype(str)
    logs.index = logs.index.str.replace("2024-","")
    logs.index = logs.index.str.replace("09:00:00","")



    Sending(userID, "time"+logs.to_string())

def SendMail(userID, coinname, logcount, email):
    m_name = coins.change_market_name(coinname)
    logs = get_ohlcv(ticker=m_name, count=int(logcount))
    logs.drop('volume', axis=1, inplace=True)
    logs.index = logs.index.astype(str)
    logs.index = logs.index.str.replace("2024-", "")
    logs.index = logs.index.str.replace("09:00:00", "")

    if my_email.sendMail("time"+logs.to_string(), email):
        bot.sendMessage(userID,"전송에 성공하였습니다")
    else:
        bot.sendMessage(userID, "전송에 실패하였습니다")
def SuggestCoin(userID, coinname):
    m_name = coins.change_market_name(coinname)
    pass

def Sending(userID, msg):
    try:
        bot.sendMessage(userID, msg)
    except:
        traceback.print_exc(file=sys.stdout)

bot.message_loop(handle)

while 1:
    time.sleep(10)



