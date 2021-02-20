import os
import shutil

from parser import Parser
from random import randint
from time import sleep, time

from crawler import crawl
from plot import plot_cdf
from hotspot_shield_utils import import_hotspot_codes, hotspot_disconnect, hotspot_connect_random
from dotenv import load_dotenv

load_dotenv(verbose=True)

try:
    CRAWLERA_API_KEY = os.getenv("CRAWLERA_API_KEY")
    print('[run.py]: CRAWLERA_API_KEY successfully loaded.')
except Exception as exc:
    print(f"[run.py]: Could not import CRAWLERA_API_KEY: {exc}")
    raise

'''
try:
    HOTSPOT_CODES = import_hotspot_codes("hotspot_shield_codes.txt")
    print("HOTSPOT SHIELD VPN codes successfully loaded!")
except Exception as exc:
    print(f"Could not import HOTSPOT SHIELD VPN codes: {exc}")
    raise
'''


### Constants ###

BASE_URL = 'https://www.vrbo.com'
BASE_WRITE_DIR = './crawled_routes'
BASE_READ_DIR = './routes_to_crawl'
BASE_FETCHED_DIR = './fetched_routes'

dirs = os.listdir()

try:
    print(f"[run.py]: Checking if required directories exist...")
    for dir in [BASE_FETCHED_DIR, BASE_READ_DIR, BASE_WRITE_DIR]:
        
        if dir[2:] not in dirs:
            print(f"[run.py]: {dir[2:]} does not exist. Creating it...")
            os.mkdir(dir[2:])
            print(f"[run.py]: {dir[2:]} successfully created.")
        else:
            print(f"[run.py]: {dir[2:]} already exists.")

except OSError:
    print(f"[run.py]: Creation of a directory failed: {exc}")
    raise

MAX_RETRIES_PER_ROUTE = 5


### global count of successfully crawled pages ###
global_count = 0


print(f"[run.py]: Beginning the crawling process on {BASE_READ_DIR}...")

try:
    for filename in os.listdir(BASE_READ_DIR):
        city = filename.split('_')[0]
        print(f"[run.py]: Reading {filename}...")
        retry_idx = 1
        routes = []
        try:
            with open(BASE_READ_DIR+'/'+filename) as f:
                lines = f.readlines()
                for line in lines:
                    routes.append(line.strip())
            print(f"[run.py]: routes {routes} were successfully imported from {filename}")
        except Exception as exc:
            print(f"[run.py]: Something went wrong while reading files from {BASE_READ_DIR}: {exc}")
            raise

        local_count = 0

        while local_count < len(routes):
            route = routes[local_count]
            sleep_time = randint(5,10)
            print(f"[run.py]: Sleeping for {sleep_time} seconds...")
            sleep(sleep_time)
            print(f"[run.py]: (Re)try number: {retry_idx} / {MAX_RETRIES_PER_ROUTE} for Vrbo room ID: {route}...")
            try:
                crawl(BASE_URL, route, city, BASE_WRITE_DIR, CRAWLERA_API_KEY)
                global_count += 1
                print(f"[run.py]: {global_count} pages crawled...")
                local_count += 1
                retry_idx = 1
            except Exception as exc:
                print(f"[run.py]: Error occurred while crawling route {route}: {exc}. Will keep trying...")
                retry_idx += 1
                if retry_idx >= MAX_RETRIES_PER_ROUTE:
                    print(f"[run.py]: Limit of {MAX_RETRIES_PER_ROUTE} retries exceeded for route {route}. Trying next route...")
                    local_count += 1
                continue

        try:
            print(f"[run.py]: Moving {filename} from {BASE_READ_DIR} to {BASE_FETCHED_DIR}...")
            shutil.move(f"{BASE_READ_DIR}/{filename}", f"{BASE_FETCHED_DIR}")
            print(f"[run.py]: File successfully moved.")
        except Exception as exc:
            print(f"[run.py]: Could not move the file: {exc}")

except Exception as exc:
    print(f"[run.py]: Something went wrong: {exc}")
    raise
    
    


'''
# parsing
print("Parsing data...")
prices = []
for filename in os.listdir(BASE_WRITE_DIR):
    print('filename:', filename)
    if filename.endswith('.html'):
        with open(BASE_WRITE_DIR+'/'+filename) as f:
            parser = Parser(f)
            ret_val, price = parser.parse()
            print('ret_val:', ret_val, 'price:', price)
            if ret_val is True:
                prices.append(int(price))
print('prices:', prices)

# plotting
print("Saving plot...")
plot_cdf(prices)
'''