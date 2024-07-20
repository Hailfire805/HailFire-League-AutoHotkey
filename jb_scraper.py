#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Ensure have venv (e.g. `python -m venv .venv`)
# Ensure venv is activated/sourced (e.g. `.venv/scripts/activate` or `source .venv/bin/activate`)
# Ensure venv has dependencies installed (e.g. `python -m pip install -Uqqr requirements.txt`)
# Ensure notebook is using the venv as a Pythonkernel


# # Attempts

# ## w/ `requests_html` rendering

# In[ ]:


import os

# requests-html and a dependency of it (pyppeteer) are no longer maintained, 
# so need to update env var to fix common issue

# Get latest revision number @ https://chromium.woolyss.com/download/en/#windows
chromium_revision_number = 1330662

# Update environment variable with latest revision number
os.environ['PYPPETEER_CHROMIUM_REVISION'] = str(chromium_revision_number)


# In[ ]:


import nest_asyncio

# Allow nested event loops
nest_asyncio.apply()


# In[ ]:


from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup


# In[ ]:


# NOTE: initial run may download the latest Chromium version

url = "https://www.op.gg/summoners/na/Fire-2842"
asession = AsyncHTMLSession()
try:
    # Navigate to the page and wait for network requests to complete
    r = await asession.get(url)
    await r.html.arender(sleep=10)
finally:
    await asession.close()


# In[ ]:


# Parse HTML from reponse using lxml parser into soup
soup = BeautifulSoup(r.html.raw_html, 'lxml')


# In[ ]:


# Ensure that the response contains the expected rendered HTML


# ## w/ `selenium` rendering

# In[ ]:


import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


# In[ ]:


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
        options.add_argument("--headless=new")
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


# In[ ]:


target_url = "lol-web-api.op.gg/api/v1.0/internal/bypass/games/na/summoners"
op_gg_summoner_profile_url = "https://www.op.gg/summoners/na/Fire-2842"
output_file = "data/output.csv"


# In[ ]:


with WebDriverManager() as driver:
    # Navigate to the page and wait for network requests to complete
    driver.get(op_gg_summoner_profile_url)

    # # Wait for the specific element to load if necessary, helps ensure page is fully loaded
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, '__next'))
    # )

    # Sleep 10 seconds
    time.sleep(10)

    # Get the page source after rendering
    html_content = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'lxml')

# print(soup.prettify()[:1000])


# In[ ]:


# # Capture network logs
# logs = driver.get_log("performance")
# print(f"Captured {len(logs)} performance logs.")  # Debugging: print number of logs captured

# # Extract and parse the JSON from the 'message' key
# parsed_logs = [json.loads(log['message']) for log in logs]
# for log, parsed in zip(logs, parsed_logs):
#     parsed['level'] = log['level']
#     parsed['timestamp'] = log['timestamp']

# df = pd.json_normalize(parsed_logs)

# _ = df[df['message.params.response.url'].fillna('').str.contains('data')]

# with pd.option_context('display.max_rows', None):
#     display(_.T)


# In[ ]:


# base_url = "https://lol-web-api.op.gg/api/v1.0/internal/bypass/summoners/na/"
# endpoint = "/most-champions/rank?game_type=RANKED&season_id=27"
# full_url = base_url + summoner_id + endpoint

# response = requests.get(full_url)

# if response.status_code == 200:
#     data = response.json()
#     df = pd.json_normalize(data)
#     df.to_csv(output_file, index=False)
#     print("Data saved to", output_file)
# else:
#     print(f"Failed to retrieve data: {response.status_code}")


# In[ ]:




