from app import db

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

if __name__ == '__main__':
    pass