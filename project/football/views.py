from django.shortcuts import render
from typing import List
import json
import requests
import pandas as pd
import os
from .models import Player
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone



# Create your views here.
def myview(request, player_name):
    player_name = clean_player_name(request, player_name)
    all_players = Player.objects.all()
    # jsonDec = json.decoder.JSONDecoder()
    already_exists = check_for_player(all_players, player_name)

    #add database check here
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

    #stats = retrieve_stats(request, player_name)
    return render(request, "index.html", {'name': player_name, 'scoring_career' : stats[3],  'passing_career' : stats[0],'rushing_career' : stats[1],  'receiving_career' : stats[2],  'defensive_career' : stats[4]})



def searchView(request):
    #player_name = "Dak Prescott"
    #player_id = get_player_id(player_name)
    #get_player_data(player_id)
    #stats = load_player(player_name)

    return render(request, "search.html")

def allPlayersView(request):
    print(Player.objects.all().order_by('-created_date'))
    return render(request, "pastPlayers.html", {'recentPlayers': Player.objects.all().order_by('-created_date'), 'mostViewed': Player.objects.all().order_by('-count')})

def pullPlayerStats(request, player_name):
    #turn this into pull_player function
    all_players = Player.objects.all()
    jsonDec = json.decoder.JSONDecoder()
    player_name  = request.GET.get('player_name')
    stats = pull_player(player_name)

    # for i in all_players:
    #     if i.name == player_name:
    #         passing_decoded = jsonDec.decode(i.passing_career)
    #         rushing_decoded = jsonDec.decode(i.rushing_career)
    #         receiving_decoded = jsonDec.decode(i.receiving_career)
    #         defensive_decoded = jsonDec.decode(i.defensive_career)
    #         scoring_decoded = jsonDec.decode(i.scoring_career)
            




    return render(request, "pullStats.html", {'name': player_name, 'scoring_career' : stats[3],  'passing_career' : stats[0],'rushing_career' : stats[1],  'receiving_career' : stats[2],  'defensive_career' : stats[4]})
    
rushing_labels = [
        "Games Played",
        "Rushing Attempts",
        "Rushing Yards",
        "Yards Per Rush Attempt",
        "Rushing Touchdowns",
        "Long Rushing",
        "Rushing 1st downs",
        "Rushing Fumbles",
        "Rushing Fumbles Lost"
      ]
receiving_labels = [
        "Games Played",
        "Receptions",
        "Receiving Targets",
        "Receiving Yards",
        "Yards Per Reception",
        "Receiving Touchdowns",
        "Long Reception",
        "Receiving First Downs",
        "Receiving Fumbles",
        "Receiving Fumbles Lost"
      ]
passing_labels = [
        "Games Played",
        "Completions",
        "Passing Attempts",
        "Completion Percentage",
        "Passing Yards",
        "Yards Per Pass Attempt",
        "Passing Touchdowns",
        "Interceptions",
        "Longest Pass",
        "Total Sacks",
        "Passer Rating",
        "Adjusted QBR"
      ]
defensive_labels = [
        "Games Played",
        "Total Tackles",
        "Solo Tackles",
        "Assist Tackles",
        "Sacks",
        "Forced Fumbles",
        "Fumbles Recovered",
        "Fumbles Recovered Yards",
        "Interceptions",
        "Interception Yards",
        "Average Interception Yards",
        "Interception Touchdowns",
        "Long Interception",
        "Passes Defended",
        "Stuffs",
        "Stuff Yards",
        "Kicks Blocked"
]
scoring_labels = [
        "Games Played",
        "Passing Touchdowns",
        "Rushing Touchdowns",
        "Receiving Touchdowns",
        "Return Touchdowns",
        "Total Touchdowns",
        "Total Two Point Conversions",
        "Kick Extra Points",
        "Field Goals",
        "Total Points"
]



class Rushing:
    labels: List[str]
    stats: List[int]
    year: int


    def __init__(self, stats: List[int], year: int) -> None:
        self.labels = rushing_labels
        self.stats = stats
        self.year = year

