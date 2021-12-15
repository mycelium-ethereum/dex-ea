import logging

# Logging 
LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG
LOGGER_NAME = 'root'

# Abis
ABI_PATHS = {
    'PAIR': 'abis/IUniswapV2Pair.json',
    'ERC20': 'abis/IUniswapV2ERC20.json',
}