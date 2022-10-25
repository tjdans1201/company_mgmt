from common import common
import sys

sys.dont_write_bytecode = True
LOGGER = common.LOGGER


def check_list(v, field):
    if not isinstance(v, list):
        type_message = "%s is not list" % field.name
        LOGGER.error(type_message)
        raise common.customException(400, type_message)
    return v


def check_dict(v, field):
    if not isinstance(v, dict):
        type_message = "%s is not dict" % field.name
        LOGGER.error(type_message)
        raise common.customException(400, type_message)
    return v
