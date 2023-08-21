W200 Project 2 -- Invest in $SAND?
 
Team Members: Chun Him Cheung, Dominic Lim, Ethan Nguonly, Sarah Zheng

OVERVIEW:
Our research project looked into the meteoric rise of $SAND prices. In our project we explore:
- $SAND transfers to/from Wallets
- $SAND price changes
- Wallet holder investment performance


SETUP:
The scripts utilize a number of non-standard Python Libraries:
- NumPy
- pandas
- BeautifulSoup
- pycoingecko  (API)


TO RUN:
We have saved down intermediate files for easier use. Our primary notebook is "crypto_EDA.ipynb" which stores:
- DATA INGESTION
- DATA CLEANING/ETL
- PLOTTING/ TABLES

Important scripts containing functions called in "crypto_EDA.ipynb" are described below:
- ethplorer.py - Contains functions to call wallet transactions and data from Ethplorer
- crypto_ETL.py - Contains functions that flatten json files into pandas dataframe
- sandinfo.py - Contains functions to pull SAND data from Coin Gecko API and graph waterfall charts


OTHER FILES/FOLDERS:
There are other files/folders stored in our repo to that contain our intermediate steps during the project.
- ETH-USD.csv - Contains daily returns data on ETH that is used in a chart in "crypt_EDA.ipynb"
- BTC-USD.csv - Contains daily returns data on BTC that is used in a chart in "crypt_EDA.ipynb"
- SPY-USD.csv - Contains daily returns data on SPY that is used in a chart in "crypt_EDA.ipynb"
- crypto_EDA - Contains previous versions of our "crypto_EDA.ipynb" jupyter notebook
- final_jsons - Contains our main (cleaned) json files pulled from API that is used in "crypto_EDA.ipynb"
- top_wallets_and_transactions_sub_files - Contains raw dataset pulled from Ethplorer that is used to created the files in final_jsons
- transactions_with_USD_prices_sub_files - Contains raw dataset that pulled SAND prices for each wallet transaction
- wallet_scripts - Contains scripts that cleaned the two raw datasets listed above into the cleaned datasets in the folder final_jsons

