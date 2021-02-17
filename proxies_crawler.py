from random import choice
import requests
from bs4 import BeautifulSoup

'''
MAPPINGS: {
    'ip_address': 0,
    'port:': 1,
    'country_code': 2,
    'country:': 3,
    'proxy_type': 4,
    'google_bool': 5,
    'https_bool': 6,
    'last_checked': 7
}
'''

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


if __name__=='__main__':
    soup = fetch_proxies()
    rows = parse_proxy_table(soup)
    #print(rows)

