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
line_bot_api = LineBotApi('o9uXB4i+zilmMHAGAJTG2I3qUKt11k8IWRPQT7qiWN6+lnoI68dqe2u0+8gEZt/zX5ZofPhMiYL5YPpoWxvLugiLro6R+AqAEXgkQDv/EVuu2jQusfu4bfNDlBokF8qtMrDkMhISVln98BeQ2tDOWAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('32ef0f1447435e584d7832fedd4336a7')

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)