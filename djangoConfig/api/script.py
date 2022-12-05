from pandas import *
from .graphs import *
from .heaps import *

from .utils import *
from os import *

from .models.response import Response


nodesList = []

# AEROPORTOS
xls = ExcelFile("./api/data/aeroportos.xlsx")
nodes = xls.parse(xls.sheet_names[0]).to_dict()
xls = ExcelFile("./api/data/tarifas.xlsx")
edges = xls.parse(xls.sheet_names[0]).to_dict()

createAirports(nodesList=nodesList, nodes=nodes)
createFlights(nodesList=nodesList, edges=edges)


def bfsExecute(origin, destination):

    finalPath = bfs(
        nodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)
    # print(finalPath)
    i = 0
    totalPrice = 0
    totalTime = 0
    totalFlights = []
    result=[]
    for airport in finalPath:
        if i != len(finalPath)-1:
            for flight in airport.flights:
                if (flight.used == True
                        and flight.origin.oaci == finalPath[i].oaci
                        and flight.destination.oaci == finalPath[i+1].oaci):
                    totalFlights.append(flight)
                    i += 1
                    totalPrice += flight.price
                    totalTime += flight.travelTimeMinutes
                    break
    result = Response(total_price=totalPrice,
                      num_arestas=i, flights=totalFlights, total_time=totalTime)

    return result


def dijikstraExecute(origin, destination):

    finalPath = dijkstra(
        nodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)
    # print(finalPath)
    i = 0
    totalPrice = 0
    totalTime = 0
    totalFlights = []
    for airport in finalPath:
        if i != len(finalPath)-1:
            for flight in airport.flights:
                if (
                    flight.origin.oaci == finalPath[i].oaci
                        and flight.destination.oaci == finalPath[i+1].oaci):
                    totalFlights.append(flight)
                    i += 1
                    totalPrice += flight.price
                    totalTime += flight.travelTimeMinutes
                    break
    result = Response(total_price=totalPrice,
                      num_arestas=i, flights=totalFlights, total_time=totalTime)

    return result

def MultiBfsExecute(origin, destination):
    i = 0
    totalPrice = 0
    totalTime = 0
    totalFlights = []
    paths =[]
    finalPath = bfs(nodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)
    paths.append(finalPath)
    results=[]
    try:
        newNodesList= copy.copy(nodesList)
        for node in newNodesList:
            for edge in node.flights:
                if edge.destination.oaci == finalPath[1].oaci:
                    node.removeEdge(edge)
        finalPath = bfs(newNodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)
        if finalPath != None:
            paths.append(finalPath)
    except: 
        print("aa")
    print(paths)
    for path in paths:
        for airport in path:        
            if i != len(finalPath)-1 and finalPath != None:
                for flight in airport.flights:
                    if (
                        flight.origin.oaci == finalPath[i].oaci
                            and flight.destination.oaci == finalPath[i+1].oaci):
                        totalFlights.append(flight)
                        print(flight.origin.oaci)
                        i += 1
                        totalPrice += flight.price
                        totalTime += flight.travelTimeMinutes
    results = Response(total_price=totalPrice,
                      num_arestas=i, flights=totalFlights, total_time=totalTime)
    
    return results

def bfsPlot(origin, destination):

    finalPath = bfs(
        nodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)

    return finalPath


def returnAirport():
    result = returnAirports(nodeList=nodesList)
    return result


def checkGraph():
    result = checkStrongConnectivity(nodesList, nodesList[0])
    return result


def plot():
    plotGraph(nodesList=nodesList)


def pathPlot(finalPath):
    plotGraph(nodesList=finalPath)
