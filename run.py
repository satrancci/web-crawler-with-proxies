import os

from parser import Parser
from random import randint
from time import sleep, time

from crawler import crawl
from plot import plot_cdf
from crawler_hotspot import crawl_with_hotspot_shield, hotspot_connect_random, import_hotspot_codes
from dotenv import load_dotenv

load_dotenv(verbose=True)

try:
    CRAWLERA_API_KEY = os.getenv("CRAWLERA_API_KEY")
    print('CRAWLERA_API_KEY successfully loaded.')
except Exception as exc:
    print(f"Could not import CRAWLERA_API_KEY: {exc}")
    raise


try:
    HOTSPOT_CODES = import_hotspot_codes("locations.txt")
    print("HOTSPOT SHIELD VPN codes successfully loaded!")
except Exception as exc:
    print(f"Could not import HOTSPOT SHIELD VPN codes: {exc}")
    raise

TEST_IDS = [1182801, 1334119]
BASE_URL = 'https://www.vrbo.com'
BASE_DIR = './crawled_data'

MAX_RETRIES_PER_ROUTE = 10

count = 0
retry_idx = 1

while count < len(TEST_IDS):
    
    test_id = TEST_IDS[count]
    sleep_time = randint(11,28)
    print(f"Sleeping for {sleep_time} seconds...")
    sleep(sleep_time)
    print(f"(Re)try number: {retry_idx} for Vrbo room ID {test_id}...")
    try:
        hotspot_connect_random(HOTSPOT_CODES)
        crawl_with_hotspot_shield(BASE_URL, test_id, BASE_DIR)
        #crawl(BASE_URL, test_id, BASE_DIR, CRAWLERA_API_KEY)
        count += 1
        print(f"{count} pages crawled...")
        retry_idx = 1
    except Exception as exc:
        print(f"error occurred: {exc}. Will keep trying...")
        retry_idx += 1
        if retry_idx >= MAX_RETRIES_PER_ROUTE:
            count += 1
        continue

# parsing
print("Parsing data...")
prices = []
for filename in os.listdir(BASE_DIR):
    print('filename:', filename)
    if filename.endswith('.html'):
        with open(BASE_DIR+'/'+filename) as f:
            parser = Parser(f)
            ret_val, price = parser.parse()
            print('ret_val:', ret_val, 'price:', price)
            if ret_val is True:
                prices.append(int(price))
print('prices:', prices)

# plotting
print("Saving plot...")
plot_cdf(prices)