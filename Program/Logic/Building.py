# coding=utf-8
from Program.Logic import Residential


class Building(Residential):
    """Is a type of residential"""

    def __init__(self, number):
        self.number = number
