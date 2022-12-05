import sys
import copy
import networkx as nx
from queue import Queue
from .models.flight import Flight
from .models.airport import Airport
from .heaps import *
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
            id=edges["ID"][i],
            origin=airportNodes[edges["ORIGEM"][i]],
            departure=edges["DEPARTURE"][i],
            destination=airportNodes[edges["DESTINO"][i]],
            arrival=edges["ARRIVAL"][i],
            travelTimeMinutes=edges["TRAVEL_TIME_MIN"][i],
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
    # print(len(result))
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

def dijkstra(nodesList, source, end, type = 'price'):
    nodes = {}
    index = {}
    s = {}

    if type in ('time', 'price'):
        for airport in nodesList:
            s[airport.oaci] = (math.inf, airport.oaci, None)
            nodes[airport.oaci] = airport  

        s[source] = (0, source, source)  

    elif type == 'real-time':
        for airport in nodesList:
            s[airport.oaci] = (math.inf, airport.oaci, None, None)
            nodes[airport.oaci] = airport  

        s[source] = (0, source, source, None)  

    heap = []
    i = 0
    decr = 0

    # Inserindo as tuplas do conjunto resposta 's' no heap
    for airport in nodesList:
        heappush(heap, s[airport.oaci])
        index[airport.oaci] = i  
        i += 1

    # Loop do Dijkstra
    while len(heap) > 0:  
        first = heappop(heap)
        del index[first[1]]
        j = 0
        for el in heap:  
            index[el[1]] = j
            j += 1
        decr += 1  

        if type == 'price':
        # Olhando as arestas do aeroporto que saiu do heap
            for flight in nodes[first[1]].flights:
                # Se não estou mapeando o index, não preciso olhar (previne erros)
                if (flight.destination.oaci in index.keys()
                    and index[flight.destination.oaci] < len(heap)):
                    # Se o voo tem um menor preço do que o que está mapeado
                    if flight.price + s[flight.origin.oaci][0] < s[flight.destination.oaci][0]:
                        # Substitua a tupla no conjunto resposta
                        s[flight.destination.oaci] = (
                            flight.price + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)
                        heap[index[flight.destination.oaci]] = (
                            flight.price + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)  # Substitua a tupla no heap
                        # Arrumar a ordem do heap
                        shiftUp(heap, (index[flight.destination.oaci]), index)
        elif type == 'time':
            # Olhando as arestas do aeroporto que saiu do heap
            for flight in nodes[first[1]].flights:
                # Se não estou mapeando o index, não preciso olhar (previne erros)
                if (flight.destination.oaci in index.keys()
                    and index[flight.destination.oaci] < len(heap)):
                    # Se o voo tem um menor preço do que o que está mapeado
                    if flight.travelTimeMinutes + s[flight.origin.oaci][0] < s[flight.destination.oaci][0]:
                        # Substitua a tupla no conjunto resposta
                        s[flight.destination.oaci] = (
                            flight.travelTimeMinutes + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)
                        heap[index[flight.destination.oaci]] = (
                            flight.travelTimeMinutes + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)  # Substitua a tupla no heap
                        # Arrumar a ordem do heap
                        shiftUp(heap, (index[flight.destination.oaci]), index)
        elif type == 'real-time':
            # Olhando as arestas do aeroporto que saiu do heap
            for flight in nodes[first[1]].flights:
                # Se não estou mapeando o index, não preciso olhar (previne erros)
                if (flight.destination.oaci in index.keys()
                    and index[flight.destination.oaci] < len(heap)):
                    # Se o voo tem um menor preço do que o que está mapeado
                    if (flight.travelTimeMinutes + s[flight.origin.oaci][0] < s[flight.destination.oaci][0]
                        and (flight.origin.oaci == source or ((s[flight.origin.oaci][3]+timedelta(hours=1)).time() <= flight.departure.time()))):
                        # Substitua a tupla no conjunto resposta
                        s[flight.destination.oaci] = (
                            flight.travelTimeMinutes + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci, flight.arrival)
                        heap[index[flight.destination.oaci]] = (
                            flight.travelTimeMinutes + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci, flight.arrival)  # Substitua a tupla no heap
                        # Arrumar a ordem do heap
                        shiftUp(heap, (index[flight.destination.oaci]), index)

    node = s[end]
    path = []
    while node[1] != s[source][1]:
        path.append(nodes[node[1]])
        node = s[node[2]]
    path.append(nodes[source])
    path.reverse()
    
    return path