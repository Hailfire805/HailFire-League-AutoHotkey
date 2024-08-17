import json
import os
import sys
import math


def update_or_add_data(data_dict, new_data):
    for key, new_values in new_data.items():
        if key in data_dict:
            for sub_key, new_value in new_values.items():
                if sub_key in data_dict[key]:
                    data_dict[key][sub_key] += new_value
                else:
                    data_dict[key][sub_key] = new_value
        else:
            data_dict[key] = new_values


def convert_to_ks(val):
    if val > 1000:
        return f"{round(val / 1000,1)}k"
    else:
        return val


# Replace With Desired Summoner or Run Script With Summoner As Arg 1
summoner = sys.argv[1] if sys.argv.__len__() > 1 else "Fire"
# Load the JSON data For Seasons
print("Loading Season Data")
try:
    with open('../src/seasons.json', 'r', encoding='utf-8') as file:
        season_data = json.load(file)['seasons']
except FileNotFoundError:
    print("Season data file not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error decoding the season data JSON.")
    sys.exit(1)
# Load the JSON data for champion IDs
print("Loading Champion Data")
try:
    with open('../src/Champion_Ids.json', 'r', encoding='utf-8') as file:
        champion_ids = json.load(file)
except FileNotFoundError:
    print("Champion IDs data file not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error decoding the champion IDs JSON.")
    sys.exit(1)

# Create a mapping of season numbers to season names
season_map = {value['Number']: key for key,
              value in season_data.items() if 'Number' in value}

# Create a mapping of champion IDs to champion names
champion_map = {str(value): key for key, value in champion_ids.items()}

# Define the output JSON file path
output_file_path = f'../data/{summoner}/{summoner}_Season_Stats.json'
if os.path.exists(output_file_path):
    try:
        with open(output_file_path, 'r', encoding='utf-8') as file:
            all_seasons_data = json.load(file)
            all_seasons_data.clear()
            all_seasons_data['Total Stats'] = {}
    except (FileNotFoundError, json.JSONDecodeError):
        all_seasons_data = {}
else:
    all_seasons_data = {
        "Total Stats": {

        }
    }
