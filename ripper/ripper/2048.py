from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random 

browser = webdriver.Firefox()
print(type(browser))

URL_MAIN = "https://www.2048.org/"

browser.get(URL_MAIN)

# def move_left()
# def move_right()
# def move_up()
# def move_down()

# game_elem = browser.find_element(By.CLASS_NAME, "game-container")
actions = ActionChains(browser)
x = 0
y = 100000
while(x < y):
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
    time.sleep(0.1)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    time.sleep(0.1)
    actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    time.sleep(0.1)
    actions.send_keys(Keys.ARROW_LEFT)
    actions.perform()
    time.sleep(0.1)
    
    x += 1
# input_field = driver.find_element(".game-container", "input[type='text']")