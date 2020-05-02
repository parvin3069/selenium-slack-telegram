import telegram
import sc_msg
import traceback
from envparse import env


env.read_envfile()
Messenger = ''
if env.str("MESSENGER") == "Slack":
    Messenger = sc_msg.Slack()
if env.str("MESSENGER") == "Telegram":
    Messenger = telegram.Telegram()

try:
    env.str("MESSENGER")
    Messenger.send_alert(env.str('ENV'))
    print("Report sent.")
except Exception as e:
    exc = traceback.format_exc()
    Messenger.send_alert(env.str('ENV'), json_err=True)
    print(exc)