# For Each Season Parse Champion Stat Data
for season_num, season_name in season_map.items():
    try:

        # Construct the file path for the current season's data
        season_file_path: str = f'../data/{summoner}/{summoner}_{season_num}_opgg.json'
        # Check if the file exists
        if not os.path.exists(season_file_path):
            continue

        # Load Champion Stat Data For Season
        with open(season_file_path, 'r', encoding='utf-8') as file:
            champion_stats = json.load(file)

            # Ensure the structure and key presence
            if 'data' in champion_stats and 'season_id' in champion_stats['data']:
                season_id = champion_stats['data']['season_id']
            else:
                continue

            # Initialize season_data for the current season
            season_data = {}
            # Extract champion stats and format the output
            # If Season Is 2023 S1 Or Later Parse Advanced Data
            if season_id >= 23:
                # For Each Champion Parse Stat Data
                for champ in champion_stats['data']['champion_stats']:
                    champion_name = champion_map.get(
                        str(champ['id']), f"Champion ID {champ['id']}")
                    wins = champ['win']
                    losses = champ['lose']
                    games = wins + losses
                    winrate = round((wins / games) *
                                    100 if wins + losses > 0 else 0, 2)
                    avg_game_length = f"{str(math.floor(champ['game_length_second'] / games // 60))} Minutes {champ['game_length_second'] % 60} Seconds"

                    avg_kills = round((round((champ['kill'] / games), 2)), 2)
                    avg_deaths = round((champ['death'] / games), 2)
                    avg_assists = round((champ['assist'] / games), 2)
                    kda = round((champ['kill'] + champ['assist']) /
                                champ['death'] if champ['death'] > 0 else 1, 2)

                    max_op_score = champ['is_max_in_team_op_score']
                    avg_op_score = round((champ['op_score'] / games), 2)
                    avg_cc_score = round(
                        (champ['time_ccing_others'] / games), 2)
                    mvp_rate = round((max_op_score / games), 2)*100

                    avg_dmg_dealt_total = round(
                        (champ['damage_dealt'] / games), 2)
                    avg_phy_dmg_dealt_total = round(
                        (champ['physical_damage_dealt'] / games), 2)
                    avg_mag_dmg_dealt_total = round(
                        (champ['magic_damage_dealt'] / games), 2)
                    avg_true_dmg_dealt_total = round(avg_dmg_dealt_total - (avg_phy_dmg_dealt_total + avg_mag_dmg_dealt_total)
                                                     if champ['magic_damage_dealt'] > 0 else avg_dmg_dealt_total - avg_phy_dmg_dealt_total, 2)
                    avg_dmg_dealt_to_objectives = round(
                        (champ['damage_dealt_to_objectives'] / games), 2)
                    avg_dmg_dealt_to_turrets = round(
                        (champ['damage_dealt_to_turrets'] / games), 2)
                    avg_dmg_healed = round((champ['heal'] / games), 2)
                    avg_dmg_taken_total = round(
                        (champ['damage_taken'] / games), 2)
                    avg_dmg_self_mitigated = round(
                        (champ['damage_self_mitigated'] / games), 2)
                    avg_dmg_to_champ = round(
                        (champ['damage_dealt_to_champions'] / games), 2)
                    avg_phy_dmg_to_champ = round(
                        (champ['physical_damage_dealt_to_champions'] / games), 2)
                    avg_mag_dmg_to_champ = round(
                        champ['magic_damage_dealt_to_champions'] / games if champ['magic_damage_dealt_to_champions'] > 0 else 0, 2)
                    avg_true_dmg_to_champ = round((avg_dmg_to_champ - (avg_phy_dmg_to_champ + avg_mag_dmg_to_champ))
                                                  if champ['magic_damage_dealt_to_champions'] > 0 else avg_dmg_to_champ - avg_phy_dmg_to_champ, 2)

                    avg_gold_earned = round((champ['gold_earned'] / games), 2)
                    avg_minion_kills = round((champ['minion_kill'] / games), 2)
                    avg_monster_kills = round(
                        (champ['neutral_minion_kill'] / games), 2)
                    avg_turret_kills = round((champ['turret_kill'] / games), 2)
                    avg_inhibitor_kills = round(
                        (champ['inhibitor_kills'] / games), 2)

                    avg_vision_score = round(
                        (champ['vision_score'] / games), 2)
                    avg_control_wards = round(
                        (champ['vision_wards_bought_in_game'] / games), 2)
                    avg_wards_placed = round(
                        (champ['wards_placed'] / games), 2)
                    avg_wards_cleared = round(
                        (champ['wards_killed'] / games), 2)

                    double_kills = champ['double_kill']
                    triple_kills = champ['triple_kill']
                    quadra_kills = champ['quadra_kill']
                    penta_kills = champ['penta_kill']

                    double_kills_per_game = round(
                        (champ['double_kill'] / games), 2)
                    triple_kills_per_game = round(
                        (champ['triple_kill'] / games), 2)
                    quadra_kills_per_game = round(
                        (champ['quadra_kill'] / games), 2)
                    penta_kills_per_game = round(
                        (champ['penta_kill'] / games), 2)

                    season_data[champion_name] = {
                        "Meta-Performance Stats": {
                            "Games Played": games,
                            "Total Wins": wins,
                            "Total Losses": losses,
                            "Winrate": f"{winrate}%",
                            "Average OP Score (O to 10)": avg_op_score,
                            "Ace/MVP Games": max_op_score,
                            "Ace/MVP Rate": f"{mvp_rate}%",
                            "Average Game Length": avg_game_length
                        },
                        "Combat & Damage Stats": {
                            "Takedowns & MultiKills": {
                                "Average Kills": avg_kills,
                                "Average Deaths": avg_deaths,
                                "Average Assists": avg_assists,
                                "KDA": kda,
                                "Total Double Kills": double_kills,
                                "Double Kills Per Game": double_kills_per_game,
                                "Total Triple Kills": triple_kills,
                                "Triple Kills Per Game": triple_kills_per_game,
                                "Total Quadra Kills": quadra_kills,
                                "Quadra Kills Per Game": quadra_kills_per_game,
                                "Total Penta Kills": penta_kills,
                                "Penta Kills Per Game": penta_kills_per_game,
                            },
                            "Per Game Average Including Versus Non-Champions": {
                                "Total Damage Dealt": convert_to_ks(avg_dmg_dealt_total),
                                "Physical Damage Dealt": convert_to_ks(avg_phy_dmg_dealt_total),
                                "Magic Damage Dealt": convert_to_ks(avg_mag_dmg_dealt_total),
                                "True Damage Dealt": convert_to_ks(avg_true_dmg_dealt_total),
                                "Damage Taken": convert_to_ks(avg_dmg_taken_total),
                                "Damage Healed": convert_to_ks(avg_dmg_healed),
                                "Damage Mitigated": convert_to_ks(avg_dmg_self_mitigated)
                            },
                            "Per Game Average Versus Only Champions": {
                                "Total Damage To Champions": convert_to_ks(avg_dmg_to_champ),
                                "Physical Damage To Champions": convert_to_ks(avg_phy_dmg_to_champ),
                                "Magic Damage To Champions": convert_to_ks(avg_mag_dmg_to_champ),
                                "True Damage To Champions": convert_to_ks(avg_true_dmg_to_champ),
                                "Crowd Control Score": avg_cc_score
                            }
                        },
                        "Per Game Average Income & Objective Stats": {
                            "Gold Earned": convert_to_ks(avg_gold_earned),
                            "Minion Kills": avg_minion_kills,
                            "Monster Kills": avg_monster_kills,
                            "Turret Kills": avg_turret_kills,
                            "Inhibitor Kills": avg_inhibitor_kills,
                            "Total Damage To Turrets": convert_to_ks(avg_dmg_dealt_to_turrets),
                            "Total Damage To Objectives": convert_to_ks(avg_dmg_dealt_to_objectives)
                        },
                        "Per Game Average Vision Stats": {
                            "Vision Score": avg_vision_score,
                            "Control Wards Placed": avg_control_wards,
                            "Wards Placed": avg_wards_placed,
                            "Wards Cleared": avg_wards_cleared

                        }
                    }
                    print(f"{champion_name}, {season_name} Processed")
                    # If champion is not yet in total data
                    if all_seasons_data['Total Stats'].get(champion_name, "new") == "new":
                        current_champ = {
                            "Meta-Performance Stats": {
                                "Games Played": games,
                                "Total Wins": wins,
                                "Total Losses": losses,
                                "Winrate": winrate,
                                "Average OP Score (O to 10)": round((champ['op_score'] / games), 2),
                                "Ace/MVP Games": max_op_score,
                                "Ace/MVP Rate": mvp_rate,
                                "Average Game Length": champ['game_length_second']
                            },
                            "Combat & Damage Stats": {
                                "Takedowns & MultiKills": {
                                    "Average Kills": avg_kills,
                                    "Average Deaths": avg_deaths,
                                    "Average Assists": avg_assists,
                                    "KDA": kda,
                                    "Total Double Kills": double_kills,
                                    "Double Kills Per Game": double_kills_per_game,
                                    "Total Triple Kills": triple_kills,
                                    "Triple Kills Per Game": triple_kills_per_game,
                                    "Total Quadra Kills": quadra_kills,
                                    "Quadra Kills Per Game": quadra_kills_per_game,
                                    "Total Penta Kills": penta_kills,
                                    "Penta Kills Per Game": penta_kills_per_game,
                                },
                                "Per Game Average Including Versus Non-Champions": {
                                    "Total Damage Dealt": avg_dmg_dealt_total,
                                    "Physical Damage Dealt": avg_phy_dmg_dealt_total,
                                    "Magic Damage Dealt": avg_mag_dmg_dealt_total,
                                    "True Damage Dealt": avg_true_dmg_dealt_total,
                                    "Damage Taken": avg_dmg_taken_total,
                                    "Damage Healed": avg_dmg_healed,
                                    "Damage Mitigated": avg_dmg_self_mitigated
                                },
                                "Per Game Average Versus Only Champions": {
                                    "Total Damage To Champions": avg_dmg_to_champ,
                                    "Physical Damage To Champions": avg_phy_dmg_to_champ,
                                    "Magic Damage To Champions": avg_mag_dmg_to_champ,
                                    "True Damage To Champions": avg_true_dmg_to_champ,
                                    "Crowd Control Score": avg_cc_score
                                }
                            },
                            "Per Game Average Income & Objective Stats": {
                                "Gold Earned": avg_gold_earned,
                                "Minion Kills": avg_minion_kills,
                                "Monster Kills": avg_monster_kills,
                                "Turret Kills": avg_turret_kills,
                                "Inhibitor Kills": avg_inhibitor_kills,
                                "Total Damage To Turrets": avg_dmg_dealt_to_turrets,
                                "Total Damage To Objectives": avg_dmg_dealt_to_objectives
                            },
                            "Per Game Average Vision Stats": {
                                "Vision Score": avg_vision_score,
                                "Control Wards Placed": avg_control_wards,
                                "Wards Placed": avg_wards_placed,
                                "Wards Cleared": avg_wards_cleared
                            }
                        }
                        print(f"{champion_name} Created")
                        all_seasons_data['Total Stats'][champion_name] = current_champ
                    # If champion does exist in total data
                    else:
                        current = all_seasons_data['Total Stats'][champion_name]
                        meta = current['Meta-Performance Stats']
                        takedowns = current["Combat & Damage Stats"]['Takedowns & MultiKills']
                        alldmg = current["Combat & Damage Stats"]["Per Game Average Including Versus Non-Champions"]
                        vschamps = current["Combat & Damage Stats"]["Per Game Average Versus Only Champions"]
                        income = current['Per Game Average Income & Objective Stats']
                        vision = current["Per Game Average Vision Stats"]
                        meta['Games Played'] += games
                        oldgames = meta['Games Played'] - games
                        meta["Total Wins"] += wins
                        meta["Total Losses"] += losses
                        meta["Winrate"] = round(meta["Total Wins"] /
                                                meta['Games Played'] *
                                                100 if meta["Total Wins"] > 0 else 0, 2)
                        meta["Average OP Score (O to 10)"] = round(
                            ((oldgames) * meta['Average OP Score (O to 10)'] + champ['op_score']) / meta['Games Played'], 2)
                        meta["Ace/MVP Games"] += max_op_score
                        meta["Ace/MVP Rate"] = round(meta["Ace/MVP Games"] /
                                                     meta['Games Played'] * 100, 2)
                        meta["Average Game Length"] += champ['game_length_second']
                        takedowns["Average Kills"] = round((
                            oldgames * takedowns["Average Kills"] + champ['kill']) / meta['Games Played'], 2)
                        takedowns["Average Deaths"] = round((
                            oldgames * takedowns["Average Deaths"] + champ['death']) / meta['Games Played'], 2)
                        takedowns["Average Assists"] = round((
                            oldgames * takedowns["Average Assists"] + champ['assist']) / meta['Games Played'], 2)
                        takedowns["KDA"] = round((
                            takedowns["Average Kills"] + takedowns["Average Assists"]) / takedowns["Average Deaths"], 2)
                        takedowns["Total Double Kills"] += double_kills
                        takedowns["Double Kills Per Game"] = round(takedowns["Total Double Kills"] /
                                                                   meta['Games Played'], 2)
                        takedowns["Total Triple Kills"] += triple_kills
                        takedowns["Triple Kills Per Game"] = round(takedowns["Total Triple Kills"] /
                                                                   meta['Games Played'], 2)
                        takedowns["Total Quadra Kills"] += quadra_kills
                        takedowns["Quadra Kills Per Game"] = round(takedowns["Total Quadra Kills"] /
                                                                   meta['Games Played'], 2)
                        takedowns["Total Penta Kills"] += penta_kills
                        takedowns["Penta Kills Per Game"] = round(takedowns["Total Penta Kills"] /
                                                                  meta['Games Played'], 2)
                        alldmg["Total Damage Dealt"] = round((
                            oldgames * alldmg['Total Damage Dealt'] + (avg_dmg_dealt_total * games)) / meta['Games Played'], 2)
                        alldmg["Physical Damage Dealt"] = round((
                            oldgames * alldmg['Physical Damage Dealt'] + (avg_phy_dmg_dealt_total * games)) / meta['Games Played'], 2)
                        alldmg["Magic Damage Dealt"] = round((
                            oldgames * alldmg['Magic Damage Dealt'] + (avg_mag_dmg_dealt_total * games)) / meta['Games Played'], 2)
                        alldmg["True Damage Dealt"] = round((
                            oldgames * alldmg['True Damage Dealt'] + (avg_true_dmg_dealt_total * games)) / meta['Games Played'], 2)
                        alldmg["Damage Taken"] = round((
                            oldgames * alldmg['Damage Taken'] + (avg_dmg_taken_total * games)) / meta['Games Played'], 2)
                        alldmg["Damage Healed"] = round((
                            oldgames * alldmg['Damage Healed'] + champ['heal']) / meta['Games Played'], 2)
                        alldmg["Damage Mitigated"] = round((
                            oldgames * alldmg['Damage Mitigated'] + champ['damage_self_mitigated']) / meta['Games Played'], 2)
                        vschamps["Total Damage To Champions"] = round((
                            oldgames * vschamps['Total Damage To Champions'] + (avg_dmg_to_champ * games)) / meta['Games Played'], 2)
                        vschamps["Physical Damage To Champions"] = round((
                            oldgames * vschamps['Total Damage To Champions'] + (avg_phy_dmg_to_champ * games)) / meta['Games Played'], 2)
                        vschamps["Magic Damage To Champions"] = round((
                            oldgames * vschamps["Magic Damage To Champions"] + (avg_mag_dmg_to_champ * games)) / meta['Games Played'], 2)
                        vschamps["True Damage To Champions"] = round((
                            oldgames * vschamps["True Damage To Champions"] + (avg_true_dmg_to_champ * games)) / meta['Games Played'], 2)
                        vschamps["Crowd Control Score"] = round((
                            oldgames * vschamps["Crowd Control Score"] + (avg_cc_score * games)) / meta['Games Played'], 2)
                        income["Gold Earned"] = round((
                            oldgames * income["Gold Earned"] + (avg_gold_earned * games)) / meta['Games Played'], 2)
                        income["Minion Kills"] = round((
                            oldgames * income["Minion Kills"] + (avg_minion_kills * games)) / meta['Games Played'], 2)
                        income["Monster Kills"] = round((
                            oldgames * income["Monster Kills"] + (avg_monster_kills * games)) / meta['Games Played'], 2)
                        income["Turret Kills"] = round((
                            oldgames * income["Turret Kills"] + (avg_turret_kills * games)) / meta['Games Played'], 2)
                        income["Inhibitor Kills"] = round((
                            oldgames * income["Inhibitor Kills"] + (avg_inhibitor_kills * games)) / meta['Games Played'], 2)
                        income["Total Damage To Turrets"] = round((oldgames * income["Total Damage To Turrets"] + (
                            avg_dmg_dealt_to_turrets * games)) / meta['Games Played'], 2)
                        income["Total Damage To Objectives"] = round((oldgames * income["Total Damage To Objectives"] + (
                            avg_dmg_dealt_to_objectives * games)) / meta['Games Played'], 2)
                        vision["Vision Score"] = round((
                            oldgames * vision["Vision Score"] + (avg_vision_score * games)) / meta['Games Played'], 2)
                        vision["Control Wards Placed"] = round((
                            oldgames * vision["Control Wards Placed"] + (avg_control_wards * games)) / meta['Games Played'], 2)
                        vision["Wards Placed"] = round((
                            oldgames * vision["Wards Placed"] + (avg_wards_placed * games)) / meta['Games Played'], 2)
                        vision["Wards Cleared"] = round((
                            oldgames * vision["Wards Cleared"] + (avg_wards_cleared * games)) / meta['Games Played'], 2)

                        print(f"{champion_name} Updated")
                        # If Earlier Than 2023 S1 Parse Basic Data
            else:
                for champ in champion_stats['data']['champion_stats']:
                    champion_name = champion_map.get(
                        str(champ['id']), f"Champion ID {champ['id']}")
                    wins = champ['win']
                    losses = champ['lose']
                    games = wins + losses
                    winrate = f"{round((wins / games) * 100 if wins + losses > 0 else 0,2)}%"
                    avg_game_length = f"{str(math.floor(champ['game_length_second'] / games // 60))} Minutes {champ['game_length_second'] % 60} Seconds" if champ['game_length_second'] != None else "N/A"

                    avg_kills = round((round((champ['kill'] / games), 2)), 2)
                    avg_deaths = round((champ['death'] / games), 2)
                    avg_assists = round((champ['assist'] / games), 2)
                    kda = round((champ['kill'] + champ['assist']) /
                                champ['death'] if champ['death'] > 0 else 1, 2)

                    double_kills = champ['double_kill']
                    triple_kills = champ['triple_kill']
                    quadra_kills = champ['quadra_kill']
                    penta_kills = champ['penta_kill']

                    double_kills_per_game = round(
                        (champ['double_kill'] / games), 2)
                    triple_kills_per_game = round(
                        (champ['triple_kill'] / games), 2)
                    quadra_kills_per_game = round(
                        (champ['quadra_kill'] / games), 2)
                    penta_kills_per_game = round(
                        (champ['penta_kill'] / games), 2)

                    avg_gold_earned = round((champ['gold_earned'] / games), 2)
                    avg_minion_kills = round((champ['minion_kill'] / games), 2)
                    avg_monster_kills = round(
                        (champ['neutral_minion_kill'] / games), 2)
                    avg_turret_kills = round((champ['turret_kill'] / games), 2)

                    avg_dmg_taken_total = round(
                        (champ['damage_taken'] / games), 2)
                    avg_dmg_dealt_total = round(
                        (champ['damage_dealt'] / games), 2)
                    avg_phy_dmg_dealt_total = round(
                        (champ['physical_damage_dealt'] / games), 2)
                    avg_mag_dmg_dealt_total = round(
                        (champ['magic_damage_dealt'] / games) if champ['magic_damage_dealt'] > 0 else 0, 2)
                    avg_true_dmg_dealt_total = round(avg_dmg_dealt_total - (avg_phy_dmg_dealt_total + avg_mag_dmg_dealt_total)
                                                     if champ['magic_damage_dealt'] > 0 else avg_dmg_dealt_total - avg_phy_dmg_dealt_total, 2)

                    season_data[champion_name] = {
                        "Meta-Performance Stats": {
                            "Games Played": games,
                            "Total Wins": wins,
                            "Total Losses": losses,
                            "Winrate": winrate,
                            "Average Game Length": avg_game_length
                        },
                        "Per Game Average Income & Objective Stats": {
                            "Gold Earned": convert_to_ks(avg_gold_earned),
                            "Minion Kills": avg_minion_kills,
                            "Monster Kills": avg_monster_kills,
                            "Turret Kills": avg_turret_kills,
                        },
                        "Combat & Damage Stats": {
                            "Takedowns & MultiKills": {
                                "Average Kills": avg_kills,
                                "Average Deaths": avg_deaths,
                                "Average Assists": avg_assists,
                                "KDA": kda,
                                "Total Double Kills": double_kills,
                                "Double Kills Per Game": double_kills_per_game,
                                "Total Triple Kills": triple_kills,
                                "Triple Kills Per Game": triple_kills_per_game,
                                "Total Quadra Kills": quadra_kills,
                                "Quadra Kills Per Game": quadra_kills_per_game,
                                "Total Penta Kills": penta_kills,
                                "Penta Kills Per Game": penta_kills_per_game,
                            },
                            "Per Game Average Including Versus Non-Champions": {
                                "Total Damage Dealt": convert_to_ks(avg_dmg_dealt_total),
                                "Physical Damage Dealt": convert_to_ks(avg_phy_dmg_dealt_total),
                                "Magic Damage Dealt": convert_to_ks(avg_mag_dmg_dealt_total),
                                "True Damage Dealt": convert_to_ks(avg_true_dmg_dealt_total),
                                "Damage Taken": convert_to_ks(avg_dmg_taken_total),
                            }
                        }
                    }
                    print(f"{champion_name}, {season_name} Processed")
            # Add Parsed Champion Data To Season Data
            all_seasons_data[season_name] = season_data
            # Save the updated data back to the JSON file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(all_seasons_data, output_file,
                          indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"An error occurred: {e.args}")
        continue


total_champ_names = list(all_seasons_data['Total Stats'].keys())
for name in total_champ_names:
    all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Average Game Length'] = f"{str(math.floor(all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Average Game Length'] / all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Games Played'] // 60))} Minutes {all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Average Game Length'] % 60} Seconds"
    all_seasons_data['Total Stats'][name]['Meta-Performance Stats'][
        'Ace/MVP Rate'] = f"{str(all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Ace/MVP Rate'])}%"
    all_seasons_data['Total Stats'][name]['Meta-Performance Stats'][
        'Winrate'] = f"{str(all_seasons_data['Total Stats'][name]['Meta-Performance Stats']['Winrate'])}%"
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(all_seasons_data, output_file,
              indent=4, ensure_ascii=False)
