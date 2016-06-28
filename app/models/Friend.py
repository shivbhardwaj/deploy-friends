from system.core.model import Model
import re

class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()
    
    def get_user(self, id):
        query="SELECT * FROM users WHERE id=:id"
        data={'id':id}
        return self.db.query_db(query, data)

    def get_friendships(self, user_id):
        query="select * from friendships"
        data={'user_id':user_id}
        return self.db.query_db(query, data)

    def remove_friend(self, user_id, friendship_id):
        print user_id
        print friendship_id
        query="DELETE from friendships where users_id=:users_id AND friends_id=:friends_id"
        data={'users_id': user_id, 'friends_id':friendship_id}
        delete_friend=self.db.query_db(query, data)
        print delete_friend
        print "testing remove friend"
        print "testing remove friend"
        print "testing remove friend"
        print "testing remove friend"
        print "testing remove friend"
        return delete_friend

    def user_by_id(self, user_id, id):
        query= 'SELECT users1.id, users1.name, users1.alias, users2.alias AS friend_alias, users2.name AS friend_name, users2.id as friend_id FROM users AS users1 JOIN friendships ON users1.id=friendships.users_id JOIN users AS users2 ON friendships.friends_id=users2.id' 
        data= {
            'users1.id': user_id, 
            'users2.id': id
        }
        users_by_id=self.db.query_db(query, data)
        print users_by_id
        print "testing user by id"
        print "testing user by id"
        print "testing user by id"
        print "testing user by id"
        print "testing user by id"
        print "testing user by id"
        return self.db.query_db(query, data)

    def add_friends(self, user_id, friendship_id):
        query="INSERT into friendships (created_at, updated_at, users_id, friends_id) VALUES (NOW(), NOW(), :users_id, :friends_id)"
        data={
            'users_id': user_id, 
            'friends_id': friendship_id
        }
        return self.db.query_db(query, data)


    def list_all_users(self, user_id):
        query='SELECT * FROM users WHERE id!=:id'
        data={
            'id': user_id
        }
        return self.db.query_db(query, data)

    def login(self, info):
        errors=[]
        query="SELECT * FROM users WHERE email=:email"
        data={
            'email':info['email'], 
            'password': info['password']
        }
        user_login=self.db.query_db(query,data)
        if user_login and self.bcrypt.check_password_hash(user_login[0]['password'], info['password']):
            return {'status': True, "user_login":user_login}
        else:
            errors.append('Invalid user or password!')
            return {'status': False, "errors": errors} 
        #check PW and if validates, return success w/ user data 
        # Go back to Controller

    def register(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors=[]
        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name'])<2:
            errors.append('Name must be at least 2 characters long')
        if not info['alias']:
            errors.append('Alias cannot be blank')
        elif len(info['alias'])<2:
            errors.append('Alias must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password'])<8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pconfirm']:
            errors.append('Password and confirmation must match!')
        # if not info['bday']:
        #     errors.append('You must be older than 16 to join!')
        if errors:
            return {'status': False, "errors": errors}
        else:
            encrypt = self.bcrypt.generate_password_hash(info['password'])
            query = "INSERT INTO users (name, alias, email, password, bday, created_at, updated_at) VALUES (:name, :alias, :email, :password, :bday, NOW(), NOW())"
            data={
                "name":info['name'], 
                "alias":info['alias'], 
                "email":info['email'], 
                "password":encrypt, 
                "bday": info['bday']
                }
            #get_user_query="SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user_id = self.db.query_db(query, data)
            return { "status": True, "user_id": user_id}