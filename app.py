from KinshipBot import KinshipBot

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,
)

app = Flask(__name__)

kinshipBot = KinshipBot()
lineBot = LineBotApi(kinshipBot.Config['LINE_ACCESS_TOKEN'])
handler = WebhookHandler(kinshipBot.Config['LINE_SECRET_TOKEN'])
kinshipBot.setLineBot(lineBot)


@app.route("/health", methods=['GET'])
def health():
    return "OK"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    kinshipBot.handleMessage(event, event.message.text)


if __name__ == "__main__":
    app.run()
