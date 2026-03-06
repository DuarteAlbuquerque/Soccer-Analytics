import json
import os
import pandas as pd

#March 12 (required): one elementary data analysis.

#find event data for the eight league-phase matches of your team in statsbomb/league_phase.zip (e.g., using the list of matches.csv)
#count all passes (.type.id==30, see documentation) your team played in these matches
#place a section on your group wiki page (e.g., PAF AD) in which you report the result and describe how you obtained it

file = '/Users/duartealbuquerque/Desktop/ETH-Switzerland/ETH_Classes/S26/Soccer Analytics/Data/league_phase'
matches_csv = pd.read_csv('/Users/duartealbuquerque/Desktop/ETH-Switzerland/ETH_Classes/S26/Soccer Analytics/Data/matches.csv')
team_name = "Arsenal"
event = 30

def get_games(team_name):
    game_ids = {}
    mask = (matches_csv['home'] == team_name) | (matches_csv['away'] == team_name)

    matches_subset = matches_csv[mask]

    for index, match in matches_subset.iterrows():
        game_ids[os.path.join(file, (str(match["statsbomb"]) + ".json"))] = match

    return game_ids

games = get_games(team_name)

def count_event(game_ids, team_name, event_id):
    total_count = 0
    games_count = {}
    for game in game_ids:
        matchup = game_ids[game]["home"] + " versus " + game_ids[game]["away"]
        games_count[matchup] = 0

        with open(game, 'r', encoding='utf-8') as f:
            events = json.load(f)

        for e in events:
            if e['type']['id'] == event_id:
                if e['possession_team']['name'] == team_name:
                    total_count += 1
                    games_count[matchup] += 1
    return total_count, games_count

print(count_event(games, team_name, event))


            
        





