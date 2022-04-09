from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://name:pw@address/database'
db = SQLAlchemy(app)

line_bot_api = LineBotApi('token')
handler = WebhookHandler('secret')

if __name__ == "__main__":
    from handle import *
    app.run(debug=True,port=5002)
