########## UNCOMMENT LINES WITH ONE '#' TO RUN THE COMMANDS ##########


##### Install virtualenv and Python packages #####
bash install.sh
##### Install Chrome Driver for Linux. https://www.ultralinux.org/post/how-to-install-selenium-python-in-linux/  #####

#wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
#unzip chromedriver_linux64.zip
#sudo mv chromedriver /usr/bin/chromedriver
#sudo chown root:root /usr/bin/chromedriver
#sudo chmod +x /usr/bin/chromedriver

##### Install Crawlera certificate ######

##### Download certificate manually from https://support.zyte.com/support/solutions/articles/22000188407-fetching-https-pages-with-zyte-smart-proxy-manager

##### Copy the downloaded certificate file to /usr/local/share/ca-certificates/directory to make it implicitly trusted #####
# sudo cp zyte-proxy-ca.crt /usr/local/share/ca-certificates/zyte-proxy-ca.crt

##### Update stored Certificate Authority files ######
# sudo update-ca-certificates

##### Add Crawlera API key (first you need to create an account with them; they offer a 14-day free trial) ######
##### Open .env and save:
# CRAWLERA_API_KEY=<YOUR_KEY> 

###### Install Hotspot Shield VPN CLI for Linux #####
###### Get file for your OS from https://www.hotspotshield.com/vpn/vpn-for-linux/  and follow the instructions ######

##### Use Hotspot Shield CLI ######
##### Available commands: https://support.hotspotshield.com/hc/en-us/articles/360041968071-What-are-all-of-the-Hotspot-Shield-commands-on-Linux ######

###### Sign in to Hotspot Shield #####
# hotspotshield account signin