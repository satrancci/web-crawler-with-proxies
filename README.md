# Table of Contents
**[Intro](#intro)**<br>
**[Proxies](#proxies)**<br>
    -**[Crawlera](#crawlera)**<br>
    -**[Hotspot Shield VPN](#hotspot-shield-vpn)**<br>
**[Usage](#usage)**<br>
**[Installation](#installation)**<br>
    -**[Linux](#linux)**<br>
    -**[Mac OS](#mac-os)**<br>
**[Limitations](#limitations)**<br>
**[License](#license)**<br>



# Intro

This is a web crawler for [https://www.vrbo.com](https://www.vrbo.com), which is one of the largest apartment booking websites in the world and is owned by Expedia Group. This crawler is extremely easy to use and is hard to block. Moreover, it is easy to adapt it to crawl other websites.

# Proxies

This crawler uses proxies in order not to get blocked by the website after sending too many requests. At first, I tried using free proxies from [https://www.sslproxies.org](https://sslproxies.org/). However, they did not seem to work reliably and so I went on to use other proxy services. However, if you are interested, here is the [commit](https://github.com/satrancci/vrbo-crawler/pull/14/commits/4b2307201fa791fdcaad3e309e7cd35b2514c3b8) where I added the script that crawls free proxies from [https://www.sslproxies.org](https://sslproxies.org/).

In the end, I ended up integrating the following two proxy services: [Crawlera](https://www.zyte.com/smart-proxy-manager/) and [HotspotShield VPN](https://www.hotspotshield.com/). Both are extremely easy to use and have been working reliably so far.

### Crawlera

[Crawlera](https://www.zyte.com/smart-proxy-manager/) offers a 14-day free trial, which can be used to send up to 10k requests. After registration, you can get an API key in your dashboard and you are good to go. Crawlera rotates proxies for every request. In this project, I integrated Crawlera API with `curl` command that is called from a Python script:

    command = f"curl '{base_url}{route_id}' \
    -U {api_key}: \
    -vx https://proxy.crawlera.com:8013 \
    --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
    -b --junk-session-cookies cookies.txt -c cookies.txt"



The API key is loaded from the `.env` file.


### Hotspot Shield VPN

[Hotspot Shield VPN](https://www.hotspotshield.com/) is one of the largest VPN services. I have been using it for years as a GUI application. However, recently they released a CLI version for Linux, which I tested in this project and so far it has been working splendidly. It can also be called from a Python script. The util functions can be found in [`/utils/hotspot_shield_utils.py`](https://github.com/satrancci/vrbo-crawler/blob/main/utils/hotspot_shield_utils.py). They rely on Python's `subprocess` module. The list of available locations can be found in [`./hotspot_shield_codes.txt`](https://github.com/satrancci/vrbo-crawler/blob/main/hotspot_shield_codes.txt) or by [installing](https://www.hotspotshield.com/vpn/vpn-for-linux/) the Hotspot Shield VPN for Linux, signing in with `hotspotshield account signin` and calling `hotspotshield locations`. Example usage in a Selenium [script](https://github.com/satrancci/vrbo-crawler/blob/739c80ae1b722eb130f8f33955f1fb1b9d63687a/run_selenium.py#L226-L235):

        proxy_connected = False

        while not proxy_connected:
            try:
                print("[RUNNER]: Disconnecting from the current proxy location...")
                hotspot_disconnect()
                print("[RUNNER]: Trying to connect to a new proxy location...")
                hotspot_connect_random(hotspot_codes)
                proxy_connected = True
            except Exception as exc:
                print(f"[RUNNER]: Failed to switch to a new proxy location, using Hotspot Shield CLI: {exc}")
                continue


which disconnnects from a current location and connects to some random location:

```
[RUNNER]: Disconnecting from the current proxy location...
[HOTSPOT_DISCONNECT]: Trying to disconnect...
[HOTSPOT_STATUS]: Checking status with hotspotshield status...
[HOTSPOT_STATUS]: hotspotshield status returned:
Client is running    : no
VPN connection state : disconnected

[HOTSPOT_DISCONNECT]: Successfully disconnected
[RUNNER]: Trying to connect to a new proxy location...
[HOTSPOT_STATUS]: Checking status with hotspotshield status...
[HOTSPOT_STATUS]: hotspotshield status returned:
Client is running    : yes
VPN connection state : connected
Connected location   : BN  (Brunei Darussalam)
Session uptime       : 0:02
Traffic per second   :    1.07 KiB down           0 B up
Traffic per session  :    3.70 KiB down      1.17 KiB up

[HOTSPOT_CONNECT_RANDOM]: Connected to BN successfully!
[RUNNER]: Successfully connected to a new proxy location
```

You can double check whether you are indeed connected by running `curl ipinfo.io`:

```
{
  "ip": "5.182.197.124",
  "city": "Bandar Seri Begawan",
  "region": "Brunei-Muara District",
  "country": "BN",
  "loc": "4.8903,114.9401",
  "org": "AS9009 M247 Ltd",
  "timezone": "Asia/Brunei",
  "readme": "https://ipinfo.io/missingauth"
}
```


# Usage

After [installation](#installation), the only thing that you need to do is just to add as many cities/locations that you want to crawl to `locations_to_crawl.txt` (one per row) and you are almost good to go. The flow is as follows:

`python3 run_selenium.py <locations_to_crawl> <MAX_PAGES> <routes_to_crawl> <vpn-usage-boolean [0 | 1]>`

The first argument `<locations_to_crawl>` is self-explanatory -- it is a reference to a file with cities/locations that you want to crawl, one per row.
The second argument `<MAX_PAGES>` refers to how many pages you want to crawl for each city/location. [Vrbo.com](https://www.vrbo.com) makes it easy to iterate over the pages: `http://vrbo.com/search/keywords:<LOCATION>/page:<PAGE_NUM>`. For example, [https://www.vrbo.com/search/keywords:miami/page:1](https://www.vrbo.com/search/keywords:miami/page:1). For some reason, only up to 20 pages are available for crawling for each city. Also, when crawling on Linux, 10 listings are displayed per page, whereas for Mac it is 50 listings per page. Thus, one can expect to crawl somewhere between 200 to 1000 listings per city/location, depending on the OS used. The third argument, `<routes_to_crawl>` refers to a directory (e.g. `/routes_to_crawl`), where crawled routes will be stored. For example, routes will be stored in the following format:

`miami_1.txt`:

```
/704271
/1138060
/1288487
/3777326ha
/704270
/741388
/849934
/4241471ha
/7272351ha
/4888175ha5
```
Those are valid routes that can be appended to the base url [https://www.vrbo.com](https://www.vrbo.com). For example, [https://www.vrbo.com/704271](https://www.vrbo.com/704271). The fourth argument, `<vpn-usage-boolean [0 | 1]>` makes sure that users that do not have Hotsot Shield VPN membership and/or are not Linux users, can also run `run_selenium.py`. They need to pass `0` as the fourth argument, whereas users who have Hotspot Shield membership and use Linux should pass `1`. The latter flag will ensure that a new proxy location is used for each crawled city.

For example, 

`python3 run_selenium.py locations_to_crawl.txt 20 routes_to_crawl 0`

will take a list of locations from `locations_to_crawl.txt` and for each location will crawl 20 pages (if they are, of course, available). Valid routes will be further stored in their respective txt file in `/routes_to_crawl` directory. For example, `miami_1.txt` would store valid routes for page_num=1 for Miami, etc.

`python3 run_curl.py` can be run in parallel with the selenium script. The former polls `ready_to_crawl` directory every N seconds (120 seconds by default), iterates over the available files and calls `curl` on each route. If you are a Crawlera member, store your API key in the `.env` file as
`CRAWLERA_API_KEY=<YOUR_KEY>`. It will be automatically loaded into the `run_curl.py` script. If the API key is not stored in the `.env` file, the program will gracefully continue, calling the `curl` command without a proxy:

    if api_key is None:
        command = f"curl '{base_url}{route_id}' \
        --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'\
        -b cookies.txt -c cookies.txt"

**IMPORTANT**: If your goal is just to crawl (which most likely it is!), then it is NOT necessary to first use selenium to get valid routes and then call `curl` on each of them. You can just use selenium, without any `curl` whatsoever, and parse/store data as you crawl. This was the project for one of my classes, for which the professor required the usage of `curl` command. I ended up adding the selenium script because 1) I wanted to extract some meaningful data (e.g. prices per city and not just some random prices) and 2) [Vrbo.com](https://www.vrbo.com) made it harder to crawl routes as they were not consecutive. For example, [https://www.vrbo.com/704271](https://www.vrbo.com/704271) is a valid listing route, whereas [https://www.vrbo.com/704272](https://www.vrbo.com/704272) is not (it either redirects to somewhere else or results in a Page Not Found error). Therefore, using `curl` just on its own would result in a lot of route misses. Selenium solved this problem as it stored only valid routes that were then passed on to `curl`.

The results from the `python3 run_curl.py` command are further stored in `/crawled_routes` directory, the listing as an `html` file and logs as a `txt` file. After `curl` is done with the file (e.g. `miami_1.txt`), it is then moved to `/fetched_routes` directory to ensure that it will not be crawled again.

After that, only parsing and plotting steps are left.

For parsing, the command is:

`python3 run_parsing.py`, which iterates over every `html` file in `./crawled_routes` directory and extracts the price. It further gets the name of the city from the filename and writes CITY,PRICE pair to `./parsed_data.txt` file, one per row.

Once parsing is done, plotting can be done with `python3 run_plotting.py single` to plot [CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function) for each city separately or with `python3 run_plotting.py multiple`, which generates one CDF plot with all cities. And that's it!


# Installation

### Linux

First read `./install_linux.sh`, then comment out lines that you need and then run `bash install_linux.sh`. It creates virtual environment and installs Python dependencies. It also has instructions/commands on how to install/integrate ChromeDriver for Selenium, Crawlera and HotspotShield VPN.

### Mac OS

Do the same with `./intall_mac_os.sh`.

# Limitations

The program needs more thorough testing.

# License
MIT
