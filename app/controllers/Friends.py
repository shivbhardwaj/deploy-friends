from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('Friend')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def register(self):
        create_status=self.models['Friend'].register(request.form)
        if create_status['status']:
            session['user_id']=create_status['user_id']
            return redirect('/friends')
        else: 
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/')
    
    def login(self):
        #whatever we set equal is what is returned
        users=self.models['Friend'].login(request.form)
        session['user_id']=users['user_login'][0]['id']
        return redirect('/friends')

    def users(self, id):
        user=self.models['Friend'].get_user(id)
        return self.load_view('user.html', user=user[0])

    def friends(self):
        user=self.models['Friend'].get_user(session['user_id'])
        all_users=self.models['Friend'].list_all_users(session['user_id'])
        users_by_id=self.models['Friend'].user_by_id(session['user_id'], id)
        friendships=self.models['Friend'].get_friendships(session['user_id']) 
        session['friendship_id']=friendships[0]['friends_id']
        friendship_id=session['friendship_id']
        print "session friends_id is", session['friends_id']
        rem_friend=self.models['Friend'].remove_friend(session['user_id'], session['friendship_id'])
        return self.load_view('friends.html', user=user[0], all_users=all_users, users_by_id=users_by_id, friendship_id=friendship_id)

    def add(self):
        self.models['Friend'].add_friends(session['user_id'], session['friends_id'])
        # friends_id=-1
        # friend = {}
        # friends = []
        # for i in add_friends:
        #     if friends_id != i['friends_id']:
        #         friend = {'friends_id': i['friends_id']}
        #         friends_id = i['friends_id']
        #         friends.append(friend)
        return redirect('/friends')

    def logout(self):
        session.pop('user_id')
        session.pop('friends_id')
        return redirect('/')