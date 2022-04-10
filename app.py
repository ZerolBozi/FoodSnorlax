from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from flask_sqlalchemy import SQLAlchemy

# set server and database coning
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://name:pw@address/database'
db = SQLAlchemy(app)

# set line bot config
line_bot_api = LineBotApi('token')
handler = WebhookHandler('secret')

if __name__ == "__main__":
    from handle import *
    '''
    start server
    import handle to set route and callback
    '''
    app.run(host='0.0.0.0',debug=True,port=5002)
