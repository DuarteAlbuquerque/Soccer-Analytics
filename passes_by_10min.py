import json
import os
from collections import defaultdict

import pandas as pd

base = "uefa-cl-2025-2026/data/statsbomb/league_phase"
matches_csv = pd.read_csv("uefa-cl-2025-2026/data/matches.csv")
team_name = "Arsenal"


def get_games(team):
    game_ids = {}
    mask = (matches_csv["home"] == team) | (matches_csv["away"] == team)
    matches_subset = matches_csv[mask]
    for _, match in matches_subset.iterrows():
        game_ids[os.path.join(base, f'{match["statsbomb"]}.json')] = match
    return game_ids


def passes_by_10min(game_ids, team):
    bins = [f"{i:02d}-{i+9:02d}" for i in range(0, 90, 10)] + ["90+"]
    agg = defaultdict(int)

    for game_path in game_ids:
        with open(game_path, "r", encoding="utf-8") as f:
            events = json.load(f)

        for e in events:
            if e.get("type", {}).get("id") == 30 and e.get("possession_team", {}).get("name") == team:
                minute = e.get("minute", 0)
                b = "90+" if minute >= 90 else f"{(minute // 10) * 10:02d}-{(minute // 10) * 10 + 9:02d}"
                agg[b] += 1

    return bins, agg


if __name__ == "__main__":
    games = get_games(team_name)
    bins, totals = passes_by_10min(games, team_name)
    print(f"{team_name} passes by 10-minute bin (all league-phase matches):")
    for b in bins:
        print(f"{b}: {totals[b]}")
