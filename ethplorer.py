import json
import requests
import time
# Ethplorer API key
apiKey = "EK-tadac-SbdwNY3-JJuAE"


# For The Sandbox crypto
def generate_sub_json_files():
    '''Create intermediate json files for retrieving each wallet's transactions'''
    
    print("Start creating sub json files")
    # retrieve top 200 largest SAND wallets
    req = requests.get(
        "https://api.ethplorer.io/getTopTokenHolders/0x3845badAde8e6dFF049820680d1F14bD3903a5d0?apiKey=" + apiKey + "&limit=200")
    holders = json.loads(req.text)
    
    # for each wallet, retrieve its transaction history
    for i in range(len(holders['holders'])):
        wallet = holders['holders'][i]
        wallet['balance'] = float(wallet['balance']) / float(10 ** 18)
        print(i, wallet['address'])
        while True:
            response = json.loads(requests.get("https://api.ethplorer.io/getAddressHistory/" + wallet[
                'address'] + "?apiKey=EK-tadac-SbdwNY3-JJuAE&type=transfer&limit=1000").text)
            time.sleep(0.1)
            if 'error' not in response:
                sandTransactions = getSandTransactions(response['operations'])
                for transaction in sandTransactions:
                    transaction.pop('tokenInfo', None)
                    transaction['value'] = float(transaction['value']) / float(10 ** 18)
                wallet['transactions'] = sandTransactions
                break
        if (i + 1) % 10 == 0:
            with open('top_wallets_and_transactions_' + str(i + 1) + '.json', 'w', encoding='utf-8') as f:
                json.dump(holders, f, ensure_ascii=False, indent=4)
    print("Finished creating sub json files")


def combine_sub_json_files(file_name):
    '''Combine results of intermediate json files with file_name root'''
    
    print("Start combining sub json files")
    combined = {'holders': []}
    for i in range(10, 210, 10):
        # For each sub_json, append its entries with the transaction results to combined['holders']
        with open(file_name + "_" + str(i) + '.json', 'r') as f:
            sub_json = json.load(f)
            combined['holders'].extend(sub_json['holders'][i - 10:i])
    # Write combined json to single file 'top_wallets_and_transactions.json'
    with open(file_name + '.json', 'w', encoding='utf-8') as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
    print("Finished combining sub json files")


def add_USD_value_for_each_transaction():
    '''Create json files with USD value for transactions in increments of 10 wallets'''
    
    print("Start adding USD value to each transaction")
    with open('top_wallets_and_transactions.json', 'r') as f:
        wallets = json.load(f)
        for i in range(len(wallets['holders'])):
            wallet = wallets['holders'][i]
            
            # print wallet address and transactions to console output
            print(i, wallet['address'])
            print("Transactions")
            
            # for each wallet, call transaction info API endpoint to get USD value of SAND at given timestamp
            for transaction in wallet['transactions']:
                print(transaction['transactionHash'])
                while True:
                    response = json.loads(requests.get("https://api.ethplorer.io/getTxInfo/" + str(
                        transaction['transactionHash']) + "?apiKey=" + apiKey + "&type=transfer&limit=1000").text)
                    time.sleep(0.1)
                    if 'error' not in response:
                        sandTransactions = getSandTransactions(response['operations'])
                        for sandTransaction in sandTransactions:
                            if sandTransaction['timestamp'] == transaction['timestamp'] and sandTransaction['from'] == \
                                    transaction['from'] and sandTransaction['to'] == transaction['to']:
                                if 'usdPrice' in sandTransaction:
                                    transaction['USD_price_at_timestamp'] = sandTransaction['usdPrice']
                                else:
                                    wallet['transactions'].remove(transaction)
                                break
                        break
            # every 10 sucessful wallets completed, create an intermediate json file to prevent loss of all API results should program abort
            if (i + 1) % 10 == 0:
                with open('top_wallets_and_transactions_with_USD_prices_' + str(i + 1) + '.json', 'w',
                          encoding='utf-8') as output:
                    json.dump(wallets, output, ensure_ascii=False, indent=4)
    print("Finished adding USD value to each transaction")


def getSandTransactions(operations):
    '''Extract SAND transactions only from all transfers'''
    return [transaction for transaction in operations if
            transaction['tokenInfo'] and 'name' in transaction['tokenInfo'] and
            transaction['tokenInfo']['name'] == 'SAND']


# I would highly recommend running each of these methods individually, commenting out the others at each step
if __name__ == "__main__":
    print("Starting script...")
    # generate_sub_json_files()
    # combine_sub_json_files('top_wallets_and_transactions')
    add_USD_value_for_each_transaction()
    combine_sub_json_files('top_wallets_and_transactions_with_USD_prices')
    print("Script has successfully completed.")
