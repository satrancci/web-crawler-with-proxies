'''
Copyright (c) 2021 Alex Ipatov

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import os
import shutil

from utils.curl import crawl
from utils.hotspot_shield_utils import import_hotspot_codes, hotspot_disconnect, hotspot_connect_random

from random import randint
from time import sleep, time

from dotenv import load_dotenv

load_dotenv(verbose=True)


try:
    CRAWLERA_API_KEY = os.getenv("CRAWLERA_API_KEY", None)
    if CRAWLERA_API_KEY is None:
        print("[run_curl.py]: CRAWLERA_API_KEY does not exist. Proceeding without it...")
    else:
        print('[run_curl.py]: CRAWLERA_API_KEY successfully loaded.')
except Exception as exc:
    print(f"[run_curl.py]: Could not import CRAWLERA_API_KEY: {exc}")
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
    print(f"[run_curl.py]: Checking if required directories exist...")
    for dir in [BASE_FETCHED_DIR, BASE_READ_DIR, BASE_WRITE_DIR]:
        
        if dir[2:] not in dirs:
            print(f"[run_curl.py]: {dir[2:]} does not exist. Creating it...")
            os.mkdir(dir[2:])
            print(f"[run_curl.py]: {dir[2:]} successfully created.")
        else:
            print(f"[run_curl.py]: {dir[2:]} already exists.")

except OSError as exc:
    print(f"[run_curl.py]: Creation of a directory failed: {exc}")
    raise

MAX_RETRIES_PER_ROUTE = 5


### global count of successfully crawled pages ###
global_count = 0


print(f"[run_curl.py]: Beginning the crawling process on {BASE_READ_DIR}...")

POLLING_TIME = 120 # check directory every N seconds once it is empty (instead of just exiting the program)

while True:
    print(f"[run_curl.py]: Sleeping for {POLLING_TIME} seconds...")
    sleep(POLLING_TIME)
    try:
        for filename in os.listdir(BASE_READ_DIR):
            city = filename.split('_')[0]
            print(f"[run_curl.py]: Reading {filename}...")
            retry_idx = 1
            routes = []
            try:
                with open(BASE_READ_DIR+'/'+filename) as f:
                    lines = f.readlines()
                    for line in lines:
                        routes.append(line.strip())
                print(f"[run_curl.py]: routes {routes} were successfully imported from {filename}")
            except Exception as exc:
                print(f"[run_curl.py]: Something went wrong while reading files from {BASE_READ_DIR}: {exc}")
                raise

            local_count = 0

            while local_count < len(routes):
                route = routes[local_count]
                sleep_time = randint(5,10)
                print(f"[run_curl.py]: Sleeping for {sleep_time} seconds...")
                sleep(sleep_time)
                print(f"[run_curl.py]: (Re)try number: {retry_idx} / {MAX_RETRIES_PER_ROUTE} for Vrbo room ID: {route}...")
                try:
                    crawl(BASE_URL, route, city, BASE_WRITE_DIR, CRAWLERA_API_KEY)
                    global_count += 1
                    print(f"[run_curl.py]: {global_count} pages crawled...")
                    local_count += 1
                    retry_idx = 1
                except Exception as exc:
                    print(f"[run_curl.py]: Error occurred while crawling route {route}: {exc}. Will keep trying...")
                    retry_idx += 1
                    if retry_idx >= MAX_RETRIES_PER_ROUTE:
                        print(f"[run_curl.py]: Limit of {MAX_RETRIES_PER_ROUTE} retries exceeded for route {route}. Trying next route...")
                        local_count += 1
                    continue

            try:
                print(f"[run_curl.py]: Moving {filename} from {BASE_READ_DIR} to {BASE_FETCHED_DIR}...")
                shutil.move(f"{BASE_READ_DIR}/{filename}", f"{BASE_FETCHED_DIR}")
                print(f"[run_curl.py]: File successfully moved.")
            except Exception as exc:
                print(f"[run_curl.py]: Could not move the file: {exc}")

    except Exception as exc:
        print(f"[run_curl.py]: Something went wrong: {exc}")
        raise
    
    
print("[run_curl.py]: Crawling completed!")