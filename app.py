import os
import requests
from decouple import config
from flask import (Flask, request, abort)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(config("LINE_CHANNEL_ACCESS_TOKEN", default = "4IdWs8utZIdEoy4PsRKlIyAx0Una3RP9HqtEurXlJj1u3jd37L6V/QHsVfiprlsbujsfog0sDcMHSS9C070U1KPUVmrO1rM922v9hf2O8aGK3j6XSFPW2fPWrBSQtWgOHzf2iOvzGZi7HWkjJAa/VgdB04t89/1O/w1cDnyilFU="))
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(config("LINE_CHANNEL_SECRET", default = "a119e4bfc78f0fb3d8cbb0bf26724579"))

class RasaClient() :
    def __init__(self, url) :
        self._base_url = url
        self._sess = requests.Session()

    def _post_rasa(self, path, data) :
        url = "{}/{}".format(self._base_url, path)
        resp = self._sess.post(url, json = data)
        resp.raise_for_status() # catch this
        return resp.json

    def post_nlu(self, message) :
        data = {"text": message}
        return self._post_rasa("model/parse", data)

    def post_action(self, message, sender = "default") :
        data = {"message": message, "sender": sender}
        return self._post_rasa("webhooks/rest/webhook", data)

@app.route("/callback", methods = ['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def message_text(event) :
    #rasa = RasaClient('http://localhost:5005')
    #sender = event.source.user_id
    #responses = rasa.post_action(event.message.text)
    #nlu = rasa.post_nlu(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = responses[0]['text']))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port)