"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
import datetime

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

VERIFY_TOKEN = ""
ACCESS_TOKEN = "EAAF7Jxw4YqwBOZB9Ex2fjqfvzaPwhr8oAOVHr298S37bRs30x0MpbVvO3XI4jCEGdmVLnh1ZBrDJgJp27ExSuvBVKaaYliR8bZAsxbR4skYMrBxSzqZCIBlRECslBfWKCjSXRNNxb3LHBswcVkONwQVFrirrAwSpZC5jkkPaURNAJLP4F2BhtUGSJDPezsYUPQQZDZD"
bot = Bot(ACCESS_TOKEN)


def log(message):
    print(f'{datetime.datetime.now()}: {message}')


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            log(request.args.get("hub.challenge"))
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            log(messaging)
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        message = x['message']['text']
                        bot.send_text_message(recipient_id, message)
                    if x['message'].get('attachments'):
                        for att in x['message'].get('attachments'):
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=80, debug=True)
