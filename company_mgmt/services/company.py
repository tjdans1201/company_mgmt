import sys
from typing import Union
from fastapi import APIRouter, Depends,Header
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
    """
    회사명 자동완성
    회사명의 일부만 들어가도 검색이 가능
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    try:
        LOGGER.info("start_get_company_name")
        # 회사명 취득
        company_list = crud.get_company_name(db, query, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=company_list)
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
    """
    회사 이름으로 회사 검색
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    검색된 회사가 없는 경우, 404를 리턴
    """
    try:
        LOGGER.info("start_get_company_by_name")
        # 회사 정보 취득
        company_dict = crud.select_company_by_name(db, company_name, x_wanted_language)
        # 검색 결과가 없을 경우 404를 리턴
        if company_dict == None:
            return JSONResponse(status_code=common.NOT_FOUND, content={})
        return JSONResponse(status_code=common.SUCCESS, content=company_dict)
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
    """
    태그명으로 회사 검색
    태그로 검색 관련된 회사가 검색
    다국어로 검색이 가능
    일본어 태그로 검색을 해도 language가 ko이면 한국 회사명이 노출
    ko언어가 없을경우 노출가능한 언어로 출력
    동일한 회사는 한번만 노출

    """
    try:
        LOGGER.info("start_get_company_by_tag")
        # 회사 검색
        company_list = crud.get_company_by_tag(db, query, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=company_list)
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_get_company_by_tag")


@router.put(
    "/companies/{company_name}/tags")
def update_company(
    request: schemas.update_company,
    company_name: str,
    x_wanted_language: Union[str, None] = Header(default=None),
    db: Session = Depends(database.get_db),
):
    """
    회사 태그 정보 추가
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력
    """
    try:
        LOGGER.info("start_update_company")
        request_body = dict(request)
        tag_dict = {}
        # 언어별로 키 생성 및 태그 추가
        # ex)
        # {"ko" : ["태그_1"], "en": ["tag_1"]}
        for i in request_body["json_list"]:
            for key, value in i["tag_name"].items():
                if "tag_" + str(key) in tag_dict.keys():
                    tag_dict["tag_" + str(key)].append(value)
                else:
                    tag_dict["tag_" + str(key)] = [value]
        # 태그 정보 업데이트
        result = crud.update_company(db, company_name, tag_dict, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
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
    """
    회사 태그 정보 삭제
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력

    """
    try:
        LOGGER.info("start_delete_company")
        # 해당 회사의 태그 정보 삭제
        result = crud.delete_company_tag(db, company_name, tag_name, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_delete_company")


@router.post("/companies")
def insert_company(
    request: schemas.insert_company,
    x_wanted_language: Union[str, None] = Header(default=None),
    db: Session = Depends(database.get_db),
):
    """
    새로운 회사 추가
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력

    """
    try:
        LOGGER.info("start_insert_company")
        request_body = dict(request)
        # 회사 추가를 위해 dict 생성
        # ex)
        # {"company_ko":원티드랩, "company_en":wantedlab, "tag_ko":[태그_1, 태그_2], "tag_en":["tag_1","tag_2"]}
        insert_dict = {}
        for lan, name in request_body["company_name"].items():
            insert_dict["company_" + lan] = name
        for tag in request_body["tags"]:
            for lan, name in tag["tag_name"].items():
                if "tag_" + lan in insert_dict.keys():
                    insert_dict["tag_" + lan].append(name)
                else:
                    insert_dict["tag_" + lan] = [name]
        # 회사 정보 추가
        result = crud.insert_company(db, insert_dict, x_wanted_language)
        return JSONResponse(status_code=common.SUCCESS, content=result)
    except Exception as e:
        raise common.customException(common.INTERNALSERVERERROR, str(e))
    finally:
        LOGGER.info("finish_insert_company")
