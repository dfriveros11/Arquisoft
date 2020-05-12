from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
import json
#prubea pull request

app = Flask(__name__)
api = Api(app)

mongodatabase = MongoClient('localhost', 27017)
db = mongodatabase['arquisoftdb']
dbPropetarios = db.propetarios
dbPermisos = db.permisos
dbHorarios = db.horarios
dbCerraduras = db.cerraduras


class Cerradura(Resource):
    """Return the pathname of the KOS root directory."""
    @app.route('/$ROUTE_NAME$', methods=['GET', 'POST'])
    def post(self):
        """Return the pathname of the KOS root directory."""
        json_data = request.get_json(force=True)
        idC = json_data['idC']
        estadoActual = json_data['EstadoActual']
        healthCheck = json_data['HealthCheck']
        horarios = json_data['Horarios']
        propetarios = json_data['Propetarios']
        guardar ={
            'idC': idC,
            'EstadoActual': estadoActual,
            'HealthCheck': healthCheck,
            'Horarios': horarios,
            'Propetarios': propetarios
        }
        dbCerraduras.insert_one(guardar).inserted_id
        return jsonify(idH = idC, EstadoActual = estadoActual, HealthCheck = healthCheck, Horarios = horarios, Propetarios = propetarios)
    def get(self):
        x = {}
        cursor = dbCerraduras.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idC = document['idC'].replace('\\','')
            estadoActual = document['EstadoActual'].replace('\\','')
            healthCheck = document['HealthCheck'].replace('\\','')
            horarios = document['Horarios']
            propetarios = document['Propetarios']
            arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
            x['Cerradura#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idC:':v[0], 'EstadoActual:':v[1], 'HealthCheck:':v[2], 'Horarios:':v[3], 'Propetarios:':v[4]}} for k,v in x.items()])
        return thejson
class CerraduraID(Resource):
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find({"idC": (idC)})
        for document in cursor:
            idH = document['idC'].replace('\\','')
            estadoActual = document['EstadoActual'].replace('\\','')
            healthCheck = document['HealthCheck'].replace('\\','')
            horarios = document['Horarios']
            propetarios = document['Propetarios']
            arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idC:':arreglo[0], 'EstadoActual:':arreglo[1], 'HealthCheck:':arreglo[2], 'Horarios:':arreglo[3], 'Propetarios:':arreglo[4]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC})
            return thejson
        return thejson
    def put(self, idC):
        json_data = request.get_json(force = True)
        estadoActual = json_data['EstadoActual']
        healthCheck = json_data['HealthCheck']
        result = dbCerraduras.update_one(
            {'idC' : idC},
            {
                "$set":{
                    'EstadoActual': estadoActual,
                    'HealthCheck': healthCheck
                }
            },
            upsert=False
        )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe la cerradura que se va actualizar con el user_id ' + idC})
            return thejson
        else:
            return jsonify(idC = idC, EstadoActual = estadoActual, HealthCheck = healthCheck)
    def delete(self, idC):
        arreglo = []
        cursor = dbCerraduras.find({"idC": (idC)})
        try:
            for document in cursor:
                idC = document['idC'].replace('\\','')
                estadoActual = document['EstadoActual'].replace('\\','')
                healthCheck = document['HealthCheck'].replace('\\','')
                horarios = document['Horarios']
                propetarios = document['Propetarios']
                arreglo=[idC, estadoActual, healthCheck, horarios, propetarios]
            thejson = json.dumps([{'idC:':arreglo[0], 'EstadoActual:':arreglo[1], 'HealthCheck:':arreglo[2], 'Horarios:':arreglo[3], 'Propetarios:':arreglo[4]}])
            dbCerraduras.remove({"idC": idC})
            result = dbPermisos.update(
                {},
                {
                    "$pull":{'Cerraduras':{
                        "idC"+str(idC):idC
                    }
                    }
                }
            )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe la cerradura que se va eliminar con el user_id ' + idC})
            return thejson
class CerraduraIDHorarios(Resource):
    def post(self, idC):
        json_data = request.get_json(force = True)
        idH = json_data['user_id']
        cursor = dbHorarios.find({"idH": idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el user_id ' + idH})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH):idH}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe el Horario con el user_id ' + idH + ' en la cerradura ' +idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Horarios':{
                                "idH"+str(idH):idH
                            }
                            }
                        }
                    )
                    return jsonify(idH = idH)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find(
            {"idC": (idC)},
        )
        for document in cursor:
            idC = document['idC'].replace('\\','')
            horarios = document['Horarios']
            arreglo=[idC, horarios]
        thejson = json.dumps([{'idC:':arreglo[0], 'Horarios:':arreglo[1]}])
        return thejson
