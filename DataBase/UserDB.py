# coding=utf-8
import datetime
import mongoengine


class UserDB(mongoengine.Document):
    """User DB"""
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    roles = mongoengine.ListField(mongoengine.StringField(required=False))
    created = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
            'db_alias': 'core',
            'collection': 'users',
            'indexes': [
                'created',
                'name',
                'roles',
            ],
            'ordering': ['name']
    }