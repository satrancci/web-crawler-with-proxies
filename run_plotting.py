import os
import sys
from utils.plot import plot_single_cdf, plot_multiple_cdf

from collections import defaultdict

FILE_TO_PARSE = 'parsed_data.txt'
WRITE_DIR = './plots'

dirs = os.listdir()

try:
    print(f"[run_plotting.py]: Checking if required directory exists...")
    if WRITE_DIR[2:] not in dirs:
        print(f"[run_plotting.py]: {WRITE_DIR[2:]} does not exist. Creating it...")
        os.mkdir(WRITE_DIR[2:])
        print(f"[run_plotting.py]: {WRITE_DIR[2:]} successfully created.")
    else:
        print(f"[run_plotting.py]: {WRITE_DIR[2:]} already exists.")

except OSError as exc:
    print(f"[run_plotting.py]: Creation of a directory failed: {exc}")
    raise


### Arguments from command line ####

try:
    args = sys.argv
    print(f"run_plotting.py]: Received: {len(args)} arguments")
    if len(args) != 2:
        print(f"[run_plotting.py]: There must be one required argument: selenium_crawler.py ['single' || 'multiple']")
        raise ValueError
    try:
        SINGLE_OR_MULTIPLE = args[1]
        if not SINGLE_OR_MULTIPLE in ['single', 'multiple']:
            raise ValueError(f"Argument must be strictly 'single' or 'multiple'")
    except Exception as exc:
        print(f"run_plotting.py]: Could not import arguments: {exc}")
        raise

except Exception as exc:
    print(f"run_plotting.py]: Something went wrong: {exc}")
    raise

print(f"run_plotting.py]: imported the following arguments: SINGLE_OR_MULTIPLE={SINGLE_OR_MULTIPLE}")




def parse_data(file_to_parse):
    cities_to_prices = defaultdict(list)
    with open(file_to_parse, 'r') as f:
        lines = f.readlines()
        for line in lines:
            city,price = line.strip().split(',')
            if price == '':
                continue
            cities_to_prices[city].append(float(price))
    return cities_to_prices


def run_plotting(file_to_parse, write_dir, single_or_multiple):
    cities_to_prices = parse_data(file_to_parse)
    if single_or_multiple == 'single':
        for city, prices in cities_to_prices.items():
            print(f"[RUN_PLOTTING]: Storing CDF plot for {city}...")
            plot_single_cdf(city, prices)
    elif single_or_multiple == 'multiple':
        print(f"[RUN_PLOTTING]: Storing one CDF plot with all cities...")
        plot_multiple_cdf(cities_to_prices)


if __name__ == '__main__':
    run_plotting(FILE_TO_PARSE, WRITE_DIR, SINGLE_OR_MULTIPLE)