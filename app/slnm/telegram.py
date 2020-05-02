import os
from datetime import datetime as dt
import glob
import json
import re
import telebot
from telebot import apihelper
import exceptions
from envparse import env


env.read_envfile()


class Telegram:
    """
    :Methods:
     - today_date
     - send_alert
    """
    def today_dt(self) -> str:
        """
        Function to get the date and time in the format: 31-12-20_00-00-00.

        :Usage:
            today_dt = component.today_dt()
        """
        now = dt.today().strftime('%d-%m-%y_%H-%M')
        return now


    def send_alert(self, t_env: str, json_err=False):
        """ Function for processing json files and creating a single file from them,
        sending a message and this file to telegram chat.

        :Args:
         - t_env: name of environment (ex: prod, test.)
         - json_err: boolean, default: False, if True, then send msg: Report not sent.

        :Usage:
            send_alert = telegram.send_alert('test', json_err=True)
        """
        token = env.str('T_TOKEN')  # token of telegram bot
        chat_id = env.str('T_CHAT_ID')  # ID of telegram chat
        bot = telebot.TeleBot(token)
        apihelper.proxy = {env.str('T_PROTOCOL'):env.str('T_PROXY')}
        # proxy for telegram

        date = self.today_dt()
        file = f"{t_env}_log_{date}.json"
        read_files = glob.glob("*_log_*")
        res_data = []
        msg_text = ''

        if json_err is True:
            msg = 'Report not sent.'
            bot.send_message(chat_id, msg)
            os.remove(file)
            return

        exception = exceptions.exc('warning')

        with open(file, "w") as outfile:  # creating or opening json file
            for f in read_files:
                with open(f, "r") as infile:  # opening individual json files one by one
                    tmp_data = json.load(infile)
                    res_data.append(tmp_data)
                    """
                    loop checking objects using the error tag for errors
                    """
                    for i in tmp_data:
                        count = 0
                        if i['Error'] is None:
                            msg_text += '✅ ' + i['Case'] + '\n'
                        else:
                            for exc in exception:
                                if re.search(exc, i['Error']):
                                    msg_text += '⚠️ ' + i['Case'] + '\n'
                                    count += 1
                            if count == 0:
                                msg_text += '❌ ' + i['Case'] + '\n'

                os.remove(f)  # deleting json file(s)
            json.dump(res_data, outfile, indent=4, ensure_ascii=False)  # parsing json
            bot.send_message(chat_id, msg_text)  # sending text to chat
        with open(file, 'r') as msg_file:
            bot.send_document(chat_id, msg_file)  # sending file to chat
        os.remove(file)  # deleting json file


