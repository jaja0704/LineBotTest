#app.py
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import json

app = Flask(__name__)

line_bot_api = LineBotApi('Psnkw2tA4j14rYrB/TTH7xW+SMqwrs/0k9jL4gx4A8RcL4OKkHUtYmcKfvsKw0ExJ8L6nK+XrasNDi5r0d6SiDXZ6n89kpJEPemdNXBbwatQk0eTq5LWOQ4MH+PDtwMQLWraff+xqM4JR8ByYbfyPQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('36d6157978f5fd29454b2dffc2962282')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    #get json data
    json_data = json.loads(body)
    print(json_data)

    # body = request.get_data(as_text=True)
    # json_data = json.loads(body)
    # print(json_data)

    # try:
    #     signature = request.headers['X-Line-Signature']
    #     handler.handle(body, signature)
    #     tk = json_data['events'][0]['replyToken']         # 取得 reply token
    #     msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
    #     text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
    #     line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    # except:
    #     print('error')
    # return 'OK'

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    messagetest = [{
    'type': "text",
    'text': "Hello, world"
}]
    messagedump = json.dumps(messagetest)
    
    if event.message.text == "給我地址":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("https://maps.app.goo.gl/PmNmbJ7MYapXBtye7"))

    elif event.message.text == "給我菜單":
        line_bot_api.reply_message(
        event.reply_token, TextSendMessage("https://stu.ntou.edu.tw/var/file/23/1023/img/1093/CampusMap.jpg")
        )

    elif event.message.text == "你好":
        line_bot_api.reply_message(
        event.reply_token,
        messagedump)

    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()