class CerraduraIDHorariosID(Resource):
    def get(self, idC, idH):
        arreglo = []
        cursor = dbCerraduras.find(
            {"idC": (idC), "Horarios.idH" + str(idH):(idH)},
            {"idC":1, "Horarios":1}
        )
        try:
            for document in cursor:
                Horarios = document['Horarios']
                for horario in Horarios:
                    idH = horario["idH" + str(idH)]
                    arreglo=[idC, idH]
            thejson = json.dumps([{'idC':arreglo[0], 'idH':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el user_id ' + idH + ' en la cerradura con el user_id ' + idC})
            return thejson
    def put(self, idC, idH):
        json_data = request.get_json(force = True)
        idN = json_data['user_id']
        cursor = dbHorarios.find({"idH":idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Horario con el user_id ' + idH})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH): idH}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe el Horario con el user_id ' + idH + ' en la cerradura con user_id '+ idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            '$pull':{
                                'Horarios': {'idH'+str(idH):idH}
                            }
                        }
                    )
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Horarios':{
                                "idH"+str(idN):idN
                            }
                            }
                        }
                    )
                    thejson = json.dumps([{'idC':idC, 'idH':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
    def delete(self, idC, idH):
        cursor = dbCerraduras.find({"idC":idC, "Horarios.idH"+str(idH):idH}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC + ' y el horario a borrar con el user_id ' + idH})
            return thejson
        else:
            try:
                result = dbCerraduras.update(
                    {'idC' : idC},
                    {
                        "$pull":{'Horarios':{
                            "idH"+str(idH):idH
                        }
                        }
                    }
                )
                thejson = json.dumps([{'idC':idC, 'idH':idH}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson
class CerraduraIDPropetarios(Resource):
    def post(self, idC):
        json_data = request.get_json(force = True)
        idP = json_data['user_id']
        cursor = dbPropetarios.find({"idP": idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetaario con el user_id ' + idP})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP):idP}).count()
            if cursor > 0:
                thejson = json.dumps({'Respuesta': 'Ya existe el Propetario con el user_id ' + idP + ' en la cerradura ' +idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Propetarios':{
                                "idP"+str(idP):idP
                            }
                            }
                        }
                    )
                    return jsonify(idP = idP)
                except:
                    thejson = json.dumps({'ERROR': "ERROR"})
                    return thejson
    def get(self, idC):
        arreglo = []
        cursor = dbCerraduras.find(
            {"idC": (idC)},
        )
        for document in cursor:
            propetarios = document['Propetarios']
            arreglo=[idC, propetarios]
        thejson = json.dumps([{'idC:':arreglo[0], 'Propetarios:':arreglo[1]}])
        return thejson
class CerraduraIDPropetariosID(Resource):
    def get(self, idC, idP):
        arreglo = []
        cursor = dbCerraduras.find(
            {"idC": (idC), "Propetarios.idP" + str(idP):(idP)},
            {"idC":1, "Propetarios":1}
        )
        try:
            for document in cursor:
                propetarios = document['Propetarios']
                for propetario in propetarios:
                    idP = propetario["idP" + str(idP)]
                    arreglo=[idC, idP]
            thejson = json.dumps([{'idC':arreglo[0], 'idP':arreglo[1]}])
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el user_id ' + idP + ' en la cerradura con el user_id ' + idC})
            return thejson
    def put(self, idC, idP):
        json_data = request.get_json(force = True)
        idN = json_data['user_id']
        cursor = dbPropetarios.find({"idP":idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el user_id ' + idP})
            return thejson
        else:
            cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP): idP}).count()
            if cursor == 0:
                thejson = json.dumps({'Respuesta': 'No existe el Propetario con el user_id ' + idP + ' en la cerradura con user_id '+ idC})
                return thejson
            else:
                try:
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            '$pull':{
                                'Propetarios': {'idP'+str(idP):idP}
                            }
                        }
                    )
                    result = dbCerraduras.update(
                        {'idC' : idC},
                        {
                            "$push":{'Propetarios':{
                                "idP"+str(idN):idN
                            }
                            }
                        }
                    )
                    thejson = json.dumps([{'idC':idC, 'idP':idN}])
                    return thejson
                except:
                    thejson = json.dumps({'ERROR': 'ERROR'})
                    return thejson
    def delete(self, idC, idP):
        cursor = dbCerraduras.find({"idC":idC, "Propetarios.idP"+str(idP):idP}).count()
        if cursor == 0:
            thejson = json.dumps({'Respuesta': 'No existe la Cerradura con el user_id ' + idC + ' y el Propetario a borrar con el user_id ' + idP})
            return thejson
        else:
            try:
                result = dbCerraduras.update(
                    {'idC' : idC},
                    {
                        "$pull":{'Propetarios':{
                            "idP"+str(idP):idP
                        }
                        }
                    }
                )
                thejson = json.dumps([{'idC':idC, 'idP':idP}])
                return thejson
            except:
                thejson = json.dumps({'ERROR': 'ERROR'})
                return thejson


api.add_resource(Cerradura, '/cerraduras')
api.add_resource(CerraduraID, '/cerraduras/<idC>')
api.add_resource(CerraduraIDHorarios, '/cerraduras/<idC>/horarios')
api.add_resource(CerraduraIDHorariosID, '/cerraduras/<idC>/horarios/<idH>')
api.add_resource(CerraduraIDPropetarios, '/cerraduras/<idC>/propetarios')
api.add_resource(CerraduraIDPropetariosID, '/cerraduras/<idC>/propetarios/<idP>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)
