from wallApp.config.mysqlDB import connect
from flask import flash
from pprint import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

myDB = 'flaskWall'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

    @staticmethod
    def validateUser(request):
        allowedSymbols = ['$', '@', '#', '%', '!', '&', '*']
        valid = True
        if len(request['firstName']) < 1:
            flash("**First Name Required**", "userError")
            valid = False
        if len(request['firstName']) >= 1 and len(request['firstName']) < 2:
            flash("**First Name Must Be 2 Characters Or More**", "userError")
            valid = False
        if len(request['lastName']) < 1:
            flash("**Last Name Required**", "userError")
            valid = False
        if len(request['lastName']) >= 1 and len(request['lastName']) < 2:
            flash("**Last Name Must Be 2 Characters Or More**", "userError")
            valid = False
        if not EMAIL_REGEX.match(request['email']):
            flash("**Invalid Email Address**", "userError")
            valid = False
        if len(request['email']) < 1:
            flash("**Email Required**", "userError")
            valid = False
        return valid

    @staticmethod
    def validatePassword(request):
        allowedSymbols = ['$', '@', '#', '%', '!', '&', '*']
        valid = True
        if len(request['password']) < 1:
            flash("**Password Required**", "passError")
            valid = False
        if len(request['password']) >= 1 and len(request['password']) < 8 or len(request['password']) > 20:
            flash("**Password Must Be 8-20 Characters**", "passError")
            valid = False
        if not any(char.isdigit() for char in request['password']):
            flash('**Password Requires Minimum Of One Number**', "passError")
            valid = False
        if not any(char.isupper() for char in request['password']):
            flash('**Password Requires Minimum Of One Uppercase Letter**', "passError")
            valid = False
        if not any(char.islower() for char in request['password']):
            flash('**Password Requires Minimum Of One Lowercase Letter**', "passError")
            valid = False
        if not any(char in allowedSymbols for char in request['password']):
            flash('**Password Requires Minimum Of One Symbol $@#%!&**', "passError")
            valid = False
        if request['password'] != request['passConf']:
            flash("**Passwords Do Not Match**", "passError")
            valid = False
        if request['password'] != request['passConf']:
            flash("**Passwords Do Not Match**", "passError")
            valid = False
        return valid

    @classmethod
    def uniqueEmail(cls, data):
        valid = True
        results = User.getByEmail(data)
        if results:
            flash("**Email Already Registered**", "userError")
            valid = False
        return valid

    @classmethod
    def getByEmail(cls, data):
        query = '''
        SELECT * 
        FROM users 
        WHERE email = %(e)s;''' 
        results = connect(myDB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getAll(cls):
        query = '''
        SELECT * 
        FROM users 
        ORDER BY firstName 
        ASC;'''
        return connect(myDB).query_db(query)

    @classmethod
    def getAllButOne(cls, data):
        query = '''
            SELECT * 
            FROM users 
            WHERE id != %(i)s 
            ORDER BY firstName 
            ASC;'''
        results = connect(myDB).query_db(query, data)
        output = []
        for row in results:
            output.append(cls(row))
        return output

    @classmethod
    def save(cls, data):
        query = '''
        Insert INTO users 
        (firstName, lastName, email, password, createdAt) 
        VALUES(%(fn)s, %(ln)s, %(e)s, %(p)s, NOW());'''
        return connect(myDB).query_db(query, data)

    @classmethod
    def findById(cls, data):
        print(f"data variable: {data}")
        query = '''
        SELECT * 
        FROM users 
        WHERE id = %(i)s;'''
        thisUser = connect(myDB).query_db(query, data)
        print(f"debugging: {thisUser}")
        return cls(thisUser[0])

    @classmethod
    def deleteById(cls, data):
        query = '''
        DELETE FROM users 
        WHERE id = %(i)s;'''
        connect(myDB).query_db(query, data)

    @classmethod
    def follow(cls, data):
        query = '''
        Insert INTO followers (followedId, followerId, createdAt) 
        VALUES(%(i)s, %(z)s, NOW());'''
        connect(myDB).query_db(query, data)

    @classmethod
    def unfollow(cls, data):
        query = '''
        DELETE FROM followers 
        WHERE followerId = %(z)s;'''
        connect(myDB).query_db(query, data)

    @classmethod
    def getFollowers(cls, data):
        query = '''
        SELECT f.followerId 
        FROM followers f 
        WHERE followedId = %(i)s 
        ORDER BY createdAt 
        ASC'''
        output = connect(myDB).query_db(query, data)
        followerIds = []
        for row in output:
            followerIds.append(row['followerId'])
        return followerIds

    @classmethod
    def updateUser(cls, data):
        query = '''
        UPDATE users 
        SET firstName = %(fn)s, lastName = %(ln)s, email = %(e)s, updatedAt = NOW() 
        WHERE id = %(i)s;'''
        connect(myDB).query_db(query, data)
