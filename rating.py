from app import db

class users(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, nullable = False ,primary_key = True)
   uid = db.Column(db.Text, nullable = False)
   name = db.Column(db.Text, nullable = False)
   last_record = db.Column(db.Text)
   fav_type = db.Column(db.Text)
   fav_rest = db.Column(db.Text)
   dislike_rest = db.Column(db.Text)

   def __init__(self, uid, name, last_record,fav_type,fav_rest,dislike_rest):
        self.uid = uid
        self.name = name
        self.last_record = last_record
        self.fav_type = fav_type
        self.fav_rest = fav_rest
        self.dislike_rest = dislike_rest

class rating(db.Model):
   __tablename__ = 'rating'
   id = db.Column(db.Integer, nullable = False ,primary_key = True)
   rest_name = db.Column(db.Text, nullable = False)
   keyword = db.Column(db.Text, nullable = False)
   location = db.Column(db.Text, nullable = False)
   rating = db.Column(db.Float)
   users_rating_total = db.Column(db.Integer)
   users = db.Column(db.Text)

   def __init__(self, rest_name, keyword, location, rating, users_rating_total, users):
        self.rest_name = rest_name
        self.keyword = keyword
        self.location = location
        self.rating = rating
        self.users_rating_total = users_rating_total
        self.users = users

def checkUserExist(uid,name):
    """
    :Check if user exist in database by uid.
    :If user not exist then add user to database.
    :rtype: if add new user return all users data list else empty list.
    """
    user = users.query.filter_by(uid = uid).first()
    if user is None:
        addUser(uid, name, "")
        return getAllUsers()
    else:
        return []

def addUser(uid, name, lastOrder):
    user = users(uid, name, lastOrder)
    db.session.add(user)
    db.session.commit()

def getAllUsers():
    return users.query.all()

def updateLastRecord(uid, lastRecord):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        user.last_record = str(lastRecord)
        db.session.commit()

def getLastRecord(uid):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        return eval(user.last_record)
    else:
        return ""

def addRating(uid,rest_name, keyword, location, user_give_rating):
    """
    :param uid: The user id.
    :type uid: string

    :param rest_name: The restaurant name.
    :type rest_name: string

    :param keyword: The restaurant search keyword.
    :type keyword: string

    :param location: The restaurant location.
    :type location: dict, list

    :param rating: The restaurant rating.
    :type rating: float
    """
    ratingData = rating.query.filter_by(rest_name = rest_name).first()
    if ratingData is not None:
        rating_users = eval(ratingData.users)
        rating_sum = 0
        flag = False
        for user_uid in rating_users.keys():
            if user_uid == uid:
                rating_tmp = round((int(rating_users[user_uid]) + user_give_rating)/2,2)
                rating_users[user_uid] = rating_tmp
                rating_sum += int(rating_tmp)
                flag = True
            else:
                rating_sum += int(rating_users[user_uid])
        if not flag:
            rating.users_rating_total = ratingData.users_rating_total + 1
            rating_users[uid] = user_give_rating
            rating_sum += int(user_give_rating)
        ratingData.rating = round(rating_sum / len(rating_users.keys()),2)
        db.session.commit()
    else:
        ratingData = rating(rest_name, keyword, location, user_give_rating, 1, str({uid:user_give_rating}))
        db.session.add(ratingData)
        db.session.commit()

def getRatingByName(rest_name):
    ratingData = rating.query.filter_by(rest_name = rest_name).first()
    if ratingData is not None:
        return ratingData
    else:
        return None

if __name__ == '__main__':
    pass
    ''''
    data = getAllUsers()
    for i in data:
        print(i.uid)
    '''
