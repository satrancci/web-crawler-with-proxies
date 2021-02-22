########## UNCOMMENT LINES WITH ONE '#' TO RUN THE COMMANDS ##########

##### Install virtualenv and Python packages #####
bash install.sh

##### Install Chrome Driver for Mac OS #####
##### Steps based on: https://stackoverflow.com/questions/38081021/using-selenium-on-mac-chrome #####

#cd $HOME/Downloads
#wget http://chromedriver.storage.googleapis.com/2.41/chromedriver_mac64.zip
#unzip chromedriver_mac64.zip
#mkdir -p $HOME/local/bin
#mv chromedriver $HOME/local/bin
#echo "export PATH=$PATH:$HOME/local/bin" >> $HOME/.bash_profile

##### Then open a new terminal window and run #####
# which chromedriver
##### and copy paste that path into run_selenium.py on the line starting with
#####  driver=webdriver.Chrome(PASTE_THE_PATH_HERE, options=options) #####

##### Install Crawlera certificate ######

##### Download certificate manually from https://support.zyte.com/support/solutions/articles/22000188407-fetching-https-pages-with-zyte-smart-proxy-manager

##### Copy the downloaded certificate file to /usr/local/share/ca-certificates/directory to make it implicitly trusted #####
# sudo cp zyte-proxy-ca.crt /usr/local/share/ca-certificates/zyte-proxy-ca.crt

##### Update stored Certificate Authority files ######
# sudo update-ca-certificates

##### Add Crawlera API key (first you need to create an account with them; they offer a 14-day free trial) ######
##### Open .env and save:
# CRAWLERA_API_KEY=<YOUR_KEY> 







