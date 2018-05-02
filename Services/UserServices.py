# coding=utf-8
from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource


from DataBase.UserDB import UserDB
from DataBase.mongo_setup import global_init

app = Flask(__name__)
api = Api(app)
global_init('usersDB')


class UserService(Resource):
    """Method for user"""

    def post(self):
        """add a new user"""
        json_data = request.get_json(force=True)
        user = UserDB()
        user.name = json_data['name']
        user.email = json_data['email']
        user.roles = json_data['roles']
        user.save()
        return jsonify(name=user.name, email=user.email, roles=user.roles)

    def get(self):
        """get all the users"""
        users = UserDB.objects()
        x = {}
        i = 1
        for user in users:
            name = user['name'].replace('\\', '')
            email = user['email'].replace('\\', '')
            roles = user['roles']
            userA = [name, email, roles]
            x['User#' + str(i)] = userA
            i += 1
        j = json.JSONEncoder().encode(
            [{k: {'name:': v[0], 'email:': v[1], 'roles:': v[2]}}
             for k, v in x.items()])
        return j

    def get(self, id):
        """get the user with <id>"""
        user = UserDB.objects(id=id)
        if not user:
            return json.dumps({'Answer': 'There is not an user with the id: ' + id})
        else:
            a = []
            for u in user:
                name = u['name'].replace('\\', '')
                email = u['email'].replace('\\', '')
                roles = u['roles']
                a = [name, email, roles]
            return jsonify(name=a[0], email=a[1], roles=a[2])

    def put(self, id):
        """the user with <id> is going to be update"""
        json_data = request.get_json(force=True)
        name = json_data['name']
        email = json_data['email']
        user = UserDB.objects(id=id).update(name=name, email=email)
        if user == 1:
            return jsonify(name=name, email=email)
        else:
            return json.dumps({'Answer': 'There is not an user with the id: ' + id})

    def delete(self,id):
        """the user with <id> is going to be deleted"""
        user = UserDB.objects(id=id).delete()
        if user == 1:
            return json.dumps({'Answer': 'The user with the id: ' + id + ' has been deleted'})
        else:
            return json.dumps({'Answer': 'The user with the id: ' + id + ' has been deleted'})

class UserRolesService(Resource):
    """the roles services"""
    def post(self, id):
        """add a role in a specific user"""
        json_data = request.get_json(force=True)
        new_rol = json_data['rol']
        rol = UserDB.objects(id=id).update(add_to_set__roles=new_rol)
        if rol == 1:
            return json.dumps({'Answer': 'The user with the id: ' + id + ' has been update with a new rol'})
        else:
            return json.dumps({'Answer': 'There is not user with the id: ' + id })

    def get(self, id):
        """get all roles of a specific user"""
        user = UserDB.objects(id=id)
        roles = []
        for u in user:
            roles = u['roles']
        return jsonify(userid=id, roles=roles)

    def get(self, id, idr):
        """get a rol of a specific user"""
        name = idr
        user = UserDB.objects(id=id, roles=name)
        if not user:
            return json.dumps({'Answer': 'The rol ' + idr + ' in the user ' + id + ' does not exist'})
        else:
            return jsonify(userID = id, rol = idr)

    def put(self, id, idr):
        """update a rol of a specific user"""
        json_data = request.get_json(force=True)
        rol_update = json_data['rol']
        user = UserDB.objects(id=id, roles=idr).update(set__roles__S=rol_update)
        if user == 1:
            return jsonify(UserID=id, Old_Rol= idr, Update_Rol=rol_update)
        else:
            return json.dumps({'Answer': 'There is not rol ' + idr + ' in the user with the id: ' + id})

    def delete(self, id, idr):
        """delete a rol of a specific user"""
        user = UserDB.objects(id=id, roles=idr).update(pull__roles=idr)
        if user == 1:
            return jsonify(UserID=id, Delete_Rol=idr)
        else:
            return json.dumps({'Answer': 'There is not rol ' + idr + ' in the user with the id: ' + id})


api.add_resource(UserService, '/users', '/users/<id>')
api.add_resource(UserRolesService, '/users/<id>/roles', '/users/<id>/roles/<idr>')
if __name__ == '__main__':
    app.run(debug=True, uses_reloader=False)
