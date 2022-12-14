
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import script


@api_view(['GET'])
def getData(request):

    origin = int(request.query_params['ido'])
    destination = int(request.query_params['idd'])
    result = script.bfsExecute(origin, destination)
    response = result.to_dict()

    return Response(response)


@api_view(['GET'])
def getDataDijkstra(request):

    origin = int(request.query_params['ido'])
    destination = int(request.query_params['idd'])
    type = request.query_params['type']
    try:
        result = script.dijikstraExecute(origin, destination, type)
        response = result.to_dict()

        return Response(response)
    except:
        return Response("Não existe caminho possível")


@api_view(['GET'])
def getAirports(request):

    response = script.returnAirport()
    return Response(response)


@api_view(['GET'])
def checkGraph(request):

    response = script.checkGraph()
    return Response(response)


@api_view(['GET'])
def plot(request):

    script.plot()
    return Response()


@api_view(['GET'])
def plotPath(request):

    origin = int(request.query_params['ido'])
    destination = int(request.query_params['idd'])
    response = script.bfsPlot(origin, destination)

    script.pathPlot(response)
    return Response()
