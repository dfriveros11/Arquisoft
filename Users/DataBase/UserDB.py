# coding=utf-8
import datetime
import mongoengine


class UserDB(mongoengine.Document):
    """User DB"""
    user_id = mongoengine.IntField(required=True, unique=True)
    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    roles = mongoengine.ListField(mongoengine.StringField(required=False, unique=True))
    created = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
            'db_alias': 'core',
            'collection': 'users',
            'indexes': [
                'created',
                'name',
                'roles',
            ],
            'ordering': ['user_id']
    }