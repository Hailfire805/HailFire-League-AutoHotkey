import json
import os
import sys
from typing import final
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from pandas import json_normalize
from requests import Session
from pathlib import Path
from time import sleep


class WebDriverManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        self.driver = self.setup_headless_chrome()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    @staticmethod
    def setup_headless_chrome():
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-software-rasterizer")
        options.set_capability('goog:loggingPrefs', {
                               "performance": "ALL", "browser": "ALL"})

        service = ChromeService(ChromeDriverManager(
            cache_manager=DriverCacheManager(valid_range=1)).install())

        driver = webdriver.Chrome(service=service, options=options)
        return driver


# For testing, use a predefined summoner name
summoner = "Fire"
tagline = 2842
# Load the JSON data for seasons
print("Loading Seasons")
try:
    with open('./src/seasons.json', 'r', encoding='utf-8') as file:
        season_data = json.load(file)['seasons']
except FileNotFoundError:
    print("Season data file not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error decoding the season data JSON.")
    sys.exit(1)


print("Creating Mapping")
# Create a mapping of season numbers to season names
season_map = {value['Number']: key for key,
              value in season_data.items() if 'Number' in value}

# Create a mapping of champion IDs to champion names
champion_map = {str(value): key for key, value in champion_ids.items()}

# Define the output JSON file path
output_file_path = f'./data/{summoner}/{summoner}_Season_Stats.json'
if os.path.exists(output_file_path):
    try:
        with open(output_file_path, 'r', encoding='utf-8') as file:
            all_seasons_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_seasons_data = {}
else:
    all_seasons_data = {}

# Process each possible season
for season_num, season_name in season_map.items():
    print(f"Processing season: {season_name}")

    try:
        season = season_num
        op_gg_summoner_profile_url = f"https://www.op.gg/summoners/na/{summoner}-{tagline}/champions"
        with WebDriverManager() as driver:
            driver.get(op_gg_summoner_profile_url)
            sleep(10)
            logs = driver.get_log("performance")

        parsed_logs = [json.loads(log['message']) for log in logs]
        for log, parsed in zip(logs, parsed_logs):
            parsed['level'] = log['level']
            parsed['timestamp'] = log['timestamp']

        df = json_normalize(parsed_logs)
        domain = 'lol-web-api.op.gg'
        df = df[df['message.params.response.url'].fillna(
            '').str.contains(domain)]

        pattern = r'https:\/\/lol-web-api\.op\.gg\/api\/v1\.0\/internal\/bypass\/summoners\/na\/([^\/]+)\/most-champions\/rank\?game_type=RANKED&season_id=27'
        df.loc[:, 'api_summoner_id'] = df['message.params.response.url'].str.extract(
            pattern)

        assert df['api_summoner_id'].nunique() == 1

        summoner_id = df[df['api_summoner_id'].notna()].iloc[0, -1]

        directory_path = Path(f'./data/{summoner}')
        directory_path.mkdir(parents=True, exist_ok=True)

        output_file = f"./data/{summoner}/{summoner}_{season}_opgg.json"
        base_url = "https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/na/"
        endpoint = f"/most-champions/rank?game_type=RANKED&season_id={season}"
        full_url = f"{base_url}{summoner_id}{endpoint}"

        with Session() as session:
            response = session.get(full_url)

            if response.ok:
                data = response.json()
                with open(output_file, 'w') as f:
                    f.write(json.dumps(data, indent=4))
                print("Data saved to", output_file)
                if 'driver' in locals() and driver:
                    driver.quit()
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
