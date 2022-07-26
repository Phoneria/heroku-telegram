import pandas as pd
from datetime import datetime as dt
import time
from binance import Client
import csv
from datetime import datetime, timedelta
import pandas_ta as ta
import requests


def message(bot_mesaj):
    id_list = ["1598072365", "1518181191"]
    # 1518181191 ataberk
    # 734839772 furkan
    for i in id_list:
        bot_token = "5424258200:AAGNGZlN5HevI2fnyQedvD7v8XPsFFSBBJA"
        url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + i + "&parse_mode=Markdown&text=" + bot_mesaj
        response = requests.get(url)



def tg_writer(coin_name):
    client = Client(None, None)

    def bring_data(symbol, periot, open, end):
        candles = client.get_historical_klines(symbol, periot, open, end)
        return candles

    def create_csv(symbol, candles):
        csv_file = open(symbol + "30MINTG.csv", "w", newline="")
        writer = csv.writer(csv_file)
        for candle in candles:
            writer.writerow(candle)

        csv_file.close()

    start_time = datetime.today() - timedelta(hours=50)
    finish_time = datetime.today() + timedelta(days=1)
    interval = Client.KLINE_INTERVAL_30MINUTE

    create_csv(coin_name, bring_data(coin_name, interval, str(start_time), str(finish_time)))
    
    


