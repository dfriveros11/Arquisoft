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

class Permisos(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        idV = json_data['idV']
        dirrecion = json_data['Dirrecion']
        cerraduras = json_data['Cerraduras']
        guardar ={
            'idV': idV,
            'Dirrecion': dirrecion,
            'Cerraduras': cerraduras
        }
        dbPermisos.insert_one(guardar).inserted_id
        return jsonify(idV = idV, Dirrecion = dirrecion, Cerraduras = cerraduras)
    def get(self):
        x = {}
        cursor = dbPermisos.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idV = document['idV'].replace('\\','')
            dirrecion = document['Dirrecion'].replace('\\','')
            cerraduras = document['Cerraduras']
            arreglo=[idV, dirrecion, cerraduras]
            x['Permiso#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idV:':v[0], 'dirrecion:':v[1], 'cerraduras:':v[2]}} for k,v in x.items()])
        return thejson
class PermisosID(Resource):
    def get(self, idV):
        arreglo = []
        cursor = dbPermisos.find({"idV": (idV)})
        for document in cursor:
            idV = document['idV'].replace('\\','')
            dirrecion = document['Dirrecion'].replace('\\','')
            cerraduras = document['Cerraduras']
            arreglo=[idV, dirrecion, cerraduras]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idV:':arreglo[0], 'Dirrecion:':arreglo[1], 'Cerraduras:':arreglo[2]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Permiso con el user_id ' + idV})
            return thejson
        return thejson
    def put(self, idV):
        json_data = request.get_json(force = True)
        dirrecion = json_data['Dirrecion']
        result = dbPermisos.update_one(
            {'idV' : idV},
            {
                "$set":{
                    'Dirrecion': dirrecion
                }
            },
            upsert=False
        )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el permiso que se va actualizar con el user_id ' + idV})
            return thejson
        else:
            return jsonify(idV = idV, Dirrecion = dirrecion)
    def delete(self, idV):
        arreglo = []
        cursor = dbPermisos.find({"idV": (idV)})
        try:
            for document in cursor:
                idV = document['idV'].replace('\\','')
                dirrecion = document['Dirrecion'].replace('\\','')
                cerraduras = document['Cerraduras']
                arreglo=[idV, dirrecion, cerraduras]
            thejson = json.dumps([{'idV:':arreglo[0], 'dirrecion:':arreglo[1], 'cerraduras:':arreglo[2]}])
            dbPermisos.remove({"idV": idV})
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el permiso que se va eliminar con el user_id ' + idV})
            return thejson
class PermisosIDCerradura(Resource):
    def post(self, idV):
        json_data = request.get_json(force = True)
        idC = json_data['user_id']
        cursor = dbCerraduras.find({"idC": idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC})
            return thejson
        else:
            cursor = dbCerraduras.find({"idV":idV, "Cerraduras.idC"+str(idC):idC}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe la Cerradura con el user_id ' + idC + ' en el permiso' +idV})
                return thejson
            else:
                try:
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            "$push":{'Cerraduras':{
                                "idC"+str(idC):idC
                            }
                            }
                        }
                    )
                    return jsonify(idC = idC)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    def get(self, idV):
        arreglo = []
        cursor = dbPermisos.find(
            {"idV": (idV)},
        )
        for document in cursor:
            cerraduras = document['Cerraduras']
            arreglo=[idV, cerraduras]
        thejson = json.dumps([{'idV:':arreglo[0], 'Cerraduras:':arreglo[1]}])
        return thejson
class PermisosIDCerraduraID(Resource):
    def get(self, idV, idC):
        arreglo = []
        cursor = dbPermisos.find(
            {"idV": (idV), "Cerraduras.idC" + str(idC):(idC)},
            {"idV":1, "Cerraduras":1}
        )
        try:
            for document in cursor:
                cerraduras = document['Cerraduras']
                for cerradura in cerraduras:
                    idC = cerradura["idC" + str(idC)]
                    arreglo=[idV, idC]
            thejson = json.dumps([{'idV':arreglo[0], 'idC':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Cerradura con el user_id ' + idC + ' en la Permiso con el user_id ' + idV})
            return thejson
    def put(self, idV, idC):
        json_data = request.get_json(force = True)
        idN = json_data['user_id']
        cursor = dbCerraduras.find({"idC":idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Cerraduras con el user_id ' + idC})
            return thejson
        else:
            cursor = dbPermisos.find({"idV":idV, "Cerraduras.idC"+str(idC): idC}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC + ' en el Permiso con user_id '+ idV})
                return thejson
            else:
                try:
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            '$pull':{
                                'Cerraduras': {'idC'+str(idC):idC}
                            }
                        }
                    )
                    result = dbPermisos.update(
                        {'idV' : idV},
                        {
                            "$push":{'Cerraduras':{
                                "idC"+str(idN):idN
                            }
                            }
                        }
                    )
                    thejson = json.dumps([{'idV':idV, 'idC':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
    def delete(self, idV, idC):
        cursor = dbPermisos.find({"idV":idV, "Cerraduras.idC"+str(idC):idC}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC + ' en el Permiso a borrar con el user_id ' + idV})
            return thejson
        else:
            try:
                result = dbPermisos.update(
                    {'idV' : idV},
                    {
                        "$pull":{'Cerraduras':{
                            "idC"+str(idC):idC
                        }
                        }
                    }
                )
                thejson = json.dumps([{'idV':idV, 'idC':idC}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson

api.add_resource(Permisos, '/permisos')
api.add_resource(PermisosID, '/permisos/<idV>')
api.add_resource(PermisosIDCerradura, '/permisos/<idV>/cerraduras')
api.add_resource(PermisosIDCerraduraID, '/permisos/<idV>/cerraduras/<idC>')

if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)