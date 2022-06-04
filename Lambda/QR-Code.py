import json,os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent , TextMessage , TextSendMessage, ImageSendMessage

#初始化
linebot_api = LineBotApi(os.environ["ACCESS_TOKEN"]) #Linebot
handler = WebhookHandler(os.environ["CHACCEL_SECRET"]) #Webhook


def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        url = event.message.text
        msg = "https://api.qrserver.com/v1/create-qr-code/?data=" + url + "&size=256x256" #qrcode generator API
        linebot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=msg,preview_image_url=msg))
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
        }
