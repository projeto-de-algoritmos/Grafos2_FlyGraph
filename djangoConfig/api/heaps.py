from heapq import *
from copy import *
from datetime import timedelta, time
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




