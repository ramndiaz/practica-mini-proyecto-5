from flask import Flask, jsonify, request, session, redirect, Response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from bson import json_util
from __main__ import app
from app import mongo
import uuid

@cross_origin
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'id': id})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'id': id})
    response = jsonify({'messsage': ' user ' + id + ' was delete'})
    return response

@cross_origin
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    if name  and email and username and password :
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'id': id}, {'$set':{
            'name': name,
            'email': email,
            'username': username,
            'password': hashed_password,
        }})
        response = jsonify({'messsage': ' user ' + id + ' was updated'})
        return response
    else:
        return not_found()

@cross_origin
@app.route('/users', methods=['POST'])
def create_user():
    id = uuid.uuid4().hex
    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    if name  and email and username and password :

        if len(password) < 7:
            return jsonify({ "error":"Password must be at least 7 characters." }), 400

        hashed_password = generate_password_hash(password)

        if mongo.db.users.find_one({ "email": email }):
            return jsonify({ "error":"Email address already in use" }), 400

        if mongo.db.users.find_one({ "username": username }):
            return jsonify({ "error":"username already in use" }), 400

        mongo.db.users.insert_one({
            'id': id,
            'name' : name,
            'email' : email,
            'username' : username,
            'password' : hashed_password
            })
        """
        response = {
            'id': id,
            'name': name,
            'username': username,
            'email': email,
            'password': hashed_password
        }
        """
        #return response
        return redirect(url_for('home'))
    else:
        return not_found()