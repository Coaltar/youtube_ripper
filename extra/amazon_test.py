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


def random_within_std(mean,std):
    #Generate a random number from a normal distribution
    random_number = random.normalvariate(mean, std)

    # Cap the random number within one standard deviation range
    random_number = max(mean - std, min(mean + std, random_number))
    return random_number

def at_bottom():
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


def scroll_down():
    scroll_amount = random_within_std(500,50)
    browser.execute_script(f"window.scrollBy(0,{scroll_amount})");

    sleep_amount = random_within_std(1,0.5)
    time.sleep(sleep_amount)

def get_product_detail(detail_name, soup):
    #obtain a singular item from product details
    header_to_find = detail_name
    headers = soup.find_all('th')


    value = ""
    for header in headers:
        if(header.get_text().upper().strip() == header_to_find.upper().strip()):
            value = header.find_next('td').get_text()
    return value


def scroll_to_bottom():
    scroll_limit = 1000
    scroll_count = 0
    scrollY = 0
    end_of_page = 0
    max_repeat = 3
    while scroll_count < scroll_limit:
        scroll_down()
        scroll_count += 1
        
        prev_scrollY = scrollY
        scrollY = browser.execute_script("return window.scrollY;")
        if(prev_scrollY == scrollY):
            end_of_page += 1
        else:
            end_of_page == 0
        if end_of_page >= max_repeat:
            break

def data_inserter(product):
    """
    For some product data,
    inserts it into the SQL database
    """
    print(product)

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

    length = float(dimensions_match.group(1))
    width = float(dimensions_match.group(3))
    height = float(dimensions_match.group(5))

    weight_match = weight_pattern.search(weight)

    print(weight_match)
    weight = float(weight_match.group(0))
    
    print(price)
    print("dimensions:", dimensions)
    print(length, width, height)
    print("item weight", weight)
    print("asin", asin)

    product = {
        "asin": asin,
        "price": price,
        "length": length,
        "width": width,
        "hieght": height,
        "weight": weight,
    }
    data_inserter(product)





def page_worker(gallery_page):
    """
    For a particular page of amazon search results,
    gathers product urls and submits them to the product worker
    """
    browser.get(gallery_page)
    scroll_to_bottom()
    print("Scroll Finished")
    
    hrefs = browser.find_elements(By.CSS_SELECTOR, ".rush-component > a.s-no-outline")
    product_urls = []
    for href in hrefs:
        product_worker(href)
        product_urls.append(href.get_attribute("href"))


def search_worker(search_page):
    """
    For a particular amazon search, gathers all search pages and submits them to the page_worker
    """
    # page_worker(search_page) # send to page worker

    browser.get(search_page)
    next_page = browser.find_elements(By.CSS_SELECTOR, "a.s-pagination-next")[0].get_attribute("href")
    search_worker(next_page)



# def collect_items(gallery_page):
#     browser.get(gallery_page)
#     scroll_to_bottom()


#     print("Scroll Finished")

#     hrefs = browser.find_elements(By.CSS_SELECTOR, ".rush-component > a.s-no-outline")
#     item_urls = []
#     for href in hrefs:
#         item_urls.append(href.get_attribute("href"))


#     first_url = item_urls[0]
#     browser.get(first_url)

#     # scroll_to_bottom() 
#     # might need to re-apply this

    
#     html = browser.page_source
#     soup = BeautifulSoup(html, 'html.parser')
    
#     price = browser.find_element(By.CSS_SELECTOR, "div#corePrice_feature_div span.a-price-whole").text
#     dimensions = get_product_detail("Product Dimensions", soup)
#     weight = get_product_detail("Item Weight", soup)
#     asin = get_product_detail("asin", soup)
    

#     dimensions_pattern = re.compile(r'(\d+(\.\d+)?)\"[^\d]*(\d+(\.\d+)?)\"[^\d]*(\d+(\.\d+)?)\"')
#     weight_pattern = re.compile(r'(\d+(\.\d+)?)')
    
#     dimensions_match = dimensions_pattern.search(dimensions)
    
#     length = float(dimensions_match.group(1))
#     width = float(dimensions_match.group(3))
#     height = float(dimensions_match.group(5))

#     weight_match = weight_pattern.search(weight)

#     print(weight_match)
#     weight = float(weight_match.group(0))
    
#     print("dimensions:", dimensions)
#     print(length, width, height)
#     print("item weight", weight)
#     print("asin", asin)




def main():
    URL_MAIN = "https://www.amazon.com/s?k=loft+frame"
    rabbit_client = RabbitMQClient()
    rabbit_client.connect()
    rabbit_client.declare_queue("gallery_page_queue")
    rabbit_client.send_message("gallery_page_queue", URL_MAIN)
    # search_worker(URL_MAIN)

    

main()