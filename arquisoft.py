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
            thejson = json.dumps({'Respuesta': 'No existe el Propetario con el user_id ' + idP})
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
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va actualizar con el user_id ' + idP})
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
            thejson = json.dumps({'Respuesta': 'No existe el Propetario que se va eliminar con el user_id ' + idP})
            return thejson
class Horario(Resource):
    def post(self):
        json_data = request.get_json(force = True)
        idH = json_data['idH']
        dia = json_data['dia']
        horaP = json_data['hora1']
        horaS = json_data['hora2']
        timeZone = json_data['timeZone']
        guardar ={
            'idH': idH,
            'Dia': dia,
            'Hora1': horaP,
            'Hora2': horaS,
            'TimeZone': timeZone
        }
        dbHorarios.insert_one(guardar).inserted_id
        return jsonify(idH = idH, Dia = dia, Hora1 = horaP, Hora2 = horaS, TimeZone = timeZone)
    def get(self):
        x = {}
        cursor = dbHorarios.find({})
        i = 1
        for document in cursor:
            arreglo = {}
            idH = document['idH'].replace('\\','')
            dia = document['Dia'].replace('\\','')
            horaP = document['Hora1'].replace('\\','')
            horaS = document['Hora2'].replace('\\','')
            timeZone = document['TimeZone'].replace('\\','')
            arreglo=[idH, dia, horaP, horaS, timeZone]
            x['Dia#' + str(i)] = arreglo
            i+=1
        thejson = json.JSONEncoder().encode([{k :{ 'idH:':v[0], 'Dia:':v[1], 'Hora1:':v[2], 'Hora2:':v[3], 'TimeZone:':v[4]}} for k,v in x.items()])
        return thejson
class HorarioID(Resource):
    def get(self, idD):
        arreglo = []
        cursor = dbHorarios.find({"idH": (idD)})
        for document in cursor:
            idH = document['idH'].replace('\\','')
            dia = document['Dia'].replace('\\','')
            horaP = document['Hora1'].replace('\\','')
            horaS = document['Hora2'].replace('\\','')
            timeZone = document['TimeZone'].replace('\\','')
            arreglo=[idH, dia, horaP, horaS, timeZone]
        if len(arreglo)> 0:
            thejson = json.dumps([{'idH:':arreglo[0], 'Dia:':arreglo[1], 'Hora1:':arreglo[2], 'Hora2:':arreglo[3], 'TimeZone:':arreglo[4]}])
        else:
            thejson = json.dumps({'Respuesta': 'No existe el Dia con el user_id ' + idD})
            return thejson
        return thejson
    def put(self, idD):
        json_data = request.get_json(force = True)
        dia = json_data['dia']
        horaP = json_data['hora1']
        horaS = json_data['hora2']
        timeZone = json_data['timeZone']
        result = dbHorarios.update_one(
            {'idH' : idD},
            {
                "$set":{
                    'Dia': dia,
                    'Hora1': horaP,
                    'Hora2': horaS,
                    'TimeZone': timeZone
                }
            },
            upsert=False
        )
        if result.matched_count == 0:
            thejson = json.dumps({'Respuesta': 'No existe el Dia que se va actualizar con el user_id ' + idD})
            return thejson
        else:
            return jsonify(idD = idD, Dia = dia, Hora1 = horaP, Hora2 = horaS, timeZone = timeZone)
    def delete(self, idD):
        arreglo = []
        cursor = dbHorarios.find({"idH": (idD)})
        try:
            for document in cursor:
                idD = document['idH'].replace('\\','')
                dia = document['Dia'].replace('\\','')
                horaP = document['Hora1'].replace('\\','')
                horaS = document['Hora2'].replace('\\','')
                timeZone = document['TimeZone'].replace('\\','')
                arreglo=[idD, dia, horaP, horaS, timeZone]
            thejson = json.dumps([{'idH:':arreglo[0], 'Dia:':arreglo[1], 'Hora1:':arreglo[2], 'Hora2:':arreglo[3], 'TimeZone:':arreglo[4]}])
            dbHorarios.remove({"idH": idD})
            result = dbCerraduras.update(
                {},
                {
                    "$pull":{'Horarios':{
                        "idH"+str(idD):idD
                    }
                    }
                }
            )
            return thejson
        except:
            thejson = json.dumps({'Respuesta': 'No existe el Horario que se va eliminar con el user_id ' + idD})
            return thejson
class Cerradura(Resource):
    def post(self):
        json_data = request.get_json(force = True)
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
api.add_resource(Propetario, '/propetarios')
api.add_resource(PropetarioID, '/propetarios/<idP>')
api.add_resource(Horario, '/horarios')
api.add_resource(HorarioID, '/horarios/<idD>')
api.add_resource(Cerradura, '/cerraduras')
api.add_resource(CerraduraID, '/cerraduras/<idC>')
api.add_resource(CerraduraIDHorarios, '/cerraduras/<idC>/horarios')
api.add_resource(CerraduraIDHorariosID, '/cerraduras/<idC>/horarios/<idH>')
api.add_resource(CerraduraIDPropetarios, '/cerraduras/<idC>/propetarios')
api.add_resource(CerraduraIDPropetariosID, '/cerraduras/<idC>/propetarios/<idP>')
api.add_resource(Permisos, '/permisos')
api.add_resource(PermisosID, '/permisos/<idV>')
api.add_resource(PermisosIDCerradura, '/permisos/<idV>/cerraduras')
api.add_resource(PermisosIDCerraduraID, '/permisos/<idV>/cerraduras/<idC>')


if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)