import os
from shutil import SameFileError
import sys
import configparser
import ast
import dictlogger

sys.dont_write_bytecode = True
CONFIG = configparser.ConfigParser()
dir = os.path.dirname(os.path.realpath(__file__))
configfile = dir + "/" + "config.ini"
CONFIG.read(configfile, encoding="utf-8_sig")


class customException(Exception):
    def __init__(
        self, status_code: int, message: str, url:str):
        self.status_code = status_code
        self.message = message if url is None else message.format(url=url)
