# coding=utf-8
from Users.DataBase.UserDB import User
from Users.DataBase.mongo_setup import global_init


def main():
    """Example"""
    global_init('example')
    u = User()
    u.name = 'Diego'
    u.email = 'df.riveros11@gmail.com'
    u.save()


if __name__ == '__main__':
    main()