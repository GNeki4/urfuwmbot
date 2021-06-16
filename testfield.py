import time
import dataset as ds
import requests

bot_token = '859875977:AAEwxEpOtglH0-tvwI-xmJc_2BmrNnEbmPE'


def send_announcments(bot_message):
    data = ds.get_all_ids_and_names()

    for i in range(len(data)):
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(data[i]['id']) + '&text=' + bot_message
        print(send_text)
        response = requests.get(send_text)
        print(response.json())
        time.sleep(1)


send_announcments("Testing new feature! Hope it works.")

