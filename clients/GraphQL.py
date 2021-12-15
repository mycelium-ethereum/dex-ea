import requests

class Bitquery:
    URL = "https://graphql.bitquery.io"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-API-KEY": self.api_key}

    def run_query(self, query: str):
        request = requests.post(self.URL, json={'query': query}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def get_volume(self, pair_address: str):
        query = """
        {
        ethereum(network: ethereum) {
            dexTrades(
            options: {limit: 1, desc: "timeInterval.day"}
            smartContractAddress: {is: "0x0463a06fbc8bf28b3f120cd1bfc59483f099d332"}
            ) {
            timeInterval {
                day(count: 1)
            }
            baseCurrency {
                symbol
                address
            }
            baseAmount
            quoteCurrency {
                symbol
                address
            }
            quoteAmount
            trades: count
            quotePrice
            maximum_price: quotePrice(calculate: maximum)
            minimum_price: quotePrice(calculate: minimum)
            open_price: minimum(of: block, get: quote_price)
            close_price: maximum(of: block, get: quote_price)
            tradeAmount(in: USD)
            }
        }
        }""".format(pair_address)
        return self.run_query(query)