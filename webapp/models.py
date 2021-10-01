from django.db import models
from base64 import b64encode
from django.db.models.deletion import CASCADE

class liga(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    teams = models.CharField(max_length=100, default=' ')
    players = models.CharField(max_length=100, default=' ')
    selfi = models.CharField(max_length=100, default=' ')

class equipo(models.Model):
    liga_id = models.ForeignKey(liga, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    league = models.CharField(max_length=100, default=' ')
    players = models.CharField(max_length=100, default=' ')
    selfi = models.CharField(max_length=100, default=' ')

class jugador(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    equipo_id = models.ForeignKey(equipo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=100)
    time_trained = models.IntegerField()
    league = models.CharField(max_length=100, default=' ')
    team = models.CharField(max_length=100, default=' ')
    selfi = models.CharField(max_length=100, default=' ')

