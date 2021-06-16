import time
import dataset as ds
import requests

bot_token = 'kek'

def send_announcments_to_all(bot_message):
    data = ds.get_all_ids_and_names()

    for i in range(len(data)):
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(data[i]['id']) + '&text=' + bot_message
        print(send_text)
        response = requests.get(send_text)
        print(response.json())
        time.sleep(1)


def send_announcments_to_specific(names, bot_message):
    data = ds.get_specific_ids_and_names(names)
    print("-----------------------")

    for i in range(len(data)):
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(data[i]['id']) + '&text=' + bot_message
        print(send_text)
        response = requests.get(send_text)
        print(response.json())
        time.sleep(1)

# send_announcments("Testing new feature! Hope it works.")

#send_announcments_to_specific("Печков Н.В.", "А сейчас а? А? а? А?")
