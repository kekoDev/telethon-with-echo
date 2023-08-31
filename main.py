from telethon import TelegramClient, sync, functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest
import requests
from time import sleep

API_ID = '25875948'
API_HASH = 'bbc8cd4753b320c932bd56254d2917a0'
user_phone = input("ادخل رقم الهاتف : ")
client = TelegramClient(user_phone, API_ID, API_HASH)
    
def main():
    client.connect()
    if not client.is_user_authorized():
        print("تم تسجيل الخروج من الحساب")
        return 0
    else:
        user_id = client.get_me().id
        bot_username = ""
        echo_token = ""
        while (bot_username == ""):
            username_bot = input("ادخل معرف البوت: ")
            if (username_bot):
                response = requests.request("GET", f"https://bot.keko.dev/api/?login={user_id}&bot_username={username_bot}")
                response_json = response.json()
                if (response_json["ok"] == True):
                    bot_username = username_bot
                    echo_token = response_json["token"]
                    print(f"- تم تسجيل الدخول بنجاح, توكن حسابك : {echo_token}")
                    break
                else:
                    print("- "+response_json["msg"])
        while (True):
            response = requests.request("GET", f"https://bot.keko.dev/api/?token={echo_token}")
            response_json = response.json()
            if (response_json["ok"] == False):
                print("- "+response_json["msg"])
                break
            print("- "+response_json["type"]+" -> "+response_json["return"]+"")
            if (response_json["type"] == "link"):
                try:
                    client(ImportChatInviteRequest(response_json["tg"]))
                    sleep(2)
                    entity = client.get_entity(response_json["return"])
                    messages = client.get_messages(entity, limit=10)
                    MSG_IDS = [message.id for message in messages]
                    client(GetMessagesViewsRequest(
                        peer=response_json["return"],
                        id=MSG_IDS,
                        increment=True
                    ))
                except:
                    print("- خطآ : انتظار 100 ثانيه")
                    sleep(100)
            else:
                try:
                    client(JoinChannelRequest(response_json["return"]))
                    sleep(2)
                    entity = client.get_entity(response_json["return"])
                    messages = client.get_messages(entity, limit=10)
                    MSG_IDS = [message.id for message in messages]
                    client(GetMessagesViewsRequest(
                        peer=response_json["return"],
                        id=MSG_IDS,
                        increment=True
                    ))
                except:
                    print("- خطآ : انتظار 100 ثانيه")
                    sleep(100)
            response = requests.request("GET", f"https://bot.keko.dev/api/?token={echo_token}&done="+response_json["return"])
            response_json = response.json()
            if (response_json["ok"] == False):
                print("- "+response_json["msg"])
            else:
                print("- اصبح عدد نقاطك : ",response_json["c"])
            print("- انتظار 30 ثانيه")
            sleep(30)
        client.disconnect()

with client:
    client.loop.run_until_complete(main())
