import json

def createWalletTagJSON():
    '''Create a JSON dictionary file with the wallet address as the key and the wallet tag as the value.'''
    with open("top_wallets_and_transactions_with_USD_prices_and_tags.json") as f:
        wallets = json.load(f)["holders"]
        address_tags = {}
        for wallet in wallets:
            if "tag" in wallet:
                address_tags[wallet["address"]] = wallet["tag"]
        # write wallet address tags to json file
        with open('wallet_address_tags.json', 'w', encoding='utf-8') as output:
            json.dump(address_tags, output, ensure_ascii=False, indent=4)
            
if __name__ == "__main__":
    createWalletTagJSON()
