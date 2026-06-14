import argparse
import logging
import os
import sys

from fastapi import FastAPI
import uvicorn

from checkout.router import router as checkout_router
from util import Util, DebugBot


app = FastAPI(title='Checkout Commercer', version='0.1.0')
app.include_router(checkout_router)


@app.get('/health_check')
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="App for checkout. Default log level is: loglevel = logging.INFO.")
    parser.add_argument("--log", choices=["normal", "quiet", "verbose"], help="Set logging level: normal(INFO, INFO); quiet(WARN, SIMPLE); VERBOSE(DEBUG, FULL)")
    parser.add_argument("--debug", choices=["NORMAL", "DRY_RUN", "DEBUG"], help="Set debug level: NORMAL (no debug); DRY_RUN (no commit/save actions); DEBUG (stop at breakpoints)")
    args = parser.parse_args()

    logger = Util.init_logger(log_type=args.log, use_file_handler=False)
    if args.log == "verbose":
        logger.info(Util.debug("args: {a}".format(a=vars(args))))
        logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())=}")

    debug: str = DebugBot.NORMAL if args.debug is None else DebugBot[args.debug]

    # TODO implement dotenv to get info
    # self._env_path = find_dotenv() if env_path is None else env_path
    # dotenv_values(self._env_path)

    host: str = os.getenv('APP_HOST', '0.0.0.0')
    port: str = os.getenv('APP_PORT', 8080)
    uvicorn.run(app, host=host, port=port)

    # sys.exit(f"Failed execution. Client bot don't recognized! {args.gecon=}")
    sys.exit(0)
