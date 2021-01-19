from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from random_username.generate import generate_username
app = Flask(__name__)
CORS(app) # <--- add this line

@app.route('/')
def hello_world():
	return 'Hello, world!'

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      } 
   ]
}

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd['id'] = generate_username(1)[0]
      users['users_list'].append(userToAdd)
      resp = jsonify(success=True)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return userToAdd, 201

@app.route('/users/<id>', methods=['DELETE', 'GET'])
def get_user(id):
   if id :
      if request.method == 'DELETE':
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               return user, 204
         return jsonify(message = "No user found with that index"), 404
      elif request.method == 'GET':
         for user in users['users_list']:
            if user['id'] == id:
               return user
         return ({})
   return users

@app.route('/users/<name>/<job>')
def get_exact_user(name, job):
   if name and job:
      for user in users['users_list']:
        if user['name'] == name and user['job'] == job:
           return user
      return ({})
   return users
