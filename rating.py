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
   delivery_link = db.Column(db.Text)

   def __init__(self, rest_name, keyword, location, rating, users_rating_total, users,delivery_link):
        self.rest_name = rest_name
        self.keyword = keyword
        self.location = location
        self.rating = rating
        self.users_rating_total = users_rating_total
        self.users = users
        self.delivery_link = delivery_link

def checkUserExist(uid,name):
    """
    :Check if user exist in database by uid.
    :If user not exist then add user to database.
    :rtype: if add new user return all users data list else empty list.
    """
    user = users.query.filter_by(uid = uid).first()
    if user is None:
        if addUser(uid, name, "","","",""):
            return getAllUsers()
        return None
    else:
        return []

def addUser(uid, name, lastRecord, fav_type, fav_rest, dislike_rest):
    # 限制測試人員8人內
    if len(getAllUsers()) <= 11:
        user = users(uid, name, lastRecord, fav_type, fav_rest, dislike_rest)
        db.session.add(user)
        db.session.commit()
        return True
    return False

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
        tmpdata = user.last_record
        if tmpdata is None:
            return None
        else:
            return eval(user.last_record)
    else:
        return None

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
                ratingData.users = str(rating_users)
                flag = True
            else:
                rating_sum += int(rating_users[user_uid])
        if not flag:
            ratingData.users_rating_total = ratingData.users_rating_total + 1
            rating_users[uid] = user_give_rating
            rating_sum += int(user_give_rating)
        ratingData.rating = round(rating_sum / len(rating_users.keys()),2)
        if keyword not in ratingData.keyword:
            ratingData.keyword += "," + keyword
        db.session.commit()
    else:
        ratingData = rating(rest_name, keyword, location, user_give_rating, 1, str({uid:user_give_rating}),'')
        db.session.add(ratingData)
        db.session.commit()

    if user_give_rating == 5:
        addFavRest(uid, rest_name)
        addFavType(uid, keyword)
    elif user_give_rating == 1:
        addDislikeRest(uid, rest_name)

def addFavRest(uid, rest_name):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        user.fav_rest = rest_name
        db.session.commit()

def addFavType(uid, fav_type):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        user.fav_type = fav_type
        db.session.commit()

def addDislikeRest(uid, dislike_rest):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        user.dislike_rest = dislike_rest
        db.session.commit()

def getFavRest(uid):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        return user.fav_rest
    else:
        return None

def getFavType(uid):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        return user.fav_type
    else:
        return None

def getDislikeRest(uid):
    user = users.query.filter_by(uid = uid).first()
    if user is not None:
        return user.dislike_rest
    else:
        return None

def getAllHobby(usersObj):
    data = dict()
    for user in usersObj:
        data[user.uid] = {"fav_rest":getFavRest(user.uid),"fav_type":getFavType(user.uid),"dislike_rest":getDislikeRest(user.uid)}
    return data

def getRatingByName(rest_name):
    ratingData = rating.query.filter_by(rest_name = rest_name).first()
    if ratingData is not None:
        return ratingData
    else:
        return None

def getAllLastRecord(dataType, usersObj):
    lastRecord = dict()
    if dataType == 0:
        for user in usersObj:
            lastRecord[user.uid] = getLastRecord(user.uid)
        return lastRecord
    if dataType == 1:
        for user in usersObj:
            tmpdata = getLastRecord(user.uid)
            if tmpdata is not None:
                lastRecord[user.uid] = getLastRecord(user.uid)['name']
        return lastRecord
    return dict()

def getRestRating(rest_name):
    data = rating.query.filter_by(rest_name = rest_name).first()
    if data is not None:
        ratingData = eval(data.users)
        sortedData = sorted(ratingData.items(), key=lambda x: x[1])
        if len(sortedData) >= 2:
            return hideUid(sortedData[0][0]),sortedData[0][1],hideUid(sortedData[len(sortedData)-1][0]),sortedData[len(sortedData)-1][1],data.rating
        else:
            return None,None,None,None,None
    else:
        return None,None,None,None,None

def hideUid(uid):
    return uid[0:2] + "*"*5

def getDeliveryLink(rest_name):
    data = rating.query.filter_by(rest_name = rest_name).first()
    if data is not None and data.delivery_link != '':
        return data.delivery_link
    else:
        return None

def addDeliveryLink(rest_name, delivery_link):
    data = rating.query.filter_by(rest_name = rest_name).first()
    if data is not None:
        data.delivery_link = delivery_link
        db.session.commit()

if __name__ == '__main__':
    pass
    '''
    data = getAllUsers()
    print(data)
    print(len(data))
    for i in data:
        print(i.uid)
    '''
    getRestRating("McDonald's")
