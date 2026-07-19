import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI

from app.checkout.router import router as checkout_router
from app.util import Util, DebugBot


# env_path = find_dotenv()
# dotenv_values(env_path)
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

app = FastAPI(title='Checkout Commercer', version='0.1.0')
app.include_router(checkout_router)

uvilogger = logging.getLogger('uvicorn.info')


@app.get('/health_check')
async def health_check():
    payment_url: str = os.getenv("URL_SERVICE_PAYMENT")
    order_url: str = os.getenv("URL_SERVICE_ORDER")
    inventory_url: str = os.getenv("URL_SERVICE_INVENTORY")
    host_app: str = os.getenv("APP_HOST")
    port_app: str = os.getenv("APP_PORT")
    response: dict = {
        "status": "ok",
        "payment_url": payment_url,
        "order_url": order_url,
        "inventory_url": inventory_url,
        "host_app": host_app,
        "port_app": port_app,
    }
    print(f'Got dict values: {response}')
    uvilogger.info(f'Logging some response: {response}')

    return response


if __name__ == "__main__":
    import uvicorn
    # TODO using argparse
    parser = argparse.ArgumentParser(description="App for checkout. Default log level is: loglevel = logging.INFO.")
    parser.add_argument("--log", choices=["normal", "quiet", "verbose"], help="Set logging level: normal(INFO, INFO); quiet(WARN, SIMPLE); VERBOSE(DEBUG, FULL)")
    parser.add_argument("--debug", choices=["NORMAL", "DRY_RUN", "DEBUG"], help="Set debug level: NORMAL (no debug); DRY_RUN (no commit/save actions); DEBUG (stop at breakpoints)")
    args = parser.parse_args()

    logger = Util.logger_factory()
    if args.log == "verbose":
        logger.info(Util.debug("args: {a}".format(a=vars(args))))
        logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())=}")

    debug: DebugBot = DebugBot.NORMAL if args.debug is None else DebugBot[args.debug]

    uvicorn_reload: bool = True
    host: str = os.getenv('APP_HOST', '0.0.0.0')
    port: str = os.getenv('APP_PORT', 8080)
    print(f'===== variables loaded is {host=} and {port=} =====')
    uvicorn.run('app.main:app', host=host, port=int(port), reload=uvicorn_reload)

    sys.exit(0)
