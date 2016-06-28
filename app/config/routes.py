from system.core.router import routes

routes['default_controller'] = 'Friends'
routes['POST']['/login']="Friends#login"
routes['POST']['/register']="Friends#register"
routes['GET']['/friends']="Friends#friends"
routes['POST']['/add']="Friends#add"
routes['POST']['/remove_friend']="Friends#remove_friend"
routes['GET']['/users/<id>']="Friends#users"
routes['GET']['/logout']='Friends#logout'
