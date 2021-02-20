import os
from utils.parser import Parser
from utils.plot import plot_cdf

BASE_READ_DIR = './crawled_routes'
FILENAME_TO_WRITE = 'parsed_data.txt'


def run_parsing(dir_to_parse, filename_to_write):

    with open(filename_to_write, "w") as f_write:
        print("[run_parsing.py]: Parsing data...")
        for filename in os.listdir(dir_to_parse):
            if filename.endswith('.html'):
                print(f"[run_parsing.py]: Parsing: {filename}...")
                _, city = filename[:filename.index(".")].split('_')
                with open(dir_to_parse+'/'+filename) as f_read:
                    parser = Parser(f_read)
                    ret_val, price = parser.parse_price()
                    if ret_val is True:
                        f_write.write(f"{city}, {price}")
                        f_write.write('\n')

if __name__== '__main__':
    run_parsing(BASE_READ_DIR, FILENAME_TO_WRITE)
