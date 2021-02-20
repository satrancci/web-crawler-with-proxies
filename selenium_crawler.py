import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs
from itertools import compress

from time import sleep, time
from random import randint


### util functions ###

def next_page_exists(soup, cur_page):
    shared_url, cur_page_num = cur_page.rsplit(':',1)
    #print('shared url:', shared_url)
    #print('cur_page_num:', cur_page_num)

    links = soup.find_all('a', href=True)
    found = False
    next_page_url = None
    for a in links:
        if shared_url in a['href']:
            val = a['href']
            #print('a[href]', val)
            next_page_num = val.rsplit(':',1)[1]
            #print('next_page_num:', next_page_num)
            if str(int(cur_page_num)+1) == next_page_num:
                found = True
                next_page_url = val
                print('[next_page_exists():] Found next page:', next_page_url)
        if found:
            found = True
            break
    return (found, next_page_url) 

def extract_valid_routes(soup):
    links = soup.find_all('a', href=True)
    bool_indices = list(map(lambda x: "unitId" in x["href"], links))
    selected = list(compress(links, bool_indices))
    cleaned = list(map(lambda x: x["href"], selected))
    ready = list(map(lambda x: x.split("?", 1)[0], cleaned))
    ready_no_dups = list(set(ready))
    #print('ready_no_dups:', ready_no_dups)
    return ready_no_dups


### Arguments from command line ####

try:
    args = sys.argv
    print(f"[selenium_crawler.py]: Received: {len(args)} arguments")
    if len(args) != 4:
        print(f"[selenium.crawler.py] There must be three required arguments: selenium_crawler.py [locations_txt_file] [max_pages] [dir_to_store]")
        raise ValueError
    try:
        LOCATIONS_FILENAME = args[1]
        MAX_PAGES = int(args[2])
        BASE_DIR = "./"+args[3]
    except Exception as exc:
        print(f"[selenium_crawler.py]: Could not import arguments: {exc}")
        raise

except Exception as exc:
    print(f"[selenium_crawler.py]: Something went wrong: {exc}")
    raise

print(f"[selenium_crawler.py]: imported the following arguments: LOCATIONS_FILENAME={LOCATIONS_FILENAME}, MAX_PAGES={MAX_PAGES}, BASE_DIR={BASE_DIR}")


LOCATIONS = []

try:
    with open(LOCATIONS_FILENAME, "r") as f:
        lines = f.readlines()
        for line in lines:
            LOCATIONS.append(line.strip())
except Exception as exc:
    print(f"[selenium_crawler.py]: Failed to read/parse {LOCATIONS_FILENAME}: {exc}")
    raise

print(f"[selenium_crawler.py]: {LOCATIONS_FILENAME} successfully imported. Received {len(LOCATIONS)} locations.")


### Constants ###

BASE_URL = "https://www.vrbo.com"

#### XPaths ###

#VALID_ROOM_URLS_XPATH = "//div[@class='HitCollection']//a/@href" # more elements (rooms previews) are loaded as we scroll down the page


