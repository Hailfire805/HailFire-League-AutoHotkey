import json
import csv

# File paths
# Replace with your actual JSON file path
json_file_path = '../data/Fire/Fire_Season_Stats.json'
csv_file_path = '../data/Fire/Fire_Champion_Stats.csv'  # Output CSV file path

# Load JSON data from file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Prepare the CSV headers
headers = [
    "Champion", "Games Played", "Total Wins", "Total Losses", "Winrate",
    "Average OP Score (O to 10)", "Ace/MVP Games", "Ace/MVP Rate",
    "Average Game Length", "Average Kills", "Average Deaths", "Average Assists",
    "KDA", "Total Double Kills", "Double Kills Per Game", "Total Triple Kills",
    "Triple Kills Per Game", "Total Quadra Kills", "Quadra Kills Per Game",
    "Total Penta Kills", "Penta Kills Per Game", "Total Damage Dealt",
    "Physical Damage Dealt", "Magic Damage Dealt", "True Damage Dealt",
    "Damage Taken", "Damage Healed", "Damage Mitigated", "Total Damage To Champions",
    "Physical Damage To Champions", "Magic Damage To Champions",
    "True Damage To Champions", "Crowd Control Score", "Gold Earned",
    "Minion Kills", "Monster Kills", "Turret Kills", "Inhibitor Kills",
    "Total Damage To Turrets", "Total Damage To Objectives", "Vision Score",
    "Control Wards Placed", "Wards Placed", "Wards Cleared"
]

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Write the headers
    writer.writerow(headers)

    # Write the data for each champion
    for champion, stats in data["Total Stats"].items():
        row = [
            champion,
            stats["Meta-Performance Stats"]["Games Played"],
            stats["Meta-Performance Stats"]["Total Wins"],
            stats["Meta-Performance Stats"]["Total Losses"],
            stats["Meta-Performance Stats"]["Winrate"],
            stats["Meta-Performance Stats"]["Average OP Score (O to 10)"],
            stats["Meta-Performance Stats"]["Ace/MVP Games"],
            stats["Meta-Performance Stats"]["Ace/MVP Rate"],
            stats["Meta-Performance Stats"]["Average Game Length"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Average Kills"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Average Deaths"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Average Assists"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["KDA"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Total Double Kills"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Double Kills Per Game"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Total Triple Kills"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Triple Kills Per Game"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Total Quadra Kills"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Quadra Kills Per Game"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Total Penta Kills"],
            stats["Combat & Damage Stats"]["Takedowns & MultiKills"]["Penta Kills Per Game"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Total Damage Dealt"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Physical Damage Dealt"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Magic Damage Dealt"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["True Damage Dealt"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Damage Taken"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Damage Healed"],
            stats["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]["Damage Mitigated"],
            stats["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]["Total Damage To Champions"],
            stats["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]["Physical Damage To Champions"],
            stats["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]["Magic Damage To Champions"],
            stats["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]["True Damage To Champions"],
            stats["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]["Crowd Control Score"],
            stats["Per Game Average Income & Objective Stats"]["Gold Earned"],
            stats["Per Game Average Income & Objective Stats"]["Minion Kills"],
            stats["Per Game Average Income & Objective Stats"]["Monster Kills"],
            stats["Per Game Average Income & Objective Stats"]["Turret Kills"],
            stats["Per Game Average Income & Objective Stats"]["Inhibitor Kills"],
            stats["Per Game Average Income & Objective Stats"]["Total Damage To Turrets"],
            stats["Per Game Average Income & Objective Stats"]["Total Damage To Objectives"],
            stats["Per Game Average Vision Stats"]["Vision Score"],
            stats["Per Game Average Vision Stats"]["Control Wards Placed"],
            stats["Per Game Average Vision Stats"]["Wards Placed"],
            stats["Per Game Average Vision Stats"]["Wards Cleared"]
        ]
        writer.writerow(row)

print(f"Data has been successfully written to {csv_file_path}")
