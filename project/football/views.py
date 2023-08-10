from django.shortcuts import render
import json
import requests
import pandas as pd
import os
from .models import Player
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from .helpers_and_objects import * 


# Create your views here.
def myview(request, player_name):
    player_name = clean_player_name(request, player_name)
    all_players = Player.objects.all()
    already_exists = check_for_player(all_players, player_name)
    #if not in database pull data
    if already_exists == False: 
        try:
            player_id = get_player_id(player_name)
            get_player_data(player_id)
            stats = load_player(player_name)
            a = Player(name = player_name, passing_career = json.dumps(stats[0]), rushing_career = json.dumps(stats[1]), receiving_career = json.dumps(stats[2]), defensive_career = json.dumps(stats[4]), scoring_career = json.dumps(stats[3])
                       ,position = stats[5], last_team = stats[6])
            a.save()
        except:
            return render(request, "notFound.html")
    else:
        stats = pull_player(player_name)
    return render(request, "index.html", {'name': player_name, 'scoring_career' : stats[3],  'passing_career' : stats[0],'rushing_career' : stats[1],  'receiving_career' : stats[2],  'defensive_career' : stats[4]})


def searchView(request):
    return render(request, "search.html")


def allPlayersView(request):
    return render(request, "pastPlayers.html", {'allPlayers': Player.objects.all(), 'recentPlayers': Player.objects.all().order_by('-created_date'), 'mostViewed': Player.objects.all().order_by('-count')})


def pullPlayerStats(request, player_name):
    all_players = Player.objects.all()
    jsonDec = json.decoder.JSONDecoder()
    player_name  = request.GET.get('player_name')
    stats = pull_player(player_name)
    return render(request, "pullStats.html", {'name': player_name, 'scoring_career' : stats[3],  'passing_career' : stats[0],'rushing_career' : stats[1],  'receiving_career' : stats[2],  'defensive_career' : stats[4]})
    
