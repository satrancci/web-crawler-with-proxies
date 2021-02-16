import os
from time import sleep
from random import randint

from crawler import crawl
from parser import Parser
from plot import plot_cdf


TEST_IDS = [1362215, 342627, 803442, 1196676, 1334119, 1182801, 998045, 7383908, 990147, 1571183]
BASE_URL = 'https://vrbo.com'
BASE_DIR = './crawled_data'



if __name__=='__main__':
    for test_id in TEST_IDS:
        sleep(randint(5,20))
        crawl(BASE_URL, test_id, BASE_DIR)
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


