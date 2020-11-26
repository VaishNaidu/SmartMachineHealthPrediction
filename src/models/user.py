import uuid
from flask import session
from src.common.database import Database
import random

class User(object):
    def __init__(self,name,password,email,mobileNo,DOB,_id =None):
        self.name = name
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.email = email
        self.mobile = mobileNo
        self.date = DOB
        #self.symptom =symptom

    @classmethod
    def get_by_name(cls,name):
        data = Database.find_one("users",{"name":name})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls,_id):
        data =Database.find_one("users",{"_id": _id})
        if data is not None:
            return cls(**data)


    @staticmethod
    def login_valid(name,password):
        #User.login_valid("karim","1234")
        #check whether a user's email matchs the password they sent us
        user = User.get_by_name(name)
        if user is not None:
            #check the password
            return user.password == password
        return False


    @classmethod
    def register(cls,name,password,email,mobileNo,DOB):
        user = cls.get_by_name(name)
        if user is None:
            #user doesnt exist ,so we can create it
            new_user = cls(name,password,email,mobileNo,DOB)
            new_user.save_to_mongo()
            session['name'] = name
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(name):
        #login_valid has already called
        session['name'] =name





    @staticmethod
    def logout():
        session['name'] = None

    def save_to_mongo(self):
        Database.insert("users",self.json())

    def json(self):
        return{
            "name":self.name,
            "_id":self._id,
            "password":self.password,
            "email":self.email,
            "mobileNo":self.mobile,
            "DOB":self.date

        }
