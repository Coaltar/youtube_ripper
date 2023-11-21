from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random 
import requests


browser = webdriver.Firefox()
print(type(browser))

URL_MAIN = "https://www.youtube.com/"
URL_DUNKEY ="https://www.youtube.com/@videogamedunkey"
URL_DUNKEY_VIDS = "https://www.youtube.com/@videogamedunkey/videos"
URL_VEWN_VIDS = "https://www.youtube.com/@vewn/videos"

browser.get(URL_VEWN_VIDS)


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
    # time.sleep(2)
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    scroll_amount = random_within_std(500,50)
    browser.execute_script(f"window.scrollBy(0,{scroll_amount})");
    sleep_amount = random_within_std(1,0.5)


    time.sleep(sleep_amount)


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

print("Scroll Finished")
rich_item_elems = browser.find_elements(By.CSS_SELECTOR, "div.ytd-rich-item-renderer")


for element in rich_item_elems:
    title = element.find_element(By.ID, "video-title").text
    print(title)

    href_extension = element.find_element(By.ID, "video-title-link").get_attribute("href")
    print(href_extension)
    #we want:
    # title

    img_src = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    print(img_src)
    # href
    # img thumbnail
    # timestamp???
# title_elements = browser.find_elements(By.ID, "video-title")
# for element in title_elements:
#     print(element.text)

#get all elements

