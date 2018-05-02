# coding=utf-8
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import json

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['usuariosDB']
dbPropetarios = db.propetarios

class Propetario(Resource):
    """This is the class propert."""
    @app.route(methods=['POST'])
    def post(self):
        """Return the Objects insert"""
        json_data = request.get_json(force=True)
        idC = json_data['idP']
        estadoActual = json_data['EstadoActual']
        healthCheck = json_data['HealthCheck']
        horarios = json_data['Horarios']
        propetarios = json_data['Propetarios']
        guardar = {
            'idC': idC,
            'EstadoActual': estadoActual,
            'HealthCheck': healthCheck,
            'Horarios': horarios,
            'Propetarios': propetarios
        }
        dbPropetarios.insert_one(guardar).inserted_id
        return jsonify(idH=idC, EstadoActual=estadoActual, HealthCheck=healthCheck, Horarios=horarios,
                       Propetarios=propetarios)


api.add_resource(Propetario, '/propetarios')
# api.add_resource(PropetarioID, '/propetarios/<idP>')
if __name__ == '__main__':
    app.run(debug=True)

