import sys
from typing import Union
from fastapi import APIRouter, Depends, Request, Path, Header, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import crud
from schemas import schemas

from database import database
from common import common

from models import models

sys.dont_write_bytecode = True
router = APIRouter()
LOGGER = common.LOGGER


@router.get("/search")
def get_company_name(
    x_wanted_language: Union[str, None] = Header(default=None),
    query: str = "",
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_get_company_name")
        company_list = crud.get_company_name(db, query, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=company_list)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_get_company_name")


@router.get(
    "/companies/{company_name}",
)
def get_company_by_name(
    x_wanted_language: Union[str, None] = Header(default=None),
    company_name: str = "",
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_get_company_by_name")
        company_dict = crud.select_company_by_name(db, company_name, x_wanted_language)
        if company_dict == None:
            return JSONResponse(status_code=404)
        return JSONResponse(status_code=common.SUCCESS, content=company_dict)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_get_company_by_name")


@router.get("/tags")
def get_company_by_tag(
    x_wanted_language: Union[str, None] = Header(default=None),
    query: str = "",
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_get_company_by_tag")
        company_list = crud.get_company_by_tag(db, query, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=company_list)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_get_company_by_tag")


@router.put(
    "/companies/{company_name}/tags",
    responses={**schemas.responses},
)
def update_company(
    request: schemas.update_company,
    company_name: str,
    x_wanted_language: Union[str, None] = Header(default=None),
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_update_company")
        request_body = dict(request)
        tag_dict = {}
        for i in request_body["json_list"]:
            for key, value in i["tag_name"].items():
                if "tag_" + str(key) in tag_dict.keys():
                    tag_dict["tag_" + str(key)].append(value)
                else:
                    tag_dict["tag_" + str(key)] = [value]
        result = crud.update_company(db, company_name, tag_dict, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_update_company")


@router.delete(
    "/companies/{company_name}/tags/{tag_name}",
)
def delete_company(
    company_name: str,
    tag_name: str,
    x_wanted_language: Union[str, None] = Header(default=None),
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_delete_company")
        result = crud.delete_company_tag(db, company_name, tag_name, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_delete_company")


@router.post("/companies")
def update_company(
    request: schemas.update_company,
    x_wanted_language: Union[str, None] = Header(default=None),
    db: Session = Depends(database.get_db),
):
    try:
        LOGGER.info("start_update_company")
        request_body = dict(request)
        insert_dict = {}
        for lan, name in request_body["company_name"].items():
            insert_dict["company_" + lan] = name
        for tag in request_body["tags"]:
            for lan, name in tag["tag_name"].items():
                if "tag_" + lan in insert_dict.keys():
                    insert_dict["tag_" + lan].append(name)
                else:
                    insert_dict["tag_" + lan] = [name]
        result = crud.insert_company(db, insert_dict, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
    except common.customException as c:
        LOGGER.error(c.message)
        raise c
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_update_company")
