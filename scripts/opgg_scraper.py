from time import sleep
from json import loads, dumps
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from pandas import json_normalize
from requests import Session
from pathlib import Path

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
        options.set_capability('goog:loggingPrefs', {"performance": "ALL", "browser": "ALL"})

        service = ChromeService(ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=1)).install())

        driver = webdriver.Chrome(service=service, options=options)
        return driver

summoner = sys.argv[1]
tagline = sys.argv[2]
season = sys.argv[3]
op_gg_summoner_profile_url = f"https://www.op.gg/summoners/na/{summoner}-{tagline}/champions"
try:
    with WebDriverManager() as driver:
        driver.get(op_gg_summoner_profile_url)
        sleep(10)
        logs = driver.get_log("performance")

    parsed_logs = [loads(log['message']) for log in logs]
    for log, parsed in zip(logs, parsed_logs):
        parsed['level'] = log['level']
        parsed['timestamp'] = log['timestamp']

    df = json_normalize(parsed_logs)
    domain = 'lol-web-api.op.gg'
    df = df[df['message.params.response.url'].fillna('').str.contains(domain)]

    pattern = r'https:\/\/lol-web-api\.op\.gg\/api\/v1\.0\/internal\/bypass\/summoners\/na\/([^\/]+)\/most-champions\/rank\?game_type=RANKED&season_id=27'
    df.loc[:, 'api_summoner_id'] = df['message.params.response.url'].str.extract(pattern)

    assert df['api_summoner_id'].nunique() == 1

    summoner_id = df[df['api_summoner_id'].notna()].iloc[0,-1]

    directory_path = Path(f'../data/{summoner}')
    directory_path.mkdir(parents=True, exist_ok=True)

    output_file = f"../data/{summoner}/{summoner}_{season}_opgg.json"
    base_url = "https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/na/"
    endpoint = f"/most-champions/rank?game_type=RANKED&season_id={season}"
    full_url = base_url + summoner_id + endpoint

    with Session() as session:
        response = session.get(full_url)

    if response.ok:
        data = response.json()
        with open(output_file, 'w') as f:
            f.write(dumps(data, indent=4))
        print("Data saved to", output_file)
        sys.exit(0)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        sys.exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

finally:
    if 'driver' in locals() and driver:
        driver.quit()
