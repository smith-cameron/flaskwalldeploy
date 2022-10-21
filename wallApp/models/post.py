from wallApp.config.mysqlDB import connect
from flask import flash
from pprint import pprint
myDB = 'flaskWall'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.creatorId = data['creatorId']
        self.recipientId = data['recipientId']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.sender = None
        self.recipient = None

    @staticmethod
    def validatePost(request):
        valid = True
        if len(request['content']) < 1:
            flash("**Post Content Required**", "postError")
            valid = False
        if len(request['content']) > 255:
            flash("**Post Too Long**", "postError")
            valid = False
        return valid

    @classmethod
    def getAll(cls):
        query = '''
        SELECT * 
        FROM posts;
        '''
        allPosts = connect(myDB).query_db(query)
        return allPosts

    @classmethod
    def save(cls, data):
        query = '''
        Insert INTO posts (content, creatorId, recipientId) 
        VALUES(%(c)s, %(ci)s, %(ri)s);
        '''
        # print(query)
        return connect(myDB).query_db(query, data)

    @classmethod
    def findRecievedByUserId(cls, data):
        query = '''
        SELECT m.* , u.firstName 
        FROM posts m 
        JOIN users u 
        ON m.creatorId = u.id 
        WHERE m.recipientId = %(i)s;
        '''
        results = connect(myDB).query_db(query, data)
        pprint(results)

        return results

    @classmethod
    def findSentByUserId(cls, data):
        query = '''
        SELECT * 
        FROM posts m 
        JOIN users u 
        ON m.recipientId = u.id 
        WHERE creatorId = %(i)s;
        '''
        results = connect(myDB).query_db(query, data)
        # print(results)
        return results

    @classmethod
    def findById(cls, data):
        query = '''
        SELECT * 
        FROM posts 
        WHERE id = %(i)s;
        '''
        thisMessage = connect(myDB).query_db(query, data)
        return cls(thisMessage[0])

    @classmethod
    def deleteById(cls, data):
        query = '''
        DELETE 
        FROM posts 
        WHERE id = %(i)s;
        '''
        connect(myDB).query_db(query, data)