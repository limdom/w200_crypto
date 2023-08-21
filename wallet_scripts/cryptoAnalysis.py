import requests
from bs4 import BeautifulSoup
import csv
if __name__ == "__main__":
    URL = "https://www.etherscan.io/accounts"
    resp = requests.get(URL)
    sess = requests.Session()
    soup = BeautifulSoup(sess.get(URL).text, 'html.parser')

    with open('output.csv', 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(map(str, "Rank Address Balance Percentage TxCount".split()))

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            rows = [0] * len(tds)
            for i in range(len(tds)):
                rows[i] = tds[i].get_text()

            try:
                wr.writerow(rows)
            except:
                # The page contains another table that we're
                # not worried about but which contains special
                # characters...
                pass
