import sys
from fastapi import APIRouter
from common import common

sys.dont_write_bytecode = True
router = APIRouter()
LOGGER = common.LOGGER