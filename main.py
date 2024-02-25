import requests
import pandas as pd
import time


def message(bot_mesaj):
    bot_token = "***********"

    id_list = ["*****","*******"]

    for i in id_list:
        url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + i + "&parse_mode=Markdown&text=" + bot_mesaj
        response = requests.get(url)
        time.sleep(1)

def indexFinder(lst,elm):
    for i in range(len(lst)):
        if lst[i] == elm:
            return i
    else:
        return -1

def get_binance_data(symbol, interval, limit):
    base_url = 'https://api.binance.com/api/v1/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

message("Restarted")


keys = ["ONEUSDT","VIBBUSD","JSTUSDT","OMUSDT","POLYXUSDT","KMDUSDT","ONTUSDT",
        "RADUSDT","JOEUSDT","KEYUSDT","TKOUSDT","DOGEUSDT","LUNCUSDT","CVPUSDT",
        "WINGUSDT","ATMUSDT","BARUSDT","ALPINEUSDT","LAZIOUSDT","CITYUSDT","OMUSDT",
        "TROYUSDT","TFUELUSDT","UMAUSDT","FITBUSD","SRMBUSD","JSTUSDT","TVKUSDT",
        "ONGUSDT","ONTUSDT","CFXUSDT","WRXUSDT","POLYXUSDT","XRPUSDT","KEYUSDT",
        "AGIXUSDT","PERLUSDT","FIDAUSDT","LOKAUSDT","VIBUSDT","PEPEUSDT","DENTUSDT"]


value = ["CELRUSDT","PROSBUSD","SUNUSDT","FIOUSDT","POWRUSDT","WTCUSDT","NEOUSDT",
         "UMAUSDT","QIUSDT","DREPUSDT","WRXUSDT","SHIBUSDT","USTCBUSD","DFUSDT",
         "BONDUSDT","ACMUSDT","JUVUSDT","SANTOSUSDT","PORTOUSDT","PSGUSDT","FIOUSDT",
         "OOKIUSDT","THETAUSDT","RADUSDT","SRMBUSD","SNMBUSD","SUNUSDT","TLMUSDT",
         "OASBUSD","NEOUSDT","ACHUSDT","TKOUSDT","POWRUSDT","XLMUSDT","LINCAUSDT","FETUSDT",
         "PNTUSDT","RAYUSDT","VOXELUSDT","PROSUSDT","FLOKIUSDT","HOTUSDT"]



def go():

    for i in keys:
        try:
            #symbol = "ETHUSDT"  # Replace with the desired symbol (e.g., "ETHUSDT" for Ethereum)
            symbol = i
            interval = "1m"     # Data interval (e.g., "1h" for 1-hour data, "1d" for 1-day data)
            limit = 6        # Number of data points to fetch (max is 1000)
            coin = get_binance_data(symbol, interval, limit)


            if ((float(coin["close"][4])-float(coin["close"][0]))/float(coin["close"][0]) > 0.02):
                message(symbol, " 5 dakika içinde yüzde", str(float(coin["close"][4])-float(coin["close"][0])/float(coin["close"][0])) ," arttı , korele coin : ", value[indexFinder(keys,symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0]) < -0.02):
                message(symbol, " 5 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0])), " düştü , korele coin : ",
                      value[indexFinder(keys, symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3]) > 0.02):
                message(symbol, " 1 dakika içinde yüzde",
                      str(float(coin["close"][4]) - float(coin["close"][3]) / float(coin["close"][3])),
                      " arttı , korele coin : ", value[indexFinder(keys, symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3]) < -0.02):
                message(symbol, " 1 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3])),
                      " düştü , korele coin : ",
                      value[indexFinder(keys, symbol)])

        except:
            pass


    for i in value:
        try:
            # symbol = "ETHUSDT"  # Replace with the desired symbol (e.g., "ETHUSDT" for Ethereum)
            symbol = i
            interval = "1m"  # Data interval (e.g., "1h" for 1-hour data, "1d" for 1-day data)
            limit = 6  # Number of data points to fetch (max is 1000)
            coin = get_binance_data(symbol, interval, limit)

            if ((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0]) > 0.02):
                message(symbol, " 5 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0])),
                      " arttı , korele coin : ", keys[indexFinder(value, symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0]) < -0.02):
                message(symbol, " 5 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][0])) / float(coin["close"][0])),
                      " düştü , korele coin : ",
                      keys[indexFinder(value, symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3]) > 0.02):
                message(symbol, " 1 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3])),
                      " arttı , korele coin : ", keys[indexFinder(value, symbol)])

            elif ((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3]) < -0.02):
                message(symbol, " 1 dakika içinde yüzde",
                      str((float(coin["close"][4]) - float(coin["close"][3])) / float(coin["close"][3])),
                      " düştü , korele coin : ",
                      keys[indexFinder(value, symbol)])

        except:
            pass



while True:

    try:
        if  time.localtime().tm_sec >= 58:
            go()
    except:
        pass
