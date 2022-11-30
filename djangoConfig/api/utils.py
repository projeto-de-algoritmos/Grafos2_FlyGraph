import json

from .models.flight import Flight
from .graphs import *

def jsonalize(object):
    parsed = json.dumps(object, indent=2, default=Flight.ComplexHandler)
    return parsed

def pprint(object):
    print(jsonalize(object))

def printFinalPath(finalPath):
    i = 0
    totalPrice = 0
    for airport in finalPath:
        for flight in airport.flights:
            if i != len(finalPath)-1:
                if flight.used == True and flight.origin.oaci == finalPath[i].oaci and flight.destination.oaci == finalPath[i+1].oaci:
                    print(f".........................................................................\nPASSO {i+1} .............. Voo DE({flight.origin.oaci} - {finalPath[i].name}) => PARA({flight.destination.oaci} - {finalPath[i+1].name}) \n.....................: {flight.seats} Assentos disponíveis | Preço: R${flight.price}\n.........................................................................\n")
                    i += 1
                    totalPrice += flight.price
                    break
    print(f"PREÇO TOTAL DA VIAGEM: R${totalPrice}")
