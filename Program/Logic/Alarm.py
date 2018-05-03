# coding=utf-8
from datetime import date


class Alarm:

    def __init__(self, alarm_id, date_created, description, lock):
        self.alarm_id = alarm_id
        self.date_created = date_created
        self.description = description
        self.lock = lock
