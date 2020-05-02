import glob
import json
import os
import random
import re
import exceptions
from datetime import datetime as dt
from slack.web.client import WebClient
from envparse import env


env.read_envfile()


token = env.str('S_TOKEN')
client = WebClient(token=token)


class Slack:
    """
    :Methods:
    - send_msg
    - send_file
    - blocks
    - gifs
    - today_date
    - send_alert
    """
    def send_msg(self, channel, msg):
        client.chat_postMessage(
            channel=channel,
            blocks=msg
        )

    def send_file(self, channel, file, type='', comment=''):
        client.files_upload(
            channels=channel,
            file=file,
            filename=file,
            filetype=type,
            initial_comment=comment
        )

    def blocks(self, msg_text):
        gif = self.gifs()
        blocks = {
            "success_block": {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*`TESTS PASSED SUCCESSFULLY`*"
                }
            },
            "error_block": {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*`UNFORTUNATELY, THERE ARE ERRORS`*"
                }
            },
            "image_block": {
                "type": "image",
                "image_url": gif,
                "alt_text": "УРАААААААААААААААА"
            },
            "title_block": {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Autotests report*"
                }
            },
            "divider": {
                "type": "divider"
            },
            "case_list": {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": msg_text
                    }
                ]
            }
        }
        return blocks

    def gifs(self):
        links = [
            "https://i.gifer.com/1IAK.gif",
            "https://i.gifer.com/1W9X.gif",
            "https://i.gifer.com/14Um.gif"
        ]

        return random.choice(links)

    def today_dt(self):
        """
        Function to get the date and time in the format: 31-12-20_00-00-00.

        :Usage:
            today_dt = component.today_dt()
        """
        now = dt.today().strftime('%d-%m-%y_%H-%M')
        return now

    def send_alert(self, s_env, json_err=False):
        """ Function for processing json files and creating a single file from them,
        sending a message and this file to slack channel.

        :Args:
         - s_env: name of environment (ex: prod, test.)
         - json_err: boolean, default: False, if True, then send msg: Report not sent.

        :Usage:
            send_alert = slack.send_alert('test', json_err=True)
        """
        res_data = []
        msg_text = ''
        date = self.today_dt()
        file = f"{s_env}_log_{date}.json"
        read_files = glob.glob("*_log_*")

        if json_err is True:
            b = self.blocks(msg_text)
            block = {
                        "error_block": {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*`'REPORT NOT SENT'`*"
                    }
                }
            }
            blocks = [b["title_block"], b["divider"], block["error_block"]]
            self.send_msg(channel=env.str('S_CHANNEL'), msg=blocks)
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
                    n = False
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
                            n = True
                os.remove(f)  # deleting json file(s)
            json.dump(res_data, outfile, indent=4, ensure_ascii=False)  # parsing json


        b = self.blocks(msg_text)
        blocks = []
        if n is False:
            blocks = [b["title_block"], b["divider"], b["success_block"], b["image_block"]]

        if n is True:
            blocks = [b["title_block"], b["divider"], b["error_block"], b["case_list"]]

        self.send_msg(channel=env.str('S_CHANNEL'), msg=blocks)
        self.send_file(channel=env.str('S_CHANNEL'), file=file, type='javascript')
        os.remove(file)  # parsing json
