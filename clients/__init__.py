from dotenv import load_dotenv
load_dotenv();

import os
from web3 import Web3
from clients.Webhook import webhook

web3 = Web3(Web3.HTTPProvider(os.environ.get("ETH_HTTP_URL")))