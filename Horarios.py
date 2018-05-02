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

api.add_resource(Horario, '/horarios')
api.add_resource(HorarioID, '/horarios/<idD>')
if __name__ == '__main__':
    app.run(debug=True, use_reloader= False)