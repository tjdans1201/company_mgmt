import os
import sys
import configparser
import dictlogger

sys.dont_write_bytecode = True
CONFIG = configparser.ConfigParser()
dir = os.path.dirname(os.path.realpath(__file__))
configfile = dir + "/" + "config.ini"
CONFIG.read(configfile, encoding="utf-8_sig")


class customException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def print_exception():
    """
    에러 발생시 에러 발생 라인 출력
    """
    exc_type, exc_obj, tb = sys.exc_info()
    lineno = tb.tb_lineno
    return "(LINE {}) {}".format(lineno, exc_obj)


LOGGER_KEY = "company_mgmt"
LOGGER = dictlogger.logger_dict[LOGGER_KEY]

# tag
TAG_KO = CONFIG.get("constant", "tag_ko")
TAG_EN = CONFIG.get("constant", "tag_en")
TAG_JA = CONFIG.get("constant", "tag_ja")
TAG_TW = CONFIG.get("constant", "tag_tw")


# status_code
INTERNALSERVERERROR = int(CONFIG.get("status", "internalServerError"))
SUCCESS = int(CONFIG.get("status", "success"))
NOT_FOUND = int(CONFIG.get("status", "not_found"))
