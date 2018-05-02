# coding=utf-8
from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource
from mongoengine import ValidationError, NotUniqueError

from Users.DataBase.UserDB import UserDB
from Users.DataBase.mongo_setup import global_init

app = Flask(__name__)
api = Api(app)
global_init('mainDB')

class ResidentialService(Resource):
    """Services"""

api.add_resource(ResidentialService, '/residentials')
if __name__ == '__main__':
    app.run(debug=True, uses_reloader=False)