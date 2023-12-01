from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import requests
import mysql.connector
import uuid
# import request


browser = webdriver.Firefox()
print(type(browser))

URL_MAIN = "https://www.youtube.com/"
URL_DUNKEY ="https://www.youtube.com/@videogamedunkey"
URL_DUNKEY_VIDS = "https://www.youtube.com/@videogamedunkey/videos"
URL_VEWN_VIDS = "https://www.youtube.com/@vewn/videos"

db_user = "youtube_ripper"
db_pass = "goog"
db_name = "youtube_test"
db_host = "localhost"



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



def insert_video_profile_overview(overview):
    #reference to database
    #insert the item
    print("Attempting to insert...", overview)
    

    connector = mysql.connector.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name)
    cursor = connector.cursor()

    table_name = "video_profile_overview"

    insertion_statement = f"""
    INSERT INTO video_profile_overview (id, title, url, views, age, length) VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (
        overview["id"].int,
        overview["title"],
        overview["url"],
        overview["views"],
        overview["age"],
        overview["length"]
    )

    for item in data:
        print(item)
        print(type(item))
    cursor.execute(insertion_statement, data)

    connector.commit()
    cursor.close()
    connector.close()


def get_all_videos_from_profile(channel_url):
    browser.get(channel_url)
        
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
        url = element.find_element(By.ID, "video-title-link").get_attribute("href")
        img_url = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        response = requests.get(img_url)
        image_data = response.content
        inline_elems = element.find_elements(By.CLASS_NAME, "inline-metadata-item")
        views = inline_elems[0].text
        age = inline_elems[1].text
        length = element.find_element(By.CSS_SELECTOR, "div#time-status").text

        video_id = uuid.uuid4()
        video_profile_overview = {
            "id": video_id,
            "title": title,
            "url": url,
            # "img": img,
            "views": views,
            "age": age,
            "length": length
        }
        
        # random_uuid = uuid.uuid4()
        # print("inserting data \n", video_profile_overview)
        insert_video_profile_overview(video_profile_overview)

        #then call the insertion function

def main():
    get_all_videos_from_profile(URL_VEWN_VIDS)
    

main()