def process_page_num(driver, keyword, url, num, base_dir):
    next_page_url = (False, None)
    FULL_URL = url+str(num)
    print(f"[SELENIUM_CRAWLER]: Crawling {FULL_URL}...")
    timeout = randint(11,39)
    print(f"[SELENIUM_CRAWLER]: Randint timeout for this page: {timeout} seconds")
    print(f"[SELENIUM_CRAWLER]: Sleeping for {timeout//5} seconds...")
    try:
        print(f"[SELENIUM_CRAWLER]: Going to {FULL_URL}...")
        driver.get(FULL_URL)
    except Exception as exc:
        print(f"[SELENIUM_CRAWLER]: Could not get {FULL_URL}: {exc}")
        raise

    print(f"[SELENIUM_CRAWLER]: Sleeping for {timeout//4} seconds...")
    sleep(timeout//4)
    try:
        print(f"[SELENIUM_CRAWLER]: Waiting for HitCollection class_name to load for {timeout} seconds, unless it loads sonner...") # make the string dynamic later
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "HitCollection")) # perhaps, this is not needed
        )

        try:
            print(f"[SELENIUM_CRAWLER]: Sleeping for {timeout//2} seconds...")
            sleep(timeout//2)
            start = time()
            time_limit_to_scroll_to_bottom = max(timeout, 20)
            while time()-start < time_limit_to_scroll_to_bottom:
                print("[SELENIUM_CRAWLER]: Scrolling by 400 pixels down")
                driver.execute_script("window.scrollBy(0, 400);")
                print(f"[SELENIUM_CRAWLER]: Sleeping for {max(2, timeout/10)} seconds")
                sleep(timeout//5)
                time_left_to_scroll_down = round(time_limit_to_scroll_to_bottom-(time()-start),2)
                print(f"[SELENIUM_CRAWLER]: {time_left_to_scroll_down} seconds left to scroll down...")
        except Exception as exc:
            print("[SELENIUM_CRAWLER]: Could not scroll down...")
            raise
        

        print("[SELENIUM_CRAWLER]: Parsing and trying to store data to disk...")
        try:
            html = driver.page_source
            filename = f"{base_dir}/{keyword}_{num}.txt"
            with open(filename, "w") as f:
                print(f"[SELENIUM_CRAWLER]: Opened connection to {filename}")
                soup = bs(html, "html.parser")
                print(f"[SELENIUM_CRAWLER]: Extracting valid routes from {FULL_URL}...")
                valid_routes = extract_valid_routes(soup)
                print(f"[SELENIUM_CRAWLER]: valid routes from {FULL_URL}: {valid_routes}")
                if valid_routes:
                    print("[SELENIUM_CRAWLER]: Writing valid routes to disk...")
                    for route in valid_routes:
                        f.write(route)
                        f.write("\n")
                next_page_url = next_page_exists(soup, FULL_URL)
                print(f"[SELENIUM_CRAWLER]: Next page URL: {next_page_url}")

            print("[SELENIUM_CRAWLER]: Valid routes have been successfully stored to disk.")
            print(f"[SELENIUM_CRAWLER]: Connection to {filename} closed.")
        except Exception as exc:
            print(f"[SELENIUM_CRAWLER]: Something went wrong with parsing and storing valid routes to disk: {exc}")
            raise

    except Exception as exc:
        print(f"[SELENIUM_CRAWLER]: Something went wrong while explicitly waiting for content: {exc}")
        raise
    finally:
        return (driver, next_page_url[1])

def run(base_url, locations, max_pages, base_dir, timeout=5):

    driver = None
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    driver=webdriver.Chrome('/usr/bin/chromedriver', options=options)

    print(f"[RUNNER]: Chrome driver successfully configured")
    print(f"[RUNNER]: Iterating over locations...")
    for location in locations:
        print(f"[RUNNER]: {location} location selected")
        url = f"{base_url}/search/keywords:{location}/page:"
        print(f"[RUNNER]: url: {url}")
        location_sleep_time = timeout * randint(9,15)
        print(f"[RUNNER]: Sleeping for {location_sleep_time} seconds...")
        sleep(location_sleep_time)
        i = 1
        next_page = True
        while i < max_pages+1 and next_page:
            print(f"[RUNNER]: sleeping for {timeout} seconds...")
            sleep(timeout)
            try:
                print(f"[RUNNER]: Trying {url} with page_num:{i}...")
                driver, next_page = process_page_num(driver, location, url, i, base_dir)
                if not next_page:
                    print(f"[RUNNER]: Next page does not exist. Exitting...")
                    break
                print(f"[RUNNER]: {url} with page_num:{i} successfully crawled!")
                i += 1
            except Exception as exc:
                print(f"[RUNNER]: Something went wrong: {url} with i={i}: {exc}")
                break

    print("[RUNNER]: Crawling successfully done!")
    print("[RUNNER]: Quitting the driver...")
    print("[RUNNER]: Sleeping for {timeout} seconds...")
    sleep(timeout)
    driver.quit()



if __name__=='__main__':
    run(BASE_URL, LOCATIONS, MAX_PAGES, BASE_DIR)