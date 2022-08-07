import requests
import os


# function to send message in telegram channel
def sendTelegramMessage(params={}):
    # https://medium.com/javarevisited/sending-a-message-to-a-telegram-channel-the-easy-way-eb0a0b32968
    sendMessageEndpoint = "https://api.telegram.org/bot" + os.environ.get(
        'TELEGRAM_KI_TOKEN', '') + "/sendMessage"

    return requests.get(sendMessageEndpoint, params={
        'chat_id': os.environ.get('TELEGRAM_KI_CHANNEL', ''),
        'text': params['message']
    })
