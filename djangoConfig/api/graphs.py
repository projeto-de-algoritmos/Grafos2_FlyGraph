import sys
import copy
import networkx as nx
from queue import Queue
from .models.flight import Flight
from .models.airport import Airport

import matplotlib.pyplot as plt

sys.path.insert(0, "models")
sys.path.insert(0, "data")


def createAirports(nodesList, nodes):
    for i in nodes["OACI"]:
        airport = Airport(
            oaci=nodes["OACI"][i],
            state=nodes["UF"][i],
            operation=nodes["Operacao"][i],
            latitude=nodes["Latitude"][i],
            longitude=nodes["Longitude"][i],
            altitude=nodes["Altitude"][i],
            name=nodes["Nome"][i],
            town=nodes["Municipio_Atendido"][i],
            flights=[]
        )
        nodesList.append(airport)


def createFlights(nodesList, edges):
    airportNodes = {}
    for airport in nodesList:
        airportNodes[airport.oaci] = airport
    for i in edges["ORIGEM"]:
        flight = Flight(
            origin=airportNodes[edges["ORIGEM"][i]],
            destination=airportNodes[edges["DESTINO"][i]],
            price=edges["TARIFA"][i],
            seats=edges["ASSENTOS"][i],
            used=False
        )
        for node in nodesList:
            if edges["ORIGEM"][i] == node.oaci:
                node.appendEdge(flight)
                break


def printGraph(nodesList):
    for node in nodesList:
        edgeList = ''
        for edge in node.flights:
            edgeList = edgeList + edge.destination.oaci + ' '
        print(f"Nó({node.oaci}) -> LA: [ {edgeList}]")


def returnAirports(nodeList):
    result = []
    for node in nodeList:
        result.append(node.to_dict())
    print(len(result))
    return result


def bfs(nodesList, source, end):
    queue = Queue()
    visited = {}
    parent = {}
    nodes = {}

    for node in nodesList:
        visited[node.oaci] = False
        parent[node.oaci] = None
        nodes[node.oaci] = node

    visited[source] = True
    n = next((n for n in nodesList if n.oaci == source), None)
    queue.put(n)

    for node in nodesList:
        if not visited[node.oaci]:

            while not queue.empty():
                u = queue.get()
                for v in u.flights:
                    if not visited[v.destination.oaci]:
                        parent[v.destination.oaci] = u.oaci
                        v.used = True
                        visited[v.destination.oaci] = True
                        n = next(
                            (x for x in nodesList if x.oaci == v.destination.oaci), None)
                        queue.put(n)

    path = []
    if parent[end] != None:
        while end is not None:
            path.append(copy.copy(nodes[end]))
            end = parent[end]
        path.reverse()
        return path


def reverseGraph(nodesList):
    reversedGraph = []
    reverseOrder = list(reversed(copy.copy(nodesList)))
    mapping = {}
    i = 0

    for airport in reverseOrder:
        mapping[airport.oaci] = i
        reversedGraph.append(Airport(
            oaci=airport.oaci,
            state=airport.state,
            operation=airport.operation,
            latitude=airport.latitude,
            longitude=airport.longitude,
            altitude=airport.altitude,
            name=airport.name,
            town=airport.town,
            flights=[]
        ))
        i += 1

    for airport in reverseOrder:
        for flight in airport.flights:
            newFlight = copy.copy(flight)
            newFlight.origin = copy.copy(flight.destination)
            newFlight.destination = copy.copy(flight.origin)
            reversedGraph[mapping[flight.destination.oaci]].flights = [
                newFlight] + reversedGraph[mapping[flight.destination.oaci]].flights

    return (reversedGraph)


def checkStrongConnectivity(nodesList, origin):
    stronglyConnected = True
    result = {"origin": "",
              "destination": "", "stronglyConnected": True, "Grafo": ""}

    for destination in nodesList:
        if (origin.oaci != destination.oaci
                and bfs(nodesList, origin.oaci, destination.oaci) is None):
            stronglyConnected = False
            result = {"origin": f"{origin.oaci} - {origin.name}",
                      "destination": f"{destination.oaci} - {destination.name}", "stronglyConnected": stronglyConnected, "Grafo": "Original"}
            break

    reversedGraph = reverseGraph(nodesList)
    for destination in nodesList:
        if (origin.oaci != destination.oaci
                and bfs(reversedGraph, origin.oaci, destination.oaci) is None):
            stronglyConnected = False
            result = {"destination": f"{origin.oaci} - {origin.name}",
                      "origin": f"{destination.oaci} - {destination.name}", "stronglyConnected": stronglyConnected, "Grafo": "Reverso"}
            break
    return result


def plotGraph(nodesList):
    plt.close('all')
    G = nx.Graph()
    G.add_node(node.oaci for node in nodesList)
    for node in nodesList:
        for edge in node.flights:
            G.add_edge(edge.origin.oaci, edge.destination.oaci)
    nx.draw_networkx(G)
    plt.show()
