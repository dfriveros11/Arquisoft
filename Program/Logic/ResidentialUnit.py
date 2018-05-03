# coding=utf-8
from abc import ABCMeta


class ResidentialUnits(metaclass=ABCMeta):
    """Main abstract class"""
    def __init__(self, address):
        self.address = address


    def operation(self):
        """operation"""
        pass
