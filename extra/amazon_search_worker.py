from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import requests
import mysql.connector
import uuid
import re
from bs4 import BeautifulSoup
from rabbit_client import RabbitMQClient
# import request




def random_within_std(mean,std):
    #Generate a random number from a normal distribution
    random_number = random.normalvariate(mean, std)

    # Cap the random number within one standard deviation range
    random_number = max(mean - std, min(mean + std, random_number))
    return random_number

def at_bottom(browser):
    # Get the current scroll position
    current_scroll_position = browser.execute_script("return window.scrollY;")

    # Get the total scroll height of the page
    total_scroll_height = browser.execute_script("return document.body.scrollHeight;")

    # You can adjust the tolerance based on your needs
    tolerance = 0

    # Check if we are close to the bottom within the tolerance
    print("scrollY", browser.execute_script("return window.scrollY;"))
    print("scrollHeight", browser.execute_script("return document.body.scrollHeight;"))
    return current_scroll_position >= total_scroll_height - tolerance


def scroll_down(browser):
    scroll_amount = random_within_std(500,50)
    browser.execute_script(f"window.scrollBy(0,{scroll_amount})");

    sleep_amount = random_within_std(1,0.5)
    time.sleep(sleep_amount)



def scroll_to_bottom(browser):
    scroll_limit = 1000
    scroll_count = 0
    scrollY = 0
    end_of_page = 0
    max_repeat = 3
    while scroll_count < scroll_limit:
        scroll_down(browser)
        scroll_count += 1
        
        prev_scrollY = scrollY
        scrollY = browser.execute_script("return window.scrollY;")
        if(prev_scrollY == scrollY):
            end_of_page += 1
        else:
            end_of_page == 0
        if end_of_page >= max_repeat:
            break




def gallery_worker(browser, rabbit_client, gallery_page):
    browser.get(gallery_page)
    scroll_to_bottom(browser)
    # print("Scroll Finished")
    
    hrefs = browser.find_elements(By.CSS_SELECTOR, ".rush-component > a.s-no-outline")
    for href in hrefs:
        url = href.get_attribute("href")
        rabbit_client.send_message("product_worker_queue", url)
        print("Publishing ${url} to product_worker_queue")
    #publish to queue

    next_page = browser.find_elements(By.CSS_SELECTOR, "a.s-pagination-next")[0].get_attribute("href")
    gallery_worker(browser, rabbit_client, next_page)




def main():

    URL_MAIN = "https://www.amazon.com/s?k=loft+frame"

    browser = webdriver.Firefox()
    rabbit_client = RabbitMQClient()
    rabbit_client.connect()
    rabbit_client.declare_queue("product_worker_queue")
    gallery_worker(browser, rabbit_client, URL_MAIN)

main()