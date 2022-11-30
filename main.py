from pandas import *
from djangoConfig.api.graphs import *
from djangoConfig.api.heaps import *
from djangoConfig.api.utils import *
from os import *

def clear():
    system('cls' if __name__ == 'nt' else 'clear')

if __name__ == "__main__":
    nodesList = []

    # DIJKSTRA
    xls = ExcelFile("./djangoConfig/api/data/heap.xlsx")
    nodes = xls.parse(xls.sheet_names[0]).to_dict()
    xls = ExcelFile("./djangoConfig/api/data/heap.xlsx")
    edges = xls.parse(xls.sheet_names[1]).to_dict()

    createAirports(nodesList=nodesList, nodes=nodes)
    createFlights(nodesList=nodesList, edges=edges)

    printGraph(nodesList)
    dijkstra(nodesList, 'S', 'T')

    # AEROPORTOS
    # xls = ExcelFile("./djangoConfig/api/data/aeroportos.xlsx")
    # nodes = xls.parse(xls.sheet_names[0]).to_dict()
    # xls = ExcelFile("./djangoConfig/api/data/tarifas.xlsx")
    # edges = xls.parse(xls.sheet_names[0]).to_dict()

    # createAirports(nodesList=nodesList, nodes=nodes)
    # createFlights(nodesList=nodesList, edges=edges)

    # clear()
    # for i in range(len(nodesList)):
    #     print(f"({i+1}) => {nodesList[i].name} ({nodesList[i].state})")    
    # print("Qual o (ID) do aeroporto que será sua origem?")
    # origin = int(input())
    # print("Qual o (ID) do aeroporto que será seu destino?")
    # destination = int(input())

    # finalPath = bfs(nodesList, nodesList[origin-1].oaci, nodesList[destination-1].oaci)
    # if finalPath is None:
    #     exit()
    # printFinalPath(finalPath)
    
    # print(f"GRAFO FORTEMENTE CONECTADO? {checkStrongConnectivity(nodesList, nodesList[0])}")

    # plotGraph(finalPath)