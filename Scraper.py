from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()

driver.get("https://www.op.gg/summoners/na/Fire-2842")

title = driver.title

driver.implicitly_wait(0.5)

searchbox = driver.find_element(by=By.ID, value="search")
message.value = "fire#2842"
button = driver.find_element(by=by.ID, value="gg-btn")
message = driver.find_element(by=By.ID, value="__NEXT_DATA__")
text = message.text

time.sleep(10)
driver.quit()