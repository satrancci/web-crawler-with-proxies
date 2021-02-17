from random import choice
import requests
from bs4 import BeautifulSoup
import threading


def get_content(tag):
    return tag.contents[0]

def find_all_td(elem):
    return elem.findAll('td')

def fetch_proxies():
    response = requests.get("https://www.sslproxies.org") 
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def parse_proxy_table(soup):
    table = soup.findAll('tr')[:101]
    rows = [list(map(get_content, i)) for i in list(map(find_all_td, table[1:]))]
    return rows

def get_proxies(proxies, proxy_type, n=float('inf')):
    '''
    proxy_type: 'anonymous', 'elite proxy'
    Returns a list of size min(n, len(proxies)), which is sorted by the last column (LAST_CHECKED)
    '''
    return list(filter(lambda x: x[4]==proxy_type, proxies))[:min(n,len(proxies))]

def proxies_fetch_parse_write_to_disk():
        soup = fetch_proxies()
        print('proxies_fetch_parse_write_disc() got another batch!')
        proxies = parse_proxy_table(soup)
        print("A list of proxies passed...")
        print('Writing the batch to proxies.txt...')
        try:
            with open('proxies.txt', 'w') as f:
                for proxy in proxies:
                    f.write(",".join(proxy))
                    f.write('\n')
            print('The batch of new proxies to proxies.txt written!')
        except Exception as exc:
            print(f"proxies_fetch_parse_write_to_disc() FAILED: {exc}")
            return False
        return True


