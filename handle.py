from app import app,line_bot_api,handler,db
from flask import request, render_template, abort
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
from search import search_Food
from rating import checkUserExist, getAllUsers, updateLastRecord, addRating, getRatingByName
import time
import random

# home page about my bot
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/author', methods=['GET'])
def author():
    return render_template('author.html')

# line bot callback function
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

# line bot postback event function
@handler.add(PostbackEvent)
def handle_Postback(event):
    user_id = event.source.user_id
    postbackData = event.postback.data
    if 'userChoose' in postbackData:
        postbackData = postbackData.replace('userChoose','')
        global userChoose
        userChoose[user_id] = postbackData
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
            text=f'您想要的是"{postbackData}"嗎？\n如想開始尋找美食請點選下方按鈕分享目前的位置給我們！',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=LocationAction(label="尋找")
                    ),
                ]
            )))
    elif 'rating' in postbackData:
        comments_1_2 = ['評價分數只能信一半','實際走訪看看吧！','挑戰最低評價分數','這家店好像有點普通','評價參考用','雖然評價不高，但有可能會有額外的收穫']
        comments_2_3 = ['疑似是一家好店','好像有點普通呢','普通','還好','還可以','其實我也不知道好不好吃','有可能好吃有可能不好吃','有些人喜歡，有些人不喜歡','雖然評價不高，但有可能會有額外的收穫']
        comments_3_4 = ['好像一家好店！','不錯吃','感覺不錯吃呢','知道今天該吃什麼了！','為了吃這家店，我起床了','為了吃這家店，我出門了','讚哦～']
        comments_4_5 = ['真是一家好店！','評價好高，應該很好吃！','看起來好好吃ㄛ！','用料實在','便宜大碗又好吃','好吃到讚不絕口','色香味俱全','好好吃～','不可多得的美味','好吃到我阿嬤都爬起來吃ㄌ','好吃到我阿公都爬起來吃ㄌ']
        sticker_id_list = [i for i in range(1,18)] + [i for i in range(100,140)] + [i for i in range(401,431)] + [21]
        global users_choose_restaurant
        postbackData = postbackData.replace('rating','')
        rest_name = users_choose_restaurant[user_id]['name']
        keyword = userChoose[user_id]
        location = [users_choose_restaurant[user_id]['geometry']['location']['lat'],users_choose_restaurant[user_id]['geometry']['location']['lng']]
        address = users_choose_restaurant[user_id]['vicinity']
        addRating(user_id, rest_name, keyword, location, int(postbackData))
        rating = getRatingByName(rest_name)
        if rating.rating < 2:
            comments = random.choice(comments_1_2)
        elif rating.rating < 3:
            comments = random.choice(comments_2_3)
        elif rating.rating < 4:
            comments = random.choice(comments_3_4)
        else:
            comments = random.choice(comments_4_5)
        msg = []
        msg.append(TextSendMessage(text=f"—————店家資訊—————\n店名：{rest_name}\n地址：{address}\n評價：{rating.rating}\n評價數：{rating.users_rating_total}\n\nSnolax評語：{comments}"))
        msg.append(StickerSendMessage(package_id='1', sticker_id=str(random.choice(sticker_id_list))))
        line_bot_api.reply_message(event.reply_token,msg)