class Receiving:
    labels: List[str]
    stats: List[int]

    def __init__(self, stats: List[int], year: int) -> None:
        self.labels = receiving_labels
        self.stats = stats
        self.year = year

class Passing:
    labels: List[str]
    stats: List[int]
    year: int

    def __init__(self, stats: List[int], year: int) -> None:
        self.labels = passing_labels
        self.stats = stats
        self.year = year

class Defensive:
    labels: List[str]
    stats: List[int]
    year: int

    def __init__(self, stats: List[int], year: int) -> None:
        self.labels = defensive_labels
        self.stats = stats
        self.year = year

class Scoring:
    labels: List[str]
    stats: List[int]
    year: int

    def __init__(self, stats: List[int], year: int) -> None:
        self.labels = scoring_labels
        self.stats = stats
        self.year = year


class PlayerObject:
    name = str
    first_year = int
    last_year = int
    rush_career = {Rushing} 
    pass_career = {Passing}
    receiving_career = {Receiving}
    defensive_career = {Defensive}
    scoring_career = {Scoring}

    def __init__(self, name, first_year, last_year, rush_career, pass_career, receiving_career, defensive_career, scoring_career) -> None:
        self.name = name
        self.first_year = first_year
        self.last_year = last_year
        self.rush_career = rush_career
        self.pass_career = pass_career
        self.receiving_career = receiving_career
        self.defensive_career = defensive_career
        self.scoring_career = scoring_career

    #def get_season(year):
    #    return(self.)
    

#retrieves player_id from textfile
#could be improved to not create new dictionary on each call
def get_player_id(name):
    name = name.split()[0].capitalize() + " " + name.split()[1].capitalize()
    file_dir = os.path.dirname(__file__)
    file_path = os.path.join(file_dir, 'playerid.txt')
    player_id_file = open(file_path, 'r')

    #skips the first line because it is not a player
    first = player_id_file.readline()
    second = player_id_file.readline()
    second_split = second.split()
    player_id_dictionary = {second_split[2] + " " + second_split[3]: second_split[1]}
    player_id_list = player_id_file.readlines()

    #creates dictionary connecting names to player_id
    for i in player_id_list:
        x = i.split()
        player_id_dictionary[x[2] + " " + x[3]] = x[1]
    print(player_id_dictionary[name])
    return(player_id_dictionary[name])

#retrieves json file from espn api
def get_player_data(id):
    url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/" + id + "/stats"
    response = requests.get(url)

    matchup_response = requests.get(url, params={"view": "statistics"})

    json_object = json.dumps(matchup_response.json(), indent=2)

    with open("athlete.json", "w") as outfile:
        outfile.write(json_object)
    response.json()
    x = pd.json_normalize(matchup_response)

