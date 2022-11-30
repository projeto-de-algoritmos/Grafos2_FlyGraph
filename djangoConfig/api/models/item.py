import math

class Item:
    def __init__(self,
                airport,
                heapPos = 0,
                parameter = math.inf,
                origin = -math.inf
                ):
        self.__parameter = parameter
        self.__airport = airport
        self.__origin = origin
        self.__heapPos = heapPos
    
    @property
    def parameter(self):
        return self.__parameter

    @property
    def airport(self):
        return self.__airport

    @property
    def origin(self):
        return self.__origin

    @property
    def heapPos(self):
        return self.__heapPos

    @parameter.setter
    def parameter(self, parameter):
        self.__parameter = parameter

    @airport.setter
    def airport(self, airport):
        self.__airport = airport
    
    @origin.setter
    def origin(self, origin):
        self.__origin = origin

    @heapPos.setter
    def heapPos(self, heapPos):
        self.__heapPos = heapPos