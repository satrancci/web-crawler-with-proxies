python3 -m pip install --upgrade pip
pip3 install virtualenv
source env/bin/activate
python3 -m pip install -r requirements.txt

mkdir -p crawled_routes
mkdir -p routes_to_crawl
mkdir -p fetched_routes
mkdir -p plots