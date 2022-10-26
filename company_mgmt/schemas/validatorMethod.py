from common import common
import sys

sys.dont_write_bytecode = True
LOGGER = common.LOGGER


def check_list(v, field):
    """
    파라미터 타입 체크(list)
    """
    if not isinstance(v, list):
        type_message = "%s is not list" % field.name
        LOGGER.error(type_message)
        raise common.customException(400, type_message)
    return v


def check_dict(v, field):
    """
    파라미터 타입 체크(dict)
    """
    if not isinstance(v, dict):
        type_message = "%s is not dict" % field.name
        LOGGER.error(type_message)
        raise common.customException(400, type_message)
    return v
