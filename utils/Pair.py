import json
import logging
import settings
from clients import *

def get_raw_abis(abi_paths):
    raw_abis = {}
    for abi_key, abi_path in abi_paths.items():
        with open(abi_path, "r") as f:
            raw_abis[abi_key] = json.loads(f.read())['abi']
    return raw_abis

abis = get_raw_abis(settings.ABI_PATHS)

class Address:
    def __init__(self, address: str, name: str = None) -> None:
        self.name = name
        self.raw = address
        self.address = self.__parse()

    def __parse(self) -> str:
        if web3.isChecksumAddress(self.raw): return self.raw
        else: return web3.toChecksumAddress(self.raw)

class Token:
    def __init__(self, address: str) -> None:
        self.logger = logging.getLogger('root')
        self.address = address
        self.contract = web3.eth.contract(
            address=self.address,
            abi=abis['ERC20'],
        )
        self.name = self.contract.functions.name().call()
        self.symbol = self.contract.functions.symbol().call()
        self.decimals = self.contract.functions.decimals().call()

class Pair:
    def __init__(self, address: str, name: str = None) -> None:
        self.logger = logging.getLogger('root')
        address_object = Address(address, name)
        self.name = address_object.name
        self.address = address_object.address
        self.name = address_object.name
        self.contract = web3.eth.contract(
            address=self.address,
            abi=abis['PAIR'],
        )
        self.token0 = Token(self.contract.functions.token0().call())
        self.token1 = Token(self.contract.functions.token1().call())
        if self.name is None: self.name = f"{self.token0.symbol}/{self.token1.symbol}"
        self.invert_flag = self.invert_reserves()
        self.amt = 1e-3
        self.mid_price = self.get_mid()
        self.logger.info(f"Created pair {self.name}")

    def invert_reserves(self) -> bool:
        if self.name == f"{self.token0.symbol}/{self.token1.symbol}": 
            return False
        elif self.name == f"{self.token1.symbol}/{self.token0.symbol}": 
            return True
        else:
            self.logger.error(f"Wrong name for {self.address}")
            self.name = f"{self.token0.symbol}/{self.token1.symbol}"
            return False

    def get_mid(self):
        reserves = self.contract.functions.getReserves().call()
        return self.get_mid_price_from_reserves(reserves[0], reserves[1])

    def get_mid_price_from_reserves(self, reserve0, reserve1):

        def get_amount_out(amt):
            amt_with_fee = amt * 1000
            numerator = amt_with_fee * reserve1
            denominator = reserve0 * 1000 + amt_with_fee
            return numerator // denominator

        def get_amount_in(amt):
            numerator = reserve1 * amt * 1000
            denominator = (reserve0 - amt) * 1000
            return (numerator // denominator) + 1

        _bid_data = get_amount_out(self.amt * (10 ** self.token0.decimals))
        bid_data = [self.amt * int(10 ** self.token0.decimals), _bid_data]
        
        _ask_data = get_amount_in(self.amt * (10 ** self.token0.decimals))
        ask_data = [_ask_data, self.amt * int(10 ** self.token0.decimals)]

        bid = (bid_data[1]/10**self.token1.decimals)/(bid_data[0]/10**self.token0.decimals)
        ask = (ask_data[0]/10**self.token1.decimals)/(ask_data[1]/10**self.token0.decimals)

        if not self.invert_flag:
            return (bid+ask)/2

        return ((1/ask)+(1/bid))/2