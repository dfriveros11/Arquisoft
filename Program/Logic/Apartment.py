# coding=utf-8
from Program.Logic import Property


class Apartment(Property):
    """Property"""
    def __init__(self, number_tower, number_house):
        self.number_tower = number_tower
        self.number_house = number_house