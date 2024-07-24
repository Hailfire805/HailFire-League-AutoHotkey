import json
import os
import sys

summoner = sys.argv[1]
season = sys.argv[2]
# Load the JSON data
with open('../src/seasons.json', 'r', encoding='utf-8') as file:
    season_numbers = json.load(file)

with open('../src/Champion_Ids.json', 'r', encoding='utf-8') as file:
    champion_ids = json.load(file)

with open(f'../data/{summoner}/{summoner}_{season}_opgg.json', 'r', encoding='utf-8') as file:
    champion_stats = json.load(file)

# Define the output JSON file path
output_file_path = f'../data/{summoner}/{summoner}_Season_Stats.json'

# Create a mapping of season numbers to season names
season_map = {value['Number']: key for key, value in season_numbers.items()}

# Create a mapping of champion IDs to champion names
champion_map = {str(value): key for key, value in champion_ids.items()}

# Extract season information
season_id = champion_stats['data']['season_id']
season_name = season_map.get(season_id, f"Season {season_id}")

# Initialize or load existing data
if os.path.exists(output_file_path):
    with open(output_file_path, 'r', encoding='utf-8') as file:
        all_seasons_data = json.load(file)
else:
    all_seasons_data = {}

# Extract champion stats and format the output
season_data = {}
for champ in champion_stats['data']['champion_stats']:
    champion_name = champion_map.get(str(champ['id']), f"Champion ID {champ['id']}")
    wins = champ['win']
    losses = champ['lose']
    op_score = champ['op_score']
    max_op_score = champ['is_max_in_team_op_score']
    vision_score = champ['vision_score']
    turret_kill = champ['turret_kill']
    minion_kill = champ['minion_kill']
    if wins != 0:
        winrate = (wins / (wins + losses)) * 100
    else:
        winrate = 0
    season_data[champion_name] = {
        "Wins": wins,
        "Losses": losses,
        "Winrate": winrate
    }

# Update the season data
all_seasons_data[season_name] = season_data

# Save the updated data back to the JSON file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(all_seasons_data, output_file, indent=4, ensure_ascii=False)

print(f"Data for {season_name} has been saved to {output_file_path}")
