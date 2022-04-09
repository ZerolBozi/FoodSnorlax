from app import app,line_bot_api,handler,db
from flask import request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, 
    TextMessage, StickerMessage, ImageMessage, LocationMessage,
    TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, 
    QuickReply, QuickReplyButton, 
    MessageAction, LocationAction, PostbackAction
)

import time
import search
import random

class users(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, nullable = False ,primary_key = True)
   uid = db.Column(db.Text, nullable = False)
   name = db.Column(db.Text, nullable = False)
   lastOrder = db.Column(db.Text)

   def __init__(self, uid, name, lastOrder):
        self.uid = uid
        self.name = name
        self.lastOrder = lastOrder

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_Postback(event):
    postbackData = event.postback.data
    if 'userChoose' in postbackData:
        postbackData = postbackData.replace('userChoose','')
        global userChoose
        userChoose = postbackData
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
            text=f'您想要的是"{postbackData}"嗎？\n如想開始尋找美食請點選下方按鈕分享目前的位置給我們！',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=LocationAction(label="尋找")
                    ),
                ]
            )))

@handler.add(MessageEvent,message=TextMessage)
def handle_TextMessage(event):
    user_msg = event.message.text
    user_id = str(event.source.user_id)
    user_data = users.query.filter_by(uid=user_id).first()
    user_info = line_bot_api.get_profile(user_id)
    if user_data is None:
        userData = users(user_id, user_info.display_name,'')
        db.session.add(userData)
        db.session.commit()
        msg = [TextSendMessage(text='哈囉！我是FoodSnorlax，歡迎使用尋找美食小助手～\n有任何的問題都可以輸入"幫助"\n我可以給你解答呦$',emojis=[{"index":54,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"002"}]),
            StickerSendMessage(11538,51626494)]
        line_bot_api.reply_message(event.reply_token,msg)
    else:
        evaluationKeywords = ['評價','評分']
        if user_msg not in evaluationKeywords:
            now_time = int(time.strftime("%H",time.localtime()))
            if 4 < now_time < 11: 
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='今早我想來點...',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="漢堡", data="userChoose漢堡")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="蛋餅", data="userChoose蛋餅")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="中式早餐", data="userChoose中式早餐")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="西式早餐", data="userChoose西式早餐")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="隨機", data="userChoose隨機")
                            ),
                        ]
                    )))
            elif 10 < now_time < 15:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='今早我想來點...',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="早午餐", data="userChoose早午餐")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="拉麵", data="userChoose拉麵")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="水餃", data="userChoose水餃")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="便當", data="userChoose便當")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="隨機", data="userChoose隨機")
                            ),
                        ]
                    )))
            elif 14 < now_time < 16:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='下午我想來點...',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="下午茶", data="userChoose下午茶")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="甜點", data="userChoose甜點")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="甜點隨機", data="userChoose甜點隨機")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="隨機", data="userChoose隨機")
                            ),
                        ]
                    )))
            elif 15 < now_time < 21:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='今晚我想來點...',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="火鍋", data="userChoose火鍋")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="拉麵", data="userChoose拉麵")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="水餃", data="userChoose水餃")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="便當", data="userChoose便當")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="隨機", data="userChoose隨機")
                            ),
                        ]
                    )))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='宵夜我想來點...',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="有開就好", data="userChoose有開就好")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="評價高", data="userChoose評價高")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="評價多", data="userChoose評價多")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="評價高且多", data="userChoose評價高且多")
                            ),
                        ]
                    )))
        elif user_msg in evaluationKeywords:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=StickerMessage)
def handle_StickerMessage(event):
    defaultPackageIdList = ['1','2','3','4','446','789','1070','6136','6325','6359','6362','6370','6632','8515','8522','8525','11537','11538','11539']
    if event.message.package_id in defaultPackageIdList:
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(event.message.package_id,event.message.sticker_id))
    else:
        msg = [TextSendMessage(text="I don't have that sticker."),TextSendMessage(text="Can you buy it for me? $",emojis=[{"index":23,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"003"}])]
        line_bot_api.reply_message(event.reply_token,msg)

@handler.add(MessageEvent, message=LocationMessage)
def handle_LocationMessage(event):
    # searchKeyword = ['eat','food','dinner','breakfast','hotpot']
    # foodKeywords = ['漢堡','蛋餅','中式早餐','西式早餐','早午餐','拉麵','水餃','便當','火鍋']
    nightMeal = {'有開就好':0,'評價高':1,'評價多':2,'評價高且多':3}
    global userChoose
    keyword = userChoose
    # address = event.message.address
    # debug
    # print(address)
    latitude = event.message.latitude
    longitude = event.message.longitude

    rating_sort = False
    rating_total_sort = False
    rndChoose = False

    if '隨機' in keyword:
        keyword = 'food' if keyword.replace('隨機','') == '' else keyword.replace('隨機','')
        rndChoose = True
    
    if keyword in nightMeal.keys():
        rndChoose = True if nightMeal[keyword] == 0 else False
        rating_sort = nightMeal[keyword] == 1 or nightMeal[keyword] == 3
        rating_total_sort = nightMeal[keyword] == 2 or nightMeal[keyword] == 3
        keyword = 'food' 
    
    res = search.search_Food(latlng=[latitude,longitude],keyword=keyword,open_now=True,search=True,rating_sort=rating_sort,rating_total_sort=rating_total_sort)

    if rndChoose:
        res = random.sample(res,1)

    msg = []

    msg.append(TextSendMessage(text='FoodSnolax小助手：\n尋找的結果如下$',emojis=[{"index":22,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"021"}]))

    title = f"{res[0]['name']} \n評分：{res[0]['rating']}\n總評論數：{res[0]['user_ratings_total']}"
    msg.append(LocationSendMessage(title,res[0]['vicinity'],res[0]['geometry']['location']['lat'],res[0]['geometry']['location']['lng']))
    line_bot_api.reply_message(event.reply_token,msg)