def candle_stick(coin_name):
    titles = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV",
              "ignore"]

    tg_writer(coin_name)

    df = pd.read_csv(coin_name + "30MINTG.csv", names=titles)

    open_level = df["Open"]
    close_level = df["Close"]
    high_level = df["High"]
    low_level = df["Low"]
    open_time = df["Open Time"]

    def calculate_time(number):
        return dt.fromtimestamp(open_time.iloc[number] / 1000)
    
    
    def pivot():
        High = 0
        Low = 10000
        Close = 0

        current_time = len(close_level) - 1


        if (calculate_time(current_time).hour == 3 and calculate_time(current_time).minute == 0):

            current_time -= 1
            for i in range(49):

                if high_level[current_time - i] > High:
                    High = high_level[current_time - i]
                if low_level[current_time - i] < Low:
                    Low = low_level[current_time - i]

                if i == 0:
                    Close = close_level[current_time - i]

            PP = (High + Low + Close) / 3
            R1 = 2 * PP - Low
            S1 = 2 * PP - High
            R2 = PP + (High - Low)
            S2 = PP - (High - Low)
            R3 = 2 * PP + (High - 2 * Low)
            S3 = 2 * PP - (2 * High - Low)
            R4 = 3 * PP + (High - 3 * Low)
            S4 = 3 * PP - (3 * High - Low)
            R5 = 4 * PP + (High - 4 * Low)
            S5 = 4 * PP - (4 * High - Low)

            pivot_list.clear()

            pivot_list.append(PP)
            pivot_list.append(R1)
            pivot_list.append(R2)
            pivot_list.append(R3)
            pivot_list.append(R4)
            pivot_list.append(R5)
            pivot_list.append(S1)
            pivot_list.append(S2)
            pivot_list.append(S3)
            pivot_list.append(S4)
            pivot_list.append(S5)

        return pivot_list

    def rsi_indicator():
        rsi = ta.rsi(close=close_level, length=14)

        if rsi.iloc[len(close_level) - 1] > 70:
            message("\nOVERBOUGHT!!!\nCURRENT RSI VALUE : "+ str(rsi.iloc[len(close_level) - 1])+"\n" +
             str( calculate_time(len(close_level) - 1)))

        if rsi.iloc[len(close_level) - 1] < 30:
             message("\nOVERSOLD!!!\nCURRENT RSI VALUE : "+str( rsi.iloc[len(close_level) - 1])+"\n" +str (calculate_time(len(close_level) - 1)))



    max_level = 0
    min_level = 1000000000
    
    
    for i in range(5, len(close_level)):
        rsi_indicator()
        pivot()
        
         if len(pivot_list > 2):

            if close_level[i-1] < pivot_list[0] and close_level[i] > pivot_list[0]:
                message("PIVOT ÇİZGİSİNİ YUKARI KIRDI")
            if close_level[i-1] < pivot_list[1] and close_level[i] > pivot_list[1]:
                message("R1 ÇİZGİSİNİ NOKTASINI YUKARI KIRDI")
            if close_level[i-1] < pivot_list[2] and close_level[i] > pivot_list[2]:
                message("R2 ÇİZGİSİNİ NOKTASINI YUKARI KIRDI")
            if close_level[i-1] < pivot_list[3] and close_level[i] > pivot_list[3]:
                message("R3 ÇİZGİSİNİ NOKTASINI YUKARI KIRDI")
            if close_level[i-1] < pivot_list[4] and close_level[i] > pivot_list[4]:
                message("R4 ÇİZGİSİNİ NOKTASINI YUKARI KIRDI")
            if close_level[i-1] < pivot_list[5] and close_level[i] > pivot_list[5]:
                message("R5 ÇİZGİSİNİ NOKTASINI YUKARI KIRDI")

            if close_level[i-1] > pivot_list[0] and close_level[i] < pivot_list[0]:
                message("PIVOT ÇİZGİSİNİ AŞAĞI KIRDI")
            if close_level[i - 1] > pivot_list[6] and close_level[i] < pivot_list[6]:
                message("S1 ÇİZGİSİNİ AŞAĞI KIRDI")
            if close_level[i - 1] > pivot_list[7] and close_level[i] < pivot_list[7]:
                message("S2 ÇİZGİSİNİ AŞAĞI KIRDI")
            if close_level[i - 1] > pivot_list[8] and close_level[i] < pivot_list[8]:
                message("S3 ÇİZGİSİNİ AŞAĞI KIRDI")
            if close_level[i - 1] > pivot_list[9] and close_level[i] < pivot_list[9]:
                message("S4 ÇİZGİSİNİ AŞAĞI KIRDI")
            if close_level[i - 1] > pivot_list[10] and close_level[i] < pivot_list[10]:
                message("S5 ÇİZGİSİNİ AŞAĞI KIRDI")

        
        
        
        
        if calculate_time(i).hour == time.localtime().tm_hour and calculate_time(i).day == datetime.today().day:
            if max_level < high_level[i]:
                max_level = high_level[i]
                message(
                    coin_name + "\nSON 100 MUMUN EN YÜKSEK SEVİYESİ : "+str(max_level) + " \nZAMAN :  " + str(
                        calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))
                
                message(str(max_level))

            if min_level > low_level[i]:
                min_level = low_level[i]
                message(
                    coin_name + "\nSON 100 MUMUN EN DÜŞÜK SEVİYESİ : "+str(min_level) + " \nZAMAN :  " + str(
                        calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))
               
                

            # ENGULF CANDLE
            if (open_level[i] > close_level[i]) and (close_level[i - 1] > open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])):
                message(
                    coin_name + "\nSHORT ENGULF MUMU" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if (open_level[i] < close_level[i]) and (close_level[i - 1] < open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])):
                message(coin_name + "\nLONG ENGULF MUMU" + "\nZAMAN : " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # GREEN CANDLE WITHOUT BOT SHADOW
            if low_level[i] == open_level[i]:
                message(coin_name + "\nALT İĞNESİZ YEŞİL MUM " + " \nZAMAN :  " + str(
                    calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # RED CANDLE WITHOUT TOP SHADOW
            if high_level[i] == open_level[i]:
                message(
                    coin_name + "\nÜST İĞNESİZ KIRMIZI MUM" + " \nZAMAN :  " + str(
                        calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            # EVENING STAR
            if (close_level[i] < open_level[i]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i] - low_level[i]) < 0.3) and (
                    close_level[i - 2] > open_level[i - 2]) and (
                    abs(close_level[i - 2] - open_level[i - 2]) > abs(close_level[i] - (open_level[i]))) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i - 1] - low_level[i - 1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i] - low_level[i]) > 0.3) and (
                    abs(close_level[i - 2] - open_level[i - 2]) / (high_level[i - 2] - low_level[i - 2]) > 0.3):
                message(coin_name + "\nGECE YILDIZI" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # MORNING STAR

            if (close_level[i] > open_level[i]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])) and (
                    close_level[i - 2] < open_level[i - 2]) and (
                    abs(close_level[i - 2] - open_level[i - 2]) < abs(close_level[i] - (open_level[i]))) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i - 1] - low_level[i - 1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i] - low_level[i]) > 0.3) and (
                    abs(close_level[i - 2] - open_level[i - 2]) / (high_level[i - 2] - low_level[i - 2]) > 0.3):
                message(coin_name + "\nSABAH YILDIZI" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 1] > open_level[i - 1]) \
                    and (close_level[i - 2] > open_level[i - 2]) and (close_level[i - 3] < open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] > open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]):
                message(
                    coin_name + "\nİKİLİ ENGULF SHORT" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 1] < open_level[i - 1]) \
                    and (close_level[i - 2] < open_level[i - 2]) and (close_level[i - 3] > open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] < open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] < close_level[i - 1] - open_level[i - 1]):
                message(
                    coin_name + "\nİKİLİ ENGULF LONG" + "\nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 1] < open_level[i - 1]) and (
                    close_level[i] - open_level[i] > open_level[i - 1] - close_level[i - 1]) and (
                    close_level[i - 2] - open_level[i - 2] > open_level[i - 1] - close_level[i - 1]):
                message(coin_name + "\nSANDVİÇ LONG" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 1] > open_level[i - 1]) and (
                    open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]) and (
                    open_level[i - 2] - close_level[i - 2] > close_level[i - 1] - open_level[i - 1]):
                message(coin_name + "\nSANDVİÇ SHORT" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 4] > open_level[i - 4]) and (
                    close_level[i - 1] < open_level[i - 1]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 3] < open_level[i - 3]) \
                    and (open_level[i - 4] < open_level[i]):
                message(
                    coin_name + "\nÜÇLÜ ENGULF LONG " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 4] < open_level[i - 4]) and (
                    close_level[i - 1] > open_level[i - 1]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 3] > open_level[i - 3]) \
                    and (open_level[i - 4] > open_level[i]):
                message(
                    coin_name + "\nÜÇLÜ ENGULF SHORT " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 1] < open_level[i - 1]) and (
                    close_level[i - 2] < open_level[i - 2]) and \
                    close_level[i] < low_level[i - 1] and close_level[i - 1] < low_level[i - 2]:
                message(coin_name + "\nÜÇ KARA KARGA" + "\nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if close_level[i] > open_level[i] and close_level[i - 1] > open_level[i - 1] and close_level[i - 2] > \
                    open_level[i - 2] and \
                    close_level[i] > high_level[i - 1] and close_level[i - 1] > high_level[i - 2]:
                message(
                    coin_name + "\nÜÇ BEYAZ ASKER " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if close_level[i] < open_level[i] and \
                    close_level[i - 1] < open_level[i - 1] and \
                    close_level[i - 2] < open_level[i - 2] and \
                    close_level[i - 3] < open_level[i - 3] and \
                    close_level[i - 4] < open_level[i - 4]:
                message(coin_name + "\nBEŞ MUM SHORT " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if close_level[i] > open_level[i] and \
                    close_level[i - 1] > open_level[i - 1] and \
                    close_level[i - 2] > open_level[i - 2] and \
                    close_level[i - 3] > open_level[i - 3] and \
                    close_level[i - 4] > open_level[i - 4]:
                message(coin_name + "\nBEŞ MUM LONG " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))



        else:
            if high_level[i] >= max_level:
                max_level = high_level[i]
            if low_level[i] <= min_level:
                min_level = low_level[i]



def tg_writer_scalp(coin_name):
    client = Client(None, None)

    def bring_data(symbol, periot, open, end):
        candles = client.get_historical_klines(symbol, periot, open, end)
        return candles

    def create_csv(symbol, candles):
        csv_file = open(symbol + "1MINTG.csv", "w", newline="")
        writer = csv.writer(csv_file)
        for candle in candles:
            writer.writerow(candle)

        csv_file.close()

    start_time = datetime.today() - timedelta(days=1)
    finish_time = datetime.today() + timedelta(days=1)
    interval = Client.KLINE_INTERVAL_1MINUTE

    create_csv(coin_name, bring_data(coin_name, interval, str(start_time), str(finish_time)))


def candle_stick_scalp(coin_name):
    titles = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV",
              "ignore"]

    tg_writer_scalp(coin_name)

    df = pd.read_csv(coin_name + "1MINTG.csv", names=titles)


    close_level = df["Close"]
    open_time = df["Open Time"]

    def calculate_time(number):
        return dt.fromtimestamp(open_time.iloc[number] / 1000)


    rsi = ta.rsi(close=close_level, length=14)

    if rsi.iloc[len(close_level) - 1] > 70:
        message("\nOVERBOUGHT!!!\nCURRENT RSI VALUE : "+ str(rsi.iloc[len(close_level) - 1])+"\n" +
             str( calculate_time(len(close_level) - 1)))

    if rsi.iloc[len(close_level) - 1] < 30:
        message("\nOVERSOLD!!!\nCURRENT RSI VALUE : "+str( rsi.iloc[len(close_level) - 1])+"\n" +str (calculate_time(len(close_level) - 1)))



message("YENİDEN BAŞLADI")


while True:
    try:
        if (time.localtime().tm_sec == 59):
            candle_stick_scalp("NEARUSDT")
            
        if (time.localtime().tm_min == 29 or time.localtime().tm_min == 59) and time.localtime().tm_sec == 50:
            candle_stick("NEARUSDT")
            candle_stick("BTCUSDT")

    except:
        message("BİR HATA OLUŞTU")
