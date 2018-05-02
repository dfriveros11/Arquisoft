# coding=utf-8
from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource
from mongoengine import ValidationError, NotUniqueError

from Users.DataBase.UserDB import UserDB
from Users.DataBase.mongo_setup import global_init

app = Flask(__name__)
api = Api(app)
global_init('usersDB')


class UserService(Resource):
    """Method for user"""

    def post(self):
        """add a new user"""
        json_data = request.get_json(force=True)
        user = UserDB()
        user.user_id = json_data['id']
        user.name = json_data['name']
        user.email = json_data['email']
        user.roles = json_data['roles']
        try:
            user.save()
            j = jsonify(user_id=user.user_id, name=user.name, email=user.email, roles=user.roles)
            return j
        except NotUniqueError:
            return json.dumps({'Exception': 'Already exist the user with user_id: ' + str(user.user_id)})
        except ValidationError:
            return json.dumps({'Exception': 'The Format for a email is "name"@"email" but the email type was this: ' + user.email})

    def get(self):
        """get all the users"""
        users = UserDB.objects()
        x = {}
        i = 1
        for user in users:
            user_id = user['id']
            name = user['name'].replace('\\', '')
            email = user['email'].replace('\\', '')
            roles = user['roles']
            userA = [user_id, name, email, roles]
            x['User#' + str(i)] = userA
            i += 1
        j = json.JSONEncoder().encode(
            [{k: {'user_id': v[0], 'name:': v[1], 'email:': v[2], 'roles:': v[3]}}
             for k, v in x.items()])
        return j


class UserServiceID(Resource):
    """Method for user with an especific user_id"""
    def get(self, id):
        """get the user with <user_id>"""
        user = UserDB.objects(user_id=id)
        if not user:
            return json.dumps({'Answer': 'There is not an user with the user_id: ' + id})
        else:
            a = []
            for u in user:
                user_id = u['id']
                name = u['name'].replace('\\', '')
                email = u['email'].replace('\\', '')
                roles = u['roles']
                a = [user_id, name, email, roles]
            return jsonify(user_id= a[0], name=a[1], email=a[2], roles=a[3])

    def put(self, id):
        """the user with <user_id> is going to be update"""
        json_data = request.get_json(force=True)
        name = json_data['name']
        email = json_data['email']
        user = UserDB.objects(user_id=id).update(name=name, email=email)
        if user == 1:
            return jsonify(name=name, email=email)
        else:
            return json.dumps({'Answer': 'There is not an user with the user_id: ' + id})

    def delete(self,id):
        """the user with <user_id> is going to be deleted"""
        user = UserDB.objects(user_id=id).delete()
        if user == 1:
            return json.dumps({'Answer': 'The user with the user_id: ' + id + ' has been deleted'})
        else:
            return json.dumps({'Error': 'The user with the user_id: ' + id + ' does not exist'})


class UserRolesService(Resource):
    """the roles services"""
    def post(self, id):
        """add a role in a specific user"""
        json_data = request.get_json(force=True)
        new_rol = json_data['rol']
        print(new_rol)
        rol = UserDB.objects(user_id=id).update(add_to_set__roles=new_rol)
        if rol == 1:
             return json.dumps({'Answer': 'The user with the user_id: ' + id + ' has been update with a new rol'})
        else:
             return json.dumps({'Answer': 'There is not user with the user_id: ' + id})

    def get(self, id):
        """get all roles of a specific user"""
        user = UserDB.objects(user_id=id)
        roles = []
        for u in user:
            roles = u['roles']
        return jsonify(userid=id, roles=roles)


class UserRolesServiceID(Resource):
    """An specific rol operations"""
    def get(self, id, idr):
        """get a rol of a specific user"""
        name = idr
        user = UserDB.objects(user_id=id, roles=name)
        if not user:
            return json.dumps({'Answer': 'The rol ' + idr + ' in the user ' + id + ' does not exist'})
        else:
            return jsonify(userID = id, rol = idr)

    def put(self, id, idr):
        """update a rol of a specific user"""
        json_data = request.get_json(force=True)
        rol_update = json_data['rol']
        user = UserDB.objects(user_id=id, roles=idr).update(set__roles__S=rol_update)
        if user == 1:
            return jsonify(UserID=id, Old_Rol= idr, Update_Rol=rol_update)
        else:
            return json.dumps({'Answer': 'There is not rol ' + idr + ' in the user with the user_id: ' + id})

    def delete(self, id, idr):
        """delete a rol of a specific user"""
        user = UserDB.objects(user_id=id, roles=idr).update(pull__roles=idr)
        if user == 1:
            return jsonify(UserID=id, Delete_Rol=idr)
        else:
            return json.dumps({'Answer': 'There is not rol ' + idr + ' in the user with the user_id: ' + id})


api.add_resource(UserService, '/users')
api.add_resource(UserServiceID, '/users/<user_id>')
api.add_resource(UserRolesService, '/users/<id>/roles')
api.add_resource(UserRolesServiceID, '/users/<id>/roles/<idr>')
if __name__ == '__main__':
    app.run(debug=True, uses_reloader=False)
