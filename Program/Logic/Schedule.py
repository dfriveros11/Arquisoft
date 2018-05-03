# coding=utf-8


class Schedule:
    def __init__(self, schedule_id, time_zone):
        self.schedule_id = schedule_id
        self.time_zone = time_zone
        self.dates = []

    def add_dates(self, Date):
        self.dates.append(Date)

    def remove_dates(self, Date):
        self.dates.append(Date)