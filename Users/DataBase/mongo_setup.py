# coding=utf-8
import mongoengine


def global_init(db_name: str):
    """Connection to the database"""
    mongoengine.register_connection(alias='core', name=db_name)
