import logging
import os
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telethon import TelegramClient, sync, functions, errors, events, types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest
from telethon.tl.functions.messages import SendReactionRequest
import requests
from time import sleep
import multiprocessing
import json
API_ID = '8'
API_HASH = '7245de8e747a0d6fbe11f7cc14fcc0bb'
bot_token = ""
running_processes = {}
try:
    with open("echo_data.json", "r") as json_file:
        info = json.load(json_file)
except FileNotFoundError:
    info = {}
if "token" not in info:
    while (True):
        bot_token = input("Enter the bot token : ")
        response = requests.request(
            "GET", f"https://api.telegram.org/bot{bot_token}/getme")
        response_json = response.json()
        if (response_json["ok"] == True):
            info["token"] = bot_token
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
            break
        else:
            print("token is not correct !")
else:
    bot_token = info["token"]

if "sudo" not in info:
    info["sudo"] = input("Enter the your telegram ID : ")
    info["admins"] = {}
    with open("echo_data.json", "w") as json_file:
        json.dump(info, json_file)


def background_task(phonex, bot_username, sudo):
    try:
        client = TelegramClient(f"echo_ac/{sudo}/{phonex}", API_ID, API_HASH)

        @client.on(events.NewMessage)
        async def handle_new_message(event):
            if event.is_channel:
                await client(GetMessagesViewsRequest(
                    peer=event.chat_id,
                    id=[event.message.id],
                    increment=True
                ))
        client.connect()
    except:
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"حدث خطا في الحساب : {phonex}"
        })
        client.disconnect()
        return 0
    if not client.is_user_authorized():
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"حدث خطا في الحساب : {phonex}"
        })
        client.disconnect()
        return 0
    else:
        user_id = client.get_me().id
        response = requests.request(
            "GET", f"https://bot.keko.dev/api/?login={user_id}&bot_username={bot_username}")
        response_json = response.json()
        if (response_json["ok"] == True):
            echo_token = response_json["token"]
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": sudo,
                "text": f"- تم تسجيل الدخول بنجاح, توكن حسابك : {echo_token} \n\n- {phonex}"
            })
            while (True):
                response = requests.request(
                    "GET", f"https://bot.keko.dev/api/?token={echo_token}")
                response_json = response.json()
                if (response_json["ok"] == False):
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": "- "+response_json["msg"]+f" \n\n- {phonex}"
                    })
                    client.disconnect()
                    break
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                    "chat_id": sudo,
                    "text": "- جاري الاشتراك في : "+response_json["type"]+" -> "+response_json["return"]+f" \n\n- {phonex}"
                })
                if (response_json["type"] == "link"):
                    try:
                        client(ImportChatInviteRequest(response_json["tg"]))
                        sleep(2)
                        messages = client.get_messages(
                            int(response_json["return"]), limit=20)
                        MSG_IDS = [message.id for message in messages]
                        client(GetMessagesViewsRequest(
                            peer=int(response_json["return"]),
                            id=MSG_IDS,
                            increment=True
                        ))
                        try:
                            client(SendReactionRequest(
                                peer=int(response_json["return"]),
                                msg_id=messages[0].id,
                                big=True,
                                add_to_recent=True,
                                reaction=[types.ReactionEmoji(
                                    emoticon='👍'
                                )]
                            ))
                        except:
                            print("error")
                    except Exception as e:
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- خطآ : انتظار 100 ثانيه \n\n{str(e)}\n\n- {phonex}"
                        })
                        sleep(100)
                else:
                    try:
                        client(JoinChannelRequest(response_json["return"]))
                        sleep(2)
                        entity = client.get_entity(response_json["return"])
                        messages = client.get_messages(entity, limit=20)
                        MSG_IDS = [message.id for message in messages]
                        client(GetMessagesViewsRequest(
                            peer=response_json["return"],
                            id=MSG_IDS,
                            increment=True
                        ))
                        try:
                            client(SendReactionRequest(
                                peer=response_json["return"],
                                msg_id=messages[0].id,
                                big=True,
                                add_to_recent=True,
                                reaction=[types.ReactionEmoji(
                                    emoticon='👍'
                                )]
                            ))
                        except:
                            print("error")
                    except Exception as e:
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- خطآ : انتظار 100 ثانيه \n\n{str(e)}\n\n- {phonex}"
                        })
                        sleep(100)
                response = requests.request(
                    "GET", f"https://bot.keko.dev/api/?token={echo_token}&done="+response_json["return"])
                response_json = response.json()
                if (response_json["ok"] == False):
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": f"- "+response_json["msg"]+f" \n\n- {phonex}"
                    })
                else:
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": f"- اصبح عدد نقاطك "+str(response_json["c"])+f" \n\n- {phonex}"
                    })
                sleep(30)
        else:
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": sudo,
                "text": f"- "+response_json["msg"]+f" \n\n- {phonex}"
            })
        client.disconnect()
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"- تم ايقاف عمل الرقم : {phonex}"
        })
        stop_background_task(phonex, sudo)


