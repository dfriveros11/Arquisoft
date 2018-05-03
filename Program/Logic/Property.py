# coding=utf-8
from Program.Logic import ResidentialUnit, Hub


class Property(ResidentialUnit):
    """The leaf"""

    def __init__(self, property_id):
        self.property_id = property_id
        self.hub = Hub()
    def operation(self):
        """operation"""
        pass