import os
import threading
from parser import Parser
from random import randint
from time import sleep, time

from crawler import crawl
from plot import plot_cdf
from proxies_crawler import get_proxies, proxies_fetch_parse_write_to_disk


TEST_IDS = [1362215, 342627, 803442, 1196676, 1334119, 1182801, 998045, 7383908, 990147, 1571183]
BASE_URL = 'https://vrbo.com'
BASE_DIR = './crawled_data'
FETCH_PROXIES_SLEEP_TIME = 600 # in seconds


proxies_fetch_parse_write_to_disk()

timer = threading.Timer(FETCH_PROXIES_SLEEP_TIME, proxies_fetch_parse_write_to_disk)
timer.start()

start = time()

count = 0
prev, cur = 0, 0

while count < len(TEST_IDS):

    for test_id in TEST_IDS:

        prev = (time()-start) // FETCH_PROXIES_SLEEP_TIME

        if prev == cur:
            print('prev:', prev, 'cur:', cur)
            # read data
            proxies = [] # for now, get rid of all proxies from the previous fetch. In the future, perhaps could implement it as a queue or combine old and new lists?
            with open('proxies.txt', 'r') as f:
                lines = f.readlines()
                for line in reversed(lines): # freshest proxy will be at the end; if it does not work, we can pop it in O(1)
                    proxies.append(line.strip().split(','))
            cur += 1
        elite_proxies = get_proxies(proxies, 'elite proxy')
        print(f"Fetched {len(elite_proxies)} elite proxies")

        proxy_found = False
        while elite_proxies and not proxy_found:
            rand_proxy = elite_proxies[-1]
            print(f"Proxy {rand_proxy} selected.")
            rand_proxy = rand_proxy[0]+':'+rand_proxy[1]
            print(f"IP address and port: {rand_proxy}")
            sleep_time = randint(2,6)
            print(f"Sleeping for {sleep_time} seconds...")
            sleep(sleep_time)
            try:
                crawl(BASE_URL, test_id, BASE_DIR, rand_proxy)
                proxy_found = True
                count += 1
                print('count:', count)
            except Exception as exc:
                print(f"error occurred: {exc}. Skipping to next iteration...")
                elite_proxies.pop()
                print(f"{rand_proxy} popped from the list of proxies.")
                print(f"{len(elite_proxies)} elite proxies left")
                continue
    break


timer.cancel()

# parsing 
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
plot_cdf(prices)