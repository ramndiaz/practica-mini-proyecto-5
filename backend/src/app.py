from flask import Flask, request, jsonify, Response, session, redirect, url_for
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from functools import wraps
from flask_cors import CORS, cross_origin



app = Flask(__name__)

app.secret_key = "key_super_secret"

#cross origin
CORS(app)

#database
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/pomodorodb'
mongo = PyMongo(app)

#decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            #return redirect('/')
            return redirect(url_for('home'))
    return wrap

#routes

@cross_origin
@app.route('/')
def home():
    holder = list()
    currentuser = mongo.db.users
    for i in currentuser.find():
        holder.append({'name': i['name'], 'email': i['email'], 'username': i['username']})
    return jsonify(holder)

@cross_origin
@app.route('/dashboard/')
@login_required
def dashboard():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return redirect(url_for('home'))

@cross_origin
@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({
    'message': 'Resource Not Found: ' + request.url,
    'status': '404'
    })
    message.status_code=404
    return message

from loger import routes
from user import routes
from tracker import routes

if __name__=="__main__":
	app.run(debug=True)
