

import time

import requests


def message(bot_mesaj):
    id_list = ["1598072365"]

    for i in id_list:
        bot_token = "5424258200:AAGNGZlN5HevI2fnyQedvD7v8XPsFFSBBJA"
        url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + i + "&parse_mode=Markdown&text=" + bot_mesaj
        response = requests.get(url)
        time.sleep(1)





message("RESTARTED")

while True:

    try:
        if (time.localtime().tm_min % 30 == 29) and time.localtime().tm_sec == 50:
            message("30MIN")
        if (time.localtime().tm_hour % 4 == 2) and (time.localtime().tm_min % 60 ==59) and time.localtime().tm_sec == 50:
            message("4HOUR")
            
    except:
        message("THERE IS AN ERROR")
