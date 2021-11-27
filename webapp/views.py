from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from base64 import b64encode
from rest_framework import serializers

from webapp.models import liga,equipo,jugador
from webapp.serializers import LigaSerializer,JugadorSerializer, EquipoSerializer

from django.core.files.storage import default_storage
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Ligas':'/leagues/',
        'Ligas_id':'/leagues/<str:league_id>/',
        'Ligas_id_teams':'/leagues/<str:league_id>/teams/',
        'Ligas_id_players':'/leagues/<str:league_id>/players/',
        'Teams':'/teams/',
        'Teams_id':'/teams/<str:team_id>/',
        'Teams_id_player':'/teams/<str:team_id>/players/',
        'Players':'/players/',
        'Players_id':'/players/<str:player_id>/',
        }

    return Response(api_urls)

@api_view(['GET','POST'])
def leagueslist(request):
    if request.method=='GET':
        leagues = liga.objects.all()
        serializer = LigaSerializer(leagues, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        if request.data['name'] and request.data['sport']:
            string = request.data['name']+':'+request.data['sport']
            request.data['id'] = b64encode(string.encode()).decode('utf')
            request.data['id'] = request.data['id'][:21]
            try:
                lig = liga.objects.get(id=request.data['id'])
                serializer = LigaSerializer(lig, many=False)
                return Response(serializer.data,status=status.HTTP_409_CONFLICT)
            except liga.DoesNotExist:
                request.data.update({"id": request.data['id']})
                request.data.update({"teams": "https://tarea2cgkuschel.herokuapp.com/webapp/leagues/{}/teams".format(request.data['id'])})
                request.data.update({"players": "https://tarea2cgkuschel.herokuapp.com/webapp/teams/{}/players".format(request.data['id'])})
                request.data.update({"self": "https://tarea2cgkuschel.herokuapp.com/webapp/leagues/{}".format(request.data['id'])})
                print(request.data)
                
                serializer = LigaSerializer(data=request.data)
                

                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'DELETE'])
def leaguesdetail(request, pk):
    if request.method=='GET':
        try:
            leagues = liga.objects.get(id=pk)
            serializer = LigaSerializer(leagues, many=False)
            return Response(serializer.data)
        except liga.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method=='DELETE':
        league = liga.objects.get(id=pk)
        league.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def leaguesdetailteam(request, pk):
    if request.method=='GET':
        try:
            teams = equipo.objects.filter(liga_id=pk)
            serializer = EquipoSerializer(teams, many=True)
            return Response(serializer.data)
        except equipo.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method=='POST':
        if request.data['name'] and request.data['city']:
            string = request.data['name']+':'+request.data['city']
            request.data['id'] = b64encode(string.encode()).decode('utf')
            request.data['id'] = request.data['id'][:21]
            try:
                equi = equipo.objects.get(id=request.data['id'])
                serializer = EquipoSerializer(equi, many=False)
                return Response(serializer.data,status=status.HTTP_409_CONFLICT)
            except equipo.DoesNotExist:
                request.data.update({"id": request.data['id']})
                request.data.update({"liga_id": pk})
                try:
                    liga.objects.get(id=pk)
                    request.data.update({"league": "https://tarea2cgkuschel.herokuapp.com/webapp/leagues/{}".format(request.data['liga_id'])})
                    request.data.update({"players": "https://tarea2cgkuschel.herokuapp.com/webapp/teams/{}/players".format(request.data['id'])})
                    request.data.update({"self": "https://tarea2cgkuschel.herokuapp.com/webapp/teams/{}".format(request.data['id'])})
                    serializer = EquipoSerializer(data=request.data)
                    print(request.data)

                    if serializer.is_valid():
                        serializer.save()
                        print(serializer.errors)
                    else:
                        print(serializer.errors)
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                except liga.DoesNotExist:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST'])
def teamsdetailplayer(request, pk):
    if request.method=='GET':
        try:
            player = jugador.objects.filter(equipo_id=pk)
            serializer = JugadorSerializer(player, many=True)
            return Response(serializer.data)
        except jugador.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method=='POST':
        if request.data['name'] and request.data['position']:
            string = request.data['name']+':'+request.data['position']
            request.data['id'] = b64encode(string.encode()).decode('utf')
            request.data['id'] = request.data['id'][:21]
            try:
                jug = jugador.objects.get(id=request.data['id'])
                serializer = EquipoSerializer(jug, many=False)
                return Response(serializer.data,status=status.HTTP_409_CONFLICT)
            except jugador.DoesNotExist:
                request.data.update({"id": request.data['id']})
                request.data.update({"equipo_id": pk})
                try:
                    print(pk)
                    equipote = equipo.objects.get(id=pk)
                    serializer2 = EquipoSerializer(equipote, many=False)
                    request.data.update({"league": "https://tarea2cgkuschel.herokuapp.com/webapp/leagues/{}".format(serializer2.data['liga_id'])})
                    request.data.update({"team": "https://tarea2cgkuschel.herokuapp.com/webapp/teams/{}".format(request.data['equipo_id'])})
                    request.data.update({"self": "https://tarea2cgkuschel.herokuapp.com/webapp/players/{}".format(request.data['id'])})
                    serializer = JugadorSerializer(data=request.data)
                    print(request.data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(serializer.errors)
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except equipo.DoesNotExist:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def teamlist(request):
    if request.method=='GET':
        teams = equipo.objects.all()
        serializer = EquipoSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','DELETE'])
def teamsdetail(request, pk):
    if request.method=='GET':
        try:
            teams = equipo.objects.get(id=pk)
            serializer = EquipoSerializer(teams, many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except equipo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method=='DELETE':
        try:
            team = equipo.objects.get(id=pk)
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except equipo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def leaguesplayers(request,pk):
    if request.method=='GET':
        try:
            equipos = equipo.objects.filter(liga_id=pk)
            listasi = []
            for team in equipos.iterator():
                listasi.append(team.id)
            players = jugador.objects.filter(equipo_id__in=listasi)
            serializer = JugadorSerializer(players, many=True)
            return Response(serializer.data)
        except equipo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET','PUT'])
def ligatrain(request,pk):
    if request.method=='GET':
        try:
            teams = equipo.objects.filter(liga_id=pk)
            serializer = EquipoSerializer(teams, many=True)
            return Response(serializer.data)
        except equipo.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method=='PUT':
        equipos = equipo.objects.filter(liga_id=pk)
        listasi = []
        for team in equipos.iterator():
            listasi.append(team.id)
        players = jugador.objects.filter(equipo_id__in=listasi)
        for jugi in players.iterator():
            players.filter(id=jugi.id).update(time_trained=request.data['time_trained'])
        serializer = JugadorSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def teamtrain(request,pk):
    if request.method=='PUT':
        players = jugador.objects.filter(equipo_id=pk)
        for jugi in players.iterator():
            players.filter(id=jugi.id).update(time_trained=request.data['time_trained'])
        serializer = JugadorSerializer(players, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def playertrain(request,pk):
    if request.method=='PUT':
        jugadores = jugador.objects.get(id=pk)
        jugadores.time_trained= request.data['time_trained']
        serializer = JugadorSerializer(jugadores, many=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def playerlist(request):
    if request.method=='GET':
        players = jugador.objects.all()
        serializer = JugadorSerializer(players, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','DELETE'])
def playerdetail(request, pk):
    if request.method=='GET':
        try:
            jugadores = jugador.objects.get(id=pk)
            serializer = JugadorSerializer(jugadores, many=False)
            return Response(serializer.data)
        except jugador.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method=='DELETE':
        player = jugador.objects.get(id=pk)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

