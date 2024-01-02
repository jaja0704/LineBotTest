
import json
import hmac
import hashlib
import base64
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

line_bot_api = LineBotApi(os.environ.get('zIT6hokPgn8EPo3xS1W4EiI791CWpZS0FE2ecr6mdXF+mIpngYxCEz9oE1B7yUyXs/PkPGbqX4BnovCmsUwcYsjiY5psqGLeVKBvxNHxlK48lJseXsJbE6KaqXQ2sATXMpCwLakmwhNCyL9O22oWaQdB04t89/1O/w1cDnyilFU='))
channel_secret = os.environ.get('12564165ca992343a29c57ef28d4adf4')
handler = WebhookHandler(channel_secret)

def linebot(request):
    if request.method == 'POST':
        if 'X-Line-Signature' not in request.headers:
            return 'Error: Invalid source', 403
        else:
            # get X-Line-Signature header value
            x_line_signature = request.headers['X-Line-Signature']
            # get body value
            body = request.get_data(as_text=True)
            # decode body
            hash = hmac.new(channel_secret.encode('utf-8'),
                        body.encode('utf-8'), hashlib.sha256).digest()
            signature = base64.b64encode(hash).decode('utf-8')
            # Compare x-line-signature request header and the signature
            if x_line_signature == signature:
                try:
                    json_data = json.loads(body)
                    handler.handle(body, x_line_signature)
                    tk = json_data['events'][0]['replyToken']         # 取得 reply token
                    msg = json_data['events'][0]['message']['text']   # 取得 訊息 
                    line_bot_api.reply_message(tk,TextSendMessage(msg)) # 回傳 訊息
                    # print(msg, tk)
                    return 'OK', 200
                except:
                    print('error')
            else:
                return 'Invalid signature', 403
    else:
        return 'Method not allowed', 400
   
