import json
import requests
import time
import urllib

import config
from dbhelper import DBHelper

#logging boilerplate
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

## enable to log to files
# fh = logging.FileHandler('log.txt')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

db = DBHelper()

#TOKEN = "" #define token here as a string
# TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    logger.debug(js)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates,last_update_id):
    import ipdb;ipdb.set_trace
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        if "text" in update["message"].keys():
            text = update["message"]["text"]
            items = db.get_items(text)
            if text in items:
                response = db.get_response(text)
                if len(response) == 1:
                    send_message(response[0][1],chat)
                else:
                    send_message(response[0][1],chat)
                return 0
            else:
                send_message("I don't understand brah, teach me?",chat)
                new_updates = get_updates(last_update_id)
                while len(new_updates["result"]) == 0:
                    new_updates = get_updates(last_update_id)
                taught_response = new_updates["result"][0]["message"]["text"]
                db.add_item(text,taught_response)
                send_message("I hope I remember brah",chat)
                return 1
        else:
            if "left_chat_member" in update["message"].keys():
                send_message("Aww {} sucks".format(update["message"]["left_chat_member"]["first_name"]),chat)
            elif "new_chat_member" in update["message"].keys():
                send_message("Welcome to da club {} boi".format(update["message"]["new_chat_member"]["first_name"]),chat)
            return 0

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

# import ipdb;ipdb.set_trace()

def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_result = handle_updates(updates,last_update_id)
            last_update_id = last_update_id + handle_result
        time.sleep(0.5)


if __name__ == '__main__':
    main()
