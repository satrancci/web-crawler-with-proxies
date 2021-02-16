import os
from time import sleep
from random import randint

from crawler import crawl
from parser import Parser
from plot import plot_cdf


TEST_PROXIES = ['139.162.41.219:8889', '198.50.163.192:3129', '185.189.112.133:3128', '23.227.201.135:3128', '46.21.153.16:3128',
                '167.172.184.166:38318','185.236.202.205:3128','193.239.86.248:3128', '193.29.104.90:3128', '163.172.93.129:3128']
TEST_IDS = [1362215, 342627, 803442, 1196676, 1334119, 1182801, 998045, 7383908, 990147, 1571183]
BASE_URL = 'https://vrbo.com'
BASE_DIR = './crawled_data'



if __name__=='__main__':
    for test_id in TEST_IDS:
        rand_proxy_idx = randint(0,9)
        rand_proxy = TEST_PROXIES[rand_proxy_idx]
        print(f"Proxy {rand_proxy} selected at index {rand_proxy_idx}")
        sleep_time = randint(5,20)
        print(f"Sleeping for {sleep_time} seconds...")
        sleep(sleep_time)
        try:
            crawl(BASE_URL, test_id, BASE_DIR, rand_proxy)
        except Exception as exc:
            print(f"error occurred: {exc}. Skipping to next iteration...")
            continue
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

    plot_cdf(prices)


