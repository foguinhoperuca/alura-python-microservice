import argparse
import logging
import sys

from bot import APIBot, Bot
from controller import AgevtController, GeneralController
from integrator import get_calendars, get_people
from job import JobType
from settings import Settings, AgevtSettings
from util import Util, DebugBot


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para integração de dados. Padrão do log é: loglevel = logging.INFO.")
    parser.add_argument("--log", choices=["normal", "quiet", "verbose"], help="Set logging level: normal(INFO, INFO); quiet(WARN, SIMPLE); VERBOSE(DEBUG, FULL)")
    parser.add_argument("--debug", choices=["NORMAL", "DRY_RUN", "DEBUG"], help="Set debug level: NORMAL (no debug); DRY_RUN (no commit/save actions); DEBUG (stop at breakpoints)")
    subparser = parser.add_subparsers(dest='integration', help="Choose system to integrate with", required=True)
    subparser.add_parser('agevt').add_argument('--routine', choices=["get_calendars", "get_people"], help='Real routine tasks that must be executed for CPFL **LOW**')
    args = parser.parse_args()

    logger = Util.init_logger(log_type=args.log, use_file_handler=False)
    if args.log == "verbose":
        logger.info(Util.debug("args: {a}".format(a=vars(args))))
        logger.info(f"{logging.getLevelName(logger.getEffectiveLevel())=}")

    debug: str = DebugBot.NORMAL if args.debug is None else DebugBot[args.debug]

    if args.integration == "agevt":
        settings: Settings = AgevtSettings(debug=debug)
        bot: Bot = APIBot(settings=settings, debug=debug)
        controller: GeneralController = AgevtController(job_type=JobType.AGEVT, settings=settings, bot=bot, debug=debug)
        if args.routine == "get_calendars":
            # TODO use a controller.py to orchestrate all actions
            print('TODO implement get calendars to store')
            get_calendars()     # FIXME need it? Probably not...
            controller.get_calendars_available()
        elif args.routine == "get_people":
            print('TODO implement get people to store')
            get_people()        # FIXME need it? Probably not...
            controller.get_people_by_calendar()
        else:
            sys.exit(f"Failed execution. Routine don't recognized! {args.routine=}")
    else:
        sys.exit(f"Failed execution. Client bot don't recognized! {args.gecon=}")

    sys.exit(0)
