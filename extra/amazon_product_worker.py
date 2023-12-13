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


browser = webdriver.Firefox()

db_user = "amazon_worker"
db_pass = "cheap"
db_name = "amazon_test"
db_host = "localhost"



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

def insert_data(data):
    print("Attempting to insert...", data)
    

    connector = mysql.connector.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name)
    cursor = connector.cursor()

    # table_name = "video_profile_overview"
    print(f"Inserting ${data} into loft beds.)")
    insertion_statement = f"""
    INSERT INTO loft_beds (asin, dim_length, dim_width, dim_height, price, weight) VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (
        data["asin"],
        data["dim_length"],
        data["dim_width"],
        data["dim_height"],
        data["price"],
        data["weight"]
    )
    # cursor.execute(insertion_statement, data)
    try:
        cursor.execute(insertion_statement, data)
    except mysql.connector.IntegrityError as e:
        print(f"Error: {e}")
        # Handle the error here


    connector.commit()
    cursor.close()
    connector.close()

def get_product_detail(detail_name, soup):
    #obtain a singular item from product details
    header_to_find = detail_name
    headers = soup.find_all('th')


    value = ""
    for header in headers:
        if(header.get_text().upper().strip() == header_to_find.upper().strip()):
            value = header.find_next('td').get_text()
    return value.strip()


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



def product_worker(product_url):
    """
    For a particular product page,
    gathers the desired product information, packages it, then sends it to the data_inserter"""
    
    browser.get(product_url)
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    

    price = browser.find_element(By.CSS_SELECTOR, "div#corePrice_feature_div span.a-price-whole").text
    dimensions = get_product_detail("Product Dimensions", soup)
    weight = get_product_detail("Item Weight", soup)
    asin = get_product_detail("asin", soup)
    

    dimensions_pattern = re.compile(r'(\d+(\.\d+)?)\"[^\d]*(\d+(\.\d+)?)\"[^\d]*(\d+(\.\d+)?)\"')
    weight_pattern = re.compile(r'(\d+(\.\d+)?)')
    
    dimensions_match = dimensions_pattern.search(dimensions)

    if(dimensions_match):
        length = float(dimensions_match.group(1))
        width = float(dimensions_match.group(3))
        height = float(dimensions_match.group(5))
    else:
        length = width = height = 0

    weight_match = weight_pattern.search(weight)

    if(weight_match):
        weight = float(weight_match.group(0))
    else:
        weight = 0

    # print(weight_match)
    # weight = float(weight_match.group(0))
    
    # print(price)
    # print("dimensions:", dimensions)
    # print(length, width, height)
    # print("item weight", weight)
    # print("asin", asin)

    product = {
        "asin": asin,
        "price": price,
        "dim_length": length,
        "dim_width": width,
        "dim_height": height,
        "weight": weight,
    }
    # print(product)
    insert_data(product)






# def search_worker(search_page):
#     """
#     For a particular amazon search, gathers all search pages and submits them to the page_worker
#     """
#     # page_worker(search_page) # send to page worker

#     browser.get(search_page)
#     next_page = browser.find_elements(By.CSS_SELECTOR, "a.s-pagination-next")[0].get_attribute("href")
#     search_worker(next_page)

def callback(ch, method, properties, body):
    # print(f"{ch} - {method} - {properties}")
    print(f"Received message: {body}")
    url = body.decode('utf-8')
    print(url)
    product_worker(url)

    time.sleep(0.5)

    



def main():

    queue_name = "product_worker_queue"

    # browser = webdriver.Firefox()
    rabbit_client = RabbitMQClient()
    rabbit_client.connect()
    rabbit_client.declare_queue(queue_name)


    rabbit_client.receive_messages(queue_name, callback)
    

    # search_worker(URL_MAIN)

    

main()