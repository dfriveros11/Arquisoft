# coding=utf-8
from Program.Logic import Property


class House(Property):
    """House is a property"""

    def __init__(self, number_house):
        self.number_house = number_house