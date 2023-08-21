import json

def generateWalletUSDBalances():
    '''Create json with SAND USD balance'''
    # sand price at 11/24/2021 at 23:00
    sand_USD_price = 7.65
    with open("top_wallets_and_transactions_with_USD_prices_and_tags.json") as f:
        holders = json.load(f)
        for wallet in holders['holders']:
            wallet['SAND_USD_balance'] = sand_USD_price * wallet['balance']
        # dump wallets with sand USD balance to final wallets json
        with open('final_wallets.json', 'w', encoding='utf-8') as f:
            json.dump(holders, f, ensure_ascii=False, indent=4)
            
if __name__=="__main__":
    generateWalletUSDBalances()
