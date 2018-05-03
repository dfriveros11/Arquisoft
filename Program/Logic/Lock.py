# coding=utf-8

class Lock:
    def __init__(self, lock_id, actual_state, health_check):
        self.lock_id = lock_id
        self.actual_state = actual_state
        self.health_check = health_check
        self.alarms = []
        self.schedules = []

    def add_alarms(self, Alarm):
        self.alarms.append(Alarm)

    def remove_alarms(self, Alarm):
        self.alarms.remove(Alarm)

    def add_schedules(self, Schedule):
        self.schedules.append(Schedule)
