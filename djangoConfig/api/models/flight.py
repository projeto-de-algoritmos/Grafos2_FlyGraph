import json
from .airport import Airport

class Flight:
    def __init__(self,
                 id,
                 origin,
                 departure,
                 destination,
                 arrival,
                 travelTimeMinutes,
                 price,
                 seats,
                 used=False):
        self.__origin = origin
        self.__destination = destination
        self.__price = price 
        self.__seats = seats
        self.__used = used
        self.__id = id
        self.__departure = departure
        self.__arrival = arrival 
        self.__travelTimeMinutes = travelTimeMinutes

    def jsonable(self):
        return self.to_dict()

    def ComplexHandler(Obj):
        if hasattr(Obj, 'jsonable'):
            return Obj.jsonable()
    
    def to_dict(self):
        return{
            "origin": json.loads(json.dumps(self.origin, default=Airport.ComplexHandler)), 
            "destination": json.loads(json.dumps(self.destination, default=Airport.ComplexHandler)), 
            "price": self.price, 
            "seats":self.seats, 
            "used": self.used,
            "departure": self.departure,
            "arrival": self.arrival,
            "id": self.id,
            "travelTimeMinutes": self.travelTimeMinutes
        }

    @property
    def origin(self):
        return self.__origin
    
    @property
    def destination(self):
        return self.__destination
    
    @property
    def price(self):
        return self.__price

    @property
    def seats(self):
        return self.__seats
    
    @property
    def used(self):
        return self.__used

    @property
    def id(self):
        return self.__id

    @property
    def departure(self):
        return self.__departure

    @property
    def arrival(self):
        return self.__arrival

    @property
    def travelTimeMinutes(self):
        return self.__travelTimeMinutes

    @origin.setter
    def origin(self, origin):
        self.__origin = origin

    @destination.setter
    def destination(self, destination):
        self.__destination = destination
    
    @price.setter
    def price(self, price):
        self.__price = price

    @seats.setter
    def seats(self, seats):
        self.__seats = seats

    @used.setter
    def used(self, used):
        self.__used = used

    @id.setter
    def id(self, id):
        self.__id = id

    @departure.setter
    def departure(self, departure):
        self.__departure = departure

    @arrival.setter
    def arrival(self, arrival):
        self.__arrival = arrival

    @travelTimeMinutes.setter
    def travelTimeMinutes(self, travelTimeMinutes):
        self.__travelTimeMinutes = travelTimeMinutes