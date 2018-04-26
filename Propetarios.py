from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json

app = Flask(__name__)
api = Api(app)

clienteMongo = MongoClient('localhost', 27017)
db = clienteMongo['arquisoftdb']
dbPropetarios = db.propetarios
dbPermisos = db.permisos
dbHorarios = db.horarios
dbCerraduras = db.cerraduras

class Propetario(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        idP = json_data['idP']
        informacion = json_data['informacion']
        guardar ={
            'idP' : idP,
            'Informacion' : informacion
        }
        dbPropetarios.insert_one(guardar).inserted_id
        return jsonify(idP = idP, Informacion = informacion)
    def get(self):
        x = {}
        cursor = dbPropetarios.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
            x['Propetario#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idP':v[0], 'Informacion':v[1]}} for k,v in x.items()])
        return thejson
class PropetarioID(Resource):
    def get(self, idP):
        arreglo = []
        cursor = dbPropetarios.find({"idP": (idP)})
        for document in cursor:
            idP = document['idP'].replace('\\','')
            informacion = document['Informacion'].replace('\\','')
            arreglo=[idP, informacion]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el id ' + idP})
            return thejson
        return thejson
    def put(self, idP):
        json_data = request.get_json(force = True)
        informacion = json_data['informacion']
        result = dbPropetarios.update_one(
            {'idP' : idP},
            {
                "$set":{
                    'Informacion': informacion
                }
            },
            upsert=False
        )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va actualizar con el id ' + idP})
            return thejson
        else:
            return jsonify(idP = idP, Informacion = informacion)
    def delete(self, idP):
        arreglo = []
        cursor = dbPropetarios.find({"idP": (idP)})
        try:
            for document in cursor:
                idP = document['idP'].replace('\\','')
                informacion = document['Informacion'].replace('\\','')
                arreglo=[idP, informacion]
            thejson = json.dumps([{'idP':arreglo[0], 'Informacion': arreglo[1]}])
            dbPropetarios.remove({"idP": idP})
            result = dbCerraduras.update(
                {},
                {
                    "$pull":{'Propetarios':{
                        "idP"+str(idP):idP
                    }
                    }
                }
            )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va eliminar con el id ' + idP})
            return thejson

api.add_resource(Propetario, '/propetarios')
api.add_resource(PropetarioID, '/propetarios/<idP>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)