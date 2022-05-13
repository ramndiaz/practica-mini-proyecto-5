from flask import Flask, jsonify, request, session, redirect, Response, url_for
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
from __main__ import app
from app import mongo
from bson import json_util
from datetime import datetime


@cross_origin
@app.route('/pomodoro', methods=['GET'])
def get_pomodoro():
    pomodoro = mongo.db.pomodoro.find()
    response = json_util.dumps(pomodoro)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/tracker', methods=['GET'])
def get_tracker():
    holder=list()
    dashboard =  mongo.db.users.aggregate( [
   {
     "$lookup":
       {
         "from": "pomodoro",
         "localField": "id",
         "foreignField": "user_id",
         "as": "pomodoro_users"
       }
  }
] )
    response = json_util.dumps(dashboard)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/pomodoro', methods=['POST'])
def create_pomodoro():
    user_id = request.json['id']
    date_time = datetime.now()
    name = request.json['name']
    description = request.json['description']
    total_pomo = request.json['total_pomo']

    if user_id  and date_time and name and description and total_pomo :

        if total_pomo:
            mongo.db.pomodoro.insert_one({
                'user_id': user_id,
                'date_time' : date_time,
                'name' : name,
                'description' : description,
                'total_pomo' : total_pomo
                })
            response = {
                'user_id': user_id,
                'date_time' : date_time,
                'name' : name,
                'description' : description,
                'total_pomo' : total_pomo
            }
            return response
        return jsonify({ "error":"must save at least 1 full pomodoro." }), 400
    else:
        return not_found()