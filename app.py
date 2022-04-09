from flask import Flask
from linebot import (
    LineBotApi, WebhookHandler
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:0204@127.0.0.1:5432/myDatabase'
db = SQLAlchemy(app)

line_bot_api = LineBotApi('Y/z2QY9AOAaFeVXtkusbrjUhTwWbdwi6976K23rBgB8XeOjHgLmf65+0zH95biSnN06HinwgXzjYGzEMtnmz1nPIL4u8Oa6hwta6FUlz2hBeP9z/H1vAkelnpmczStlQkg7eT8iR7kY+mw+y6YOWKwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cb13329defbe529d0795b1a631b5b5e2')

if __name__ == "__main__":
    from handle import *
    app.run(debug=True,port=5002)