def start_background_task(phone, bot_username, chat_id):
    if str(chat_id) not in running_processes:
        running_processes[str(chat_id)] = {}
    if phone in running_processes[str(chat_id)]:
        process = running_processes[str(chat_id)][phone]
        process.terminate()
        del running_processes[str(chat_id)][phone]
    process = multiprocessing.Process(
        target=background_task, args=(phone, bot_username, chat_id))
    process.start()
    running_processes[str(chat_id)][phone] = process


def stop_background_task(phone, chat_id):
    if str(chat_id) not in running_processes:
        running_processes[str(chat_id)] = {}
    if phone in running_processes[str(chat_id)]:
        process = running_processes[str(chat_id)][phone]
        process.terminate()
        del running_processes[str(chat_id)][phone]


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
if not os.path.isdir("echo_ac"):
    os.makedirs("echo_ac")
what_need_to_do_echo = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    print(update)
    if (update.message.chat.type == "private"):
        if (update.message.chat.id == info["sudo"]):
            if not os.path.isdir("echo_ac/"+str(update.message.chat.id)):
                os.makedirs("echo_ac/"+str(update.message.chat.id))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضافه حساب", callback_data="addecho"),
                    InlineKeyboardButton("مسح حساب", callback_data="delecho"),
                ],
                [
                    InlineKeyboardButton("الحسابات", callback_data="myecho")
                ],
                [
                    InlineKeyboardButton(
                        "اضافه ادمن", callback_data="addadminecho"),
                    InlineKeyboardButton(
                        "مسح ادمن", callback_data="deladminecho"),
                ],
                [
                    InlineKeyboardButton(
                        "الادمنيه", callback_data="myadminsecho"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("مرحبا بك في سورس التجميع الخاص ببوتات ايكو :\n\n- اشترك في قناة تحديثات بوت التجميع : @Echo_Auto", reply_markup=reply_markup)
        elif (str(update.message.chat.id) in info["admins"]):
            if not os.path.isdir("echo_ac/"+str(update.message.chat.id)):
                os.makedirs("echo_ac/"+str(update.message.chat.id))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضافه حساب", callback_data="addecho"),
                    InlineKeyboardButton("مسح حساب", callback_data="delecho"),
                ],
                [
                    InlineKeyboardButton("الحسابات", callback_data="myecho")
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("مرحبا بك في سورس التجميع الخاص ببوتات ايكو :", reply_markup=reply_markup)


async def echoMaker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    if (update.message.chat.type != "private"):
        return 0
    if (update.message.chat.id != info["sudo"] and str(update.message.chat.id) not in info["admins"]):
        return 0
    if (update.message.text and (str(update.message.chat.id) in what_need_to_do_echo)):
        if (what_need_to_do_echo[str(update.message.chat.id)] == "addecho"):
            client = TelegramClient(
                f"echo_ac/{update.message.chat.id}/{update.message.text}", API_ID, API_HASH)
            try:
                await client.connect()
                what_need_to_do_echo[str(
                    update.message.chat.id)+":phone"] = update.message.text
                eeecho = await client.send_code_request(update.message.text)
                print(eeecho)
                what_need_to_do_echo[str(
                    update.message.chat.id)+":phone_code_hash"] = eeecho.phone_code_hash
                await update.message.reply_text(f"ارسل رمز تسجيل الدخول : ", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = "echocode"
            except Exception as e:
                await client.log_out()
                what_need_to_do_echo[str(update.message.chat.id)] = ""
                await update.message.reply_text(f"حدث خطأ غير متوقع: {str(e)}", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
            await client.disconnect()
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "deladminecho"):
            if os.path.isdir("echo_ac/"+str(update.message.text)):
                os.rmdir("echo_ac/"+str(update.message.text))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if "admins" not in info:
                info["admins"] = {}
            if str(update.message.text) in info["admins"]:
                del running_processes[str(update.message.text)]
                with open("echo_data.json", "w") as json_file:
                    json.dump(info, json_file)
                await update.message.reply_text(f"تم مسح الادمن بنجاح.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                if str(update.message.text) not in running_processes:
                    running_processes[str(update.message.text)] = {}
                for phone in running_processes[str(update.message.text)]:
                    process = running_processes[str(
                        update.message.text)][phone]
                    process.terminate()
                    del running_processes[str(update.message.text)]
            else:
                await update.message.reply_text(f"لا يوجد هكذا ادمن.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "addadminecho"):
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if not os.path.isdir("echo_ac/"+str(update.message.text)):
                os.makedirs("echo_ac/"+str(update.message.text))
            if "admins" not in info:
                info["admins"] = {}
            info["admins"][str(update.message.text)] = str(5)
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
            await update.message.reply_text(f"تم اضافه ادمن جديد بنجاح.\n\n- يمكن للادمن اضافه 5 حسابات (يمكنك تعديل ذالك من قسم الادمنيه)", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "echocode"):
            what_need_to_do_echo[str(update.message.chat.id)] = "anthercode"
            what_need_to_do_echo[str(
                update.message.chat.id)+"code"] = update.message.text
            await update.message.reply_text(f"ارسل رمز تحقق بخطوتين (اذا لم يكن هناك رمز ارسل اي شيء): ")
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "anthercode"):
            client = TelegramClient(f"echo_ac/{update.message.chat.id}/"+str(
                what_need_to_do_echo[str(update.message.chat.id)+":phone"]), API_ID, API_HASH)
            await client.connect()
            try:
                await client.sign_in(phone=what_need_to_do_echo[str(update.message.chat.id)+":phone"], code=what_need_to_do_echo[str(update.message.chat.id)+"code"], phone_code_hash=what_need_to_do_echo[str(update.message.chat.id)+":phone_code_hash"])
                await update.message.reply_text(f"تم تسجيل الدخول بنجاح : "+str(what_need_to_do_echo[str(update.message.chat.id)+":phone"]), reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = ""
            except errors.SessionPasswordNeededError:
                await client.sign_in(password=update.message.text, phone_code_hash=what_need_to_do_echo[str(update.message.chat.id)+":phone_code_hash"])
                await update.message.reply_text(f"تم تسجيل الدخول بنجاح \n\n- "+str(what_need_to_do_echo[str(update.message.chat.id)+":phone"]), reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = ""
            except Exception as e:
                await client.log_out()
                what_need_to_do_echo[str(update.message.chat.id)] = ""
                await update.message.reply_text(f"حدث خطأ غير متوقع: {str(e)}", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
            await client.disconnect()
        elif (what_need_to_do_echo[str(update.message.chat.id)].startswith("setlimt:")):
            admin = what_need_to_do_echo[str(
                update.message.chat.id)].split(":")[1]
            await update.message.reply_text(f"تم تعين عدد الحسابات المسموحه لهذه الادمن !\n\n- {admin}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="myadminsecho")],
            ]))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if "admins" not in info:
                info["admins"] = {}
            info["admins"][str(admin)] = str(update.message.text)
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
        elif (what_need_to_do_echo[str(update.message.chat.id)].startswith("run:")):
            filename = what_need_to_do_echo[str(
                update.message.chat.id)].split(":")[1]
            await update.message.reply_text(f"تم بدء العمل !\n\n- {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            start_background_task(
                filename, update.message.text, update.message.chat.id)
            what_need_to_do_echo[str(update.message.chat.id)] = ""


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    query = update.callback_query
    await query.answer()
    if (query.message.chat.type != "private"):
        return 0
    if (str(query.message.chat.id) != str(info["sudo"]) and str(query.message.chat.id) not in info["admins"]):
        return 0
    if (query.data == "addecho"):
        if (query.message.chat.id == info["sudo"]):
            what_need_to_do_echo[str(query.message.chat.id)] = query.data
            await query.edit_message_text(text=f"ارسل رقم الحساب الان :", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
        elif (str(query.message.chat.id) in info["admins"]):
            directory_path = Path(f"echo_ac/{query.message.chat.id}")
            file_list = [file.name for file in directory_path.iterdir(
            ) if file.is_file() and file.name.endswith('.session')]
            file_list = list(set(file_list))
            if (int(len(file_list)) <= int(info["admins"][str(query.message.chat.id)])):
                what_need_to_do_echo[str(query.message.chat.id)] = query.data
                await query.edit_message_text(text=f"ارسل رقم الحساب الان :", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
            else:
                await query.edit_message_text(text=f"لا يمكنك اضافه المزيد من الحسابات !", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
    elif (query.data == "deladminecho"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        await query.edit_message_text(text=f"ارسل ايدي الادمن الان :", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif (query.data == "addadminecho"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        await query.edit_message_text(text=f"ارسل ايدي الادمن الان :", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif (query.data == "sudohome"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (query.message.chat.id == info["sudo"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضافه حساب", callback_data="addecho"),
                    InlineKeyboardButton("مسح حساب", callback_data="delecho"),
                ],
                [
                    InlineKeyboardButton("الحسابات", callback_data="myecho")
                ],
                [
                    InlineKeyboardButton(
                        "اضافه ادمن", callback_data="addadminecho"),
                    InlineKeyboardButton(
                        "مسح ادمن", callback_data="deladminecho"),
                ],
                [
                    InlineKeyboardButton(
                        "الادمنيه", callback_data="myadminsecho"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في سورس التجميع الخاص ببوتات ايكو :", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضافه حساب", callback_data="addecho"),
                    InlineKeyboardButton("مسح حساب", callback_data="delecho"),
                ],
                [
                    InlineKeyboardButton("الحسابات", callback_data="myecho")
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في سورس التجميع الخاص ببوتات ايكو :", reply_markup=reply_markup)
    elif (query.data == "myadminsecho"):
        if "admins" not in info:
            info["admins"] = {}
        keyboard = []
        for key, value in info["admins"].items():
            button = InlineKeyboardButton(
                f"{key}", callback_data=f"setlimt:{key}")
            button2 = InlineKeyboardButton(
                str(value), callback_data=f"setlimt:{key}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="sudohome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الادمنيه في البوت : \n\n- اضغط على ايدي لتعديل عدد الحسابات المسموح ", reply_markup=reply_markup)
    elif query.data.startswith("setlimt:"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        admin = query.data.split(":")[1]
        await query.edit_message_text(f"ارسل عدد الحسابات المسموحه لهذه الشخص : \n\n- {admin}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="myadminsecho")],
        ]))
    elif (query.data == "delecho"):
        directory_path = Path(f"echo_ac/{query.message.chat.id}")
        file_list = [file.name for file in directory_path.iterdir(
        ) if file.is_file() and file.name.endswith('.session')]
        file_list = list(set(file_list))
        keyboard = []
        for filename in file_list:
            filename = filename.split(".")[0]
            button = InlineKeyboardButton(
                f"{filename}", callback_data=f"del:{filename}")
            button2 = InlineKeyboardButton(
                f"❌", callback_data=f"del:{filename}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="sudohome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الحسابات الخاصه بك : \n\n- اضغط على ❌ للمسح ", reply_markup=reply_markup)
    elif query.data.startswith("del:"):
        filename = query.data.split(":")[1]
        stop_background_task(filename, query.message.chat.id)
        try:
            client = TelegramClient(
                f"echo_ac/{query.message.chat.id}/{filename}", API_ID, API_HASH)
            await client.connect()
            await client.log_out()
            await client.disconnect()
            what_need_to_do_echo[str(query.message.chat.id)] = ""
            await query.edit_message_text(f"تم تسجيل الخروج من رقم : {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="delecho")],
            ]))
        except:
            await query.edit_message_text(f"لا يوجد هكذا رقم : {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="delecho")],
            ]))
    elif (query.data == "myecho"):
        directory_path = Path(f"echo_ac/{query.message.chat.id}")
        file_list = [file.name for file in directory_path.iterdir(
        ) if file.is_file() and file.name.endswith('.session')]
        file_list = list(set(file_list))
        keyboard = []
        if str(query.message.chat.id) not in running_processes:
            running_processes[str(query.message.chat.id)] = {}
        for filename in file_list:
            filename = filename.split(".")[0]
            if filename in running_processes[str(query.message.chat.id)]:
                button = InlineKeyboardButton(
                    f"{filename}", callback_data=f"stop:{filename}")
                button2 = InlineKeyboardButton(
                    f"✅ | اضغط للايقاف", callback_data=f"stop:{filename}")
            else:
                button = InlineKeyboardButton(
                    f"{filename}", callback_data=f"run:{filename}")
                button2 = InlineKeyboardButton(
                    f"❌ | اضغط للتشغيل", callback_data=f"run:{filename}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="sudohome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الحسابات الخاصه بك : \n\n- ✅ = يعمل \n- ❌ = متوقف ", reply_markup=reply_markup)
    elif query.data.startswith("run:"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        filename = query.data.split(":")[1]
        await query.edit_message_text(f"ارسل معرف البوت الذي تريد للحساب التجميع منه : \n\n- {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif query.data.startswith("stop:"):
        filename = query.data.split(":")[1]
        await query.edit_message_text(f"تم ايقاف عمل الرقم : {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        stop_background_task(filename, query.message.chat.id)


def main() -> None:
    global what_need_to_do_echo
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, echoMaker))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
