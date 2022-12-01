from heapq import *
from copy import *
import math


def parent(i):
    return (i - 1) // 2


def leftChild(i):
    return ((2 * i) + 1)


def rightChild(i):
    return ((2 * i) + 2)


def swap(heap, i, index):
    smallerPos = i
    biggerPos = parent(i)

    index[heap[biggerPos][1]] -= 1
    index[heap[smallerPos][1]] += 1

    temp = heap[biggerPos]
    heap[biggerPos] = heap[smallerPos]
    heap[smallerPos] = temp


def shiftUp(heap, i, index):
    while (i > 0 and heap[parent(i)][0] > heap[i][0]):
        swap(heap, i, index)
        i = parent(i)


def dijkstra(nodesList, source, end):
    # Criando as variáveis suporte
    nodes = {}
    index = {}
    s = {}

    for airport in nodesList:
        # Criando o dicionário 's' de resultado com as tuplas
        s[airport.oaci] = (math.inf, airport.oaci, None)
        nodes[airport.oaci] = airport  # Mapeando os nós aos seus OACI

    # Inicializando a tupla do nó inicial
    s[source] = (0, source, source)  # (param[0], nodeOaci[1], fromOaci[2])

    # Criação do heap e auxiliares
    heap = []
    i = 0
    decr = 0

    # Inserindo as tuplas do conjunto resposta 's' no heap
    for airport in nodesList:
        heappush(heap, s[airport.oaci])
        index[airport.oaci] = i  # Mapeando os índices das tuplas no heap
        i += 1

    # print(index)

    # Loop do Dijkstra
    while len(heap) > 0:  # 0, 1, 2, ... , 7 ( 8 elementos )

        # # Print de debug
        # print('\n\n','step',decr+1)
        # print('ANSWER:',s)
        # print('HEAP',heap)

        # Retirando a tupla de menor preço no heap
        first = heappop(heap)
        del index[first[1]]
        j = 0
        for el in heap:  # Reajustando o contador de index
            index[el[1]] = j
            j += 1
        decr += 1  # Decrementando

        # Olhando as arestas do aeroporto que saiu do heap
        for flight in nodes[first[1]].flights:
            # Se não estou mapeando o index, não preciso olhar (previne erros)
            if flight.destination.oaci in index.keys():
                # Se o voo tem um menor preço do que o que está mapeado
                if flight.price + s[flight.origin.oaci][0] < s[flight.destination.oaci][0]:
                    # Substitua a tupla no conjunto resposta
                    s[flight.destination.oaci] = (
                        flight.price + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)
                    heap[index[flight.destination.oaci]] = (
                        flight.price + s[flight.origin.oaci][0], flight.destination.oaci, flight.origin.oaci)  # Substitua a tupla no heap
                    # Arrumar a ordem do heap
                    shiftUp(heap, (index[flight.destination.oaci]), index)

    # # Print final
    # print('\n\nfinal step\n','ANSWER:',s)
    # print('HEAP',heap)

    node = s[end]
    path = []
    while node[1] != s[source][1]:
        path.append(nodes[node[1]])
        node = s[node[2]]
    path.append(nodes[source])
    path.reverse()
    return path

    # print('\n\nSHORTEST PATH')
    # print('menor preço:', s[end][0])
    # for e in path:
    #     print(e[0], e[1].name)
