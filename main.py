from utils import *
from fastapi import FastAPI

app = FastAPI()
alert(f"{os.getenv('NAME')} Starting DEX-EA server now")
logger = setup_custom_logger('root')
setup_file_logger(logger)

@app.get("/price")
async def root(pair_address: str, name: str = None):
    try:
        pair = Pair(address=pair_address, name=name)
        decimals_to_use = min(pair.token0.decimals, pair.token1.decimals)
        return {
            "success": True,
            "data": {
                "price": int(pair.mid_price * 10 ** decimals_to_use),
                "decimals": decimals_to_use
            }
        }
    except Exception as e:
        logger.error(e)
        alert(f"Error for {pair_address} from {os.getenv('NAME')}")
        return {"success": False}