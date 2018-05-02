# coding=utf-8
from Program.Logic import ResidentialUnit


class Residential(ResidentialUnit):
    """This is the composite"""
    def __init__(self):
        self._residential_units = set()

    def operation(self):
        """operation"""
        for residential in self._residential_units:
            residential.operation()

    def add(self, residential_unit):
        """Add a new element in the list"""
        self._residential_units.add(residential_unit)

    def remove(self, residential_unit):
        """remove a element of the list"""
        self._residential_units.discard(residential_unit)