"""
dictLogger.py
"""
import os
import sys
import logging
from logging.config import dictConfig

sys.dont_write_bytecode = True


class RemoveLevelFilter(object):
    def __init__(self):
        self.level = "INFO"

    def filter(self, record):
        return record.levelno <= self.getLogLevelNum(self.level)

    def getLogLevelNum(self, level):
        switcher = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
        return switcher.get(level, "INVALID")


sys.dont_write_bytecode = True

curDir = os.path.dirname(os.path.normpath(__file__))

log_ext = ".log"
log_path = "/log/"
test_log_path = "/log/test/"
backupCnt = 2
logLevel = "INFO"
errLevel = "WARNING"

try:
    target = os.environ["TARGET"]
except:
    target = "local"

if target == "local":
    if not os.path.exists(curDir + log_path):  
        os.makedirs(curDir + log_path)

    if not os.path.exists(curDir + test_log_path):  
        os.makedirs(curDir + test_log_path)

formatter = logging.Formatter(
    "%(levelname)s %(asctime)s [%(thread)d] %(name)s.%(module)s [%(funcName)s:%(lineno)d] - %(message)s"
)
# stdout Handler
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logLevel)
consoleHandler.addFilter(RemoveLevelFilter())
# stderror Handler
consoleErrHandler = logging.StreamHandler(sys.stderr)
consoleErrHandler.setFormatter(formatter)
consoleErrHandler.setLevel(errLevel)

defaultHandler = [consoleHandler, consoleErrHandler]
logger_dict = {}
handler_list = defaultHandler
if target == "local":
    handler = logging.handlers.TimedRotatingFileHandler(
        curDir + log_path + "company_mgmt" + log_ext,
        when="midnight",
        backupCount=backupCnt,
        encoding="UTF-8",
    )
    handler.setFormatter(formatter)
    handler.setLevel(logLevel)
    # defaultHandlerにmainHandler追加必要
    handler_list = defaultHandler + [handler]

    # root logger
    logger = logging.getLogger("company_mgmt")
    logger.handlers = handler_list
    logger.setLevel(logLevel)
    logger_dict["company_mgmt"] = logger
