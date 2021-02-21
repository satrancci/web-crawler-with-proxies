python3 -m pip install --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate && python3 -m pip install -r requirements.txt
mkdir -p crawled_routes && mkdir -p routes_to_crawl && mkdir -p fetched_routes && mkdir -p plots
source env/bin/activate