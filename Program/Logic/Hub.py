# coding=utf-8


class Hub():
    """hub"""

    def __init__(self, frequency, max_health_check):
        self.frequency = frequency
        self.max_health_check = max_health_check
        self.locks = []

    def add(self, lock):
        self.locks.append(lock)

    def remove(self, lock):
        self.locks.remove(lock)