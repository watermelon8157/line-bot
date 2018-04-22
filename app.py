from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('XHFuFp3irD+5yex6NnFv7OlsTrwnx9F3/CUhvnWmpIuMaF9NGizD1mF9orKnxIrVX5ZofPhMiYL5YPpoWxvLugiLro6R+AqAEXgkQDv/EVu+PwFDZP5HRazhW7TX68nD1X8B9hPgYjHJsyqI+FUorgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6d0e190d410374917e4751e936b302ef')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	msg = event.message.text
    msg = msg.encode('utf-8')
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))