#creates player object for easier data storage
def load_player(player_name):
    #finish loading into player object and return object
    with open('athlete.json') as json_file:
        data = json.load(json_file)

        #get player position
        position = data['categories'][0]['statistics'][2]['position']

        last_team_raw = data['categories'][0]['statistics'][-1]['teamSlug']
        # last_team_split = last_team_raw.split('-')
        # last_team = ""
        # for i in last_team_split:
        #     last_team += i.capitalize() + " "

        last_team = get_last_team(last_team_raw)

        
     
        receiving_season_dict = {}
        rushing_season_dict = {}
        passing_season_dict = {}
        defensive_season_dict = {}
        scoring_season_dict = {}
        min_list = []
        max_list = []

        for i in range(len(data['categories'])):
            try:
               #iterates through each season type
                for j in range(len(data['categories'][i]['statistics'])):
                    season_type = data['categories'][i]['name']
                    season_year = data['categories'][i]['statistics'][j]['season']['year']
                    season_stats = data['categories'][i]['statistics'][j]['stats']
                    #adds stats to the apropriate dictionary
                    if (season_type == 'passing'):
                        passing_season = Passing(season_stats, season_year)
                        passing_season_dict[passing_season.year] = passing_season
                    if (season_type == 'receiving'):
                        receiving_season = Receiving(season_stats, season_year)
                        receiving_season_dict[receiving_season.year] = receiving_season
                    if (season_type == 'rushing'):
                        rushing_season = Rushing(season_stats, season_year)
                        rushing_season_dict[rushing_season.year] = rushing_season
                    if (season_type == 'defensive'):
                        defensive_season = Defensive(season_stats, season_year)
                        defensive_season_dict[defensive_season.year] = defensive_season
                    if (season_type == 'scoring'):
                        scoring_season = Scoring(season_stats, season_year)
                        scoring_season_dict[scoring_season.year] = scoring_season
            except:
                pass

        
        #package stats to send to template
        scoring_stats_packaged = []
        for i in scoring_season_dict:
            scoring_stats_packaged.append(tuple([i, scoring_season_dict[i].stats]))

        passing_stats_packaged = []
        for i in passing_season_dict:
            passing_stats_packaged.append(tuple([i, passing_season_dict[i].stats]))
        
        rushing_stats_packaged = []
        for i in rushing_season_dict:
            rushing_stats_packaged.append(tuple([i, rushing_season_dict[i].stats]))
        
        receiving_stats_packaged = []
        for i in receiving_season_dict:
            receiving_stats_packaged.append(tuple([i, receiving_season_dict[i].stats]))

        defensive_stats_packaged = []
        for i in defensive_season_dict:
            defensive_stats_packaged.append(tuple([i, defensive_season_dict[i].stats]))


        #adds title and labels to tuple lists
        scoring_career = ("Scoring", scoring_labels, scoring_stats_packaged)
        passing_career = ("Passing", passing_labels, passing_stats_packaged)
        rushing_career = ("Rushing", rushing_labels, rushing_stats_packaged)
        defensive_career = ("Defense", defensive_labels, defensive_stats_packaged)
        receiving_career = ("Receiving", receiving_labels, receiving_stats_packaged)

    return passing_career, rushing_career, receiving_career, scoring_career, defensive_career, position, last_team

def pull_player(player_name):
    
    all_players = Player.objects.all()
    
    jsonDec = json.decoder.JSONDecoder()
    
    for i in all_players:
        if i.name == player_name:
            passing_decoded = jsonDec.decode(i.passing_career)
            rushing_decoded = jsonDec.decode(i.rushing_career)
            receiving_decoded = jsonDec.decode(i.receiving_career)
            defensive_decoded = jsonDec.decode(i.defensive_career)
            scoring_decoded = jsonDec.decode(i.scoring_career)
            i.created_date = timezone.now()
            i.count += 1
            i.save()
    return passing_decoded, rushing_decoded, receiving_decoded, scoring_decoded, defensive_decoded


#checks if player exists and returns name in searchable format
def clean_player_name(request, player_name):
    try:
        player_name  = request.GET.get('player_name')
        player_name = player_name.split()[0].capitalize() + " " + player_name.split()[1].capitalize()
        return player_name
    except:
        return render(request, "notFound.html")
    
def check_for_player(all_players, player_name):
    already_exists = False
    for i in all_players:
        if i.name == player_name:
            already_exists = True
    return already_exists

def retrieve_stats(request, player_name):
    player_name = clean_player_name(request, player_name)
    all_players = Player.objects.all()
    jsonDec = json.decoder.JSONDecoder()
    already_exists = check_for_player(all_players, player_name)
    if already_exists == False: 
        try:
            player_id = get_player_id(player_name)
            get_player_data(player_id)
            stats = load_player(player_name)
            a = Player(name = player_name, passing_career = json.dumps(stats[0]), rushing_career = json.dumps(stats[1]), receiving_career = json.dumps(stats[2]), defensive_career = json.dumps(stats[4]), scoring_career = json.dumps(stats[3]), position = stats[5], last_team = stats[6])
            a.save()
        except:
            return render(request, "notFound.html")
    else:
        stats = pull_player(player_name)
    return stats

def get_last_team(team_data):
    last_team_split = team_data.split('-')
    last_team = ""
    for i in last_team_split:
        last_team += i.capitalize() + " "
    return last_team