# line bot message event function
@handler.add(MessageEvent,message=TextMessage)
def handle_TextMessage(event):
    user_msg = event.message.text
    user_id = str(event.source.user_id)
    user_info = line_bot_api.get_profile(user_id)
    global users_data
    global users_choose_restaurant
    global userChoose
    flag = False
    try:
        if users_data != []:
            for users in users_data:
                if users.uid == user_id:
                    flag = True
    except:
        users_choose_restaurant = dict()
        users_data = getAllUsers()
        userChoose = dict()

    if not flag:
        tmpData = checkUserExist(user_id,user_info.display_name)
        users_data = users_data if tmpData == [] else tmpData
        msg = [TextSendMessage(text='哈囉！我是FoodSnorlax，歡迎使用尋找美食小助手～\n有任何的問題都可以輸入"幫助"\n我可以給你解答呦$',emojis=[{"index":54,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"002"}]),
            StickerSendMessage(11538,51626494)]
        line_bot_api.reply_message(event.reply_token,msg)
    else:
        ratingKeywords = ['評價','評分']
        ratingKeywords2 = ['1','2','3','4','5']
        helpKeywords = ['幫助','help','幫手','求救','點餐','找餐廳','找食物','小助手','助手','小幫手']
        adoutMeKeywords = ['關於我','foodsnorlax','about me','robot','about','line bot','bot','關於','簡介']
        if user_msg in ratingKeywords:
            if user_id in users_choose_restaurant.keys():
                # rest_data = users_choose_restaurant[user_id]
                line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='如果覺得值得下次光顧\n請給予$\n所以覺得尚可\n請給予$\n如果覺得不適合您的口味\n請給予$\n\n請給分（點擊數字1-5）：',
                    emojis = [{"index":14,"productId":"5ac21a18040ab15980c9b43e","emojiId":"142"},{"index":26,"productId":"5ac21a18040ab15980c9b43e","emojiId":"140"},{"index":43,"productId":"5ac21a18040ab15980c9b43e","emojiId":"138"}],
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="1", data="rating1")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="2", data="rating2")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="3", data="rating3")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="4", data="rating4")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="5", data="rating5")
                            ),
                        ]
                )))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請先使用「尋找」功能找尋附近的餐廳！！'))
        
        elif user_msg in ratingKeywords2:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(
                    text='請點擊下方按鈕進行評分！',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(label="1", data="rating1")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="2", data="rating2")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="3", data="rating3")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="4", data="rating4")
                            ),
                            QuickReplyButton(
                                action=PostbackAction(label="5", data="rating5")
                            ),
                        ]
                )))

        elif user_msg.lower() in helpKeywords:
            msg = [TextSendMessage(text='輸入關鍵字以外的文字\n就可以進行尋找食物哦$',emojis=[{"index":21,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"032"}]),
            StickerSendMessage(11538,51626501)]
            line_bot_api.reply_message(event.reply_token,msg)
        
        elif user_msg in adoutMeKeywords:
            msg = [TextSendMessage(text='我是FoodSnorlax，歡迎使用尋找美食小助手～\n有任何的問題都可以輸入"幫助"\n我可以給你解答呦$',emojis=[{"index":54,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"002"}]),
            StickerSendMessage(11538,51626494)]
            line_bot_api.reply_message(event.reply_token,msg)
            
        # other message give order function
        else:
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

# line bot sticker event function
@handler.add(MessageEvent, message=StickerMessage)
def handle_StickerMessage(event):
    defaultPackageIdList = ['1','2','3','4','446','789','1070','6136','6325','6359','6362','6370','6632','8515','8522','8525','11537','11538','11539']
    if event.message.package_id in defaultPackageIdList:
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(event.message.package_id,event.message.sticker_id))
    else:
        msg = [TextSendMessage(text="I don't have that sticker."),TextSendMessage(text="Can you buy it for me? $",emojis=[{"index":23,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"003"}])]
        line_bot_api.reply_message(event.reply_token,msg)

# line bot location event function
@handler.add(MessageEvent, message=LocationMessage)
def handle_LocationMessage(event):
    # searchKeyword = ['eat','food','dinner','breakfast','hotpot']
    # foodKeywords = ['漢堡','蛋餅','中式早餐','西式早餐','早午餐','拉麵','水餃','便當','火鍋']
    nightMeal = {'有開就好':0,'評價高':1,'評價多':2,'評價高且多':3}
    user_id = event.source.user_id
    global userChoose
    keyword = userChoose[user_id]
    # address = event.message.address
    # debug
    # print(address)
    latitude = event.message.latitude
    longitude = event.message.longitude

    rating_sort = False
    rating_total_sort = False
    rndChoose = True

    if '隨機' in keyword:
        keyword = 'food' if keyword.replace('隨機','') == '' else keyword.replace('隨機','')
    
    if keyword in nightMeal.keys():
        rndChoose = True if nightMeal[keyword] == 0 else False
        rating_sort = nightMeal[keyword] == 1 or nightMeal[keyword] == 3
        rating_total_sort = nightMeal[keyword] == 2 or nightMeal[keyword] == 3
        keyword = 'food' 
    
    res = search_Food(latlng=[latitude,longitude],keyword=keyword,open_now=True,search=True,rating_sort=rating_sort,rating_total_sort=rating_total_sort)

    if rndChoose:
        res = random.sample(res,1)

    global users_choose_restaurant
    msg = []

    msg.append(TextSendMessage(text='FoodSnolax小助手：\n尋找的結果如下$',emojis=[{"index":22,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"021"}]))

    title = f"{res[0]['name']} \n評分：{res[0]['rating']}\n總評論數：{res[0]['user_ratings_total']}"
    msg.append(LocationSendMessage(title,res[0]['vicinity'],res[0]['geometry']['location']['lat'],res[0]['geometry']['location']['lng']))
    msg.append(TextSendMessage(
        text='前往餐廳用餐後完畢後\n可以輸入評分或是評價\n對餐廳進行評分呦～\n您的評分可以提供我們做數據分析\n挑選符合您喜好的餐廳類型$',
        emojis=[{"index":60,"productId":"5ac1bfd5040ab15980c9b435","emojiId":"009"}],
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action = MessageAction(label="評分", text="評分")
                ),
            ])
        ))
    line_bot_api.reply_message(event.reply_token,msg)
    users_choose_restaurant[user_id] = res[0]
    updateLastRecord(user_id,res[0])
    
