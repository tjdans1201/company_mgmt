from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.dialects.postgresql import insert
from models import models
from common import common
import sys
from natsort import natsorted

sys.dont_write_bytecode = True
LOGGER = common.LOGGER


def get_company_name(db, query, x_wanted_language):
    """
    회사명 자동완성
    회사명의 일부만 들어가도 검색
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        result_data = []
        company = models.Company
        keyword = "%" + query + "%"
        # 모든 언어로 검색
        result_data = (
            db.query(company)
            .filter(
                or_(
                    (company.company_ko.like(keyword)),
                    (company.company_en.like(keyword)),
                    (company.company_ja.like(keyword)),
                )
            )
            .all()
        )
        # 헤더의 언어에 따라 회사명 출력
        result_data = [
            {"company_name": row.__dict__["company_" + x_wanted_language]} for row in result_data
        ]
        return result_data
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def select_company_by_name(db, company_name, x_wanted_language):
    """
    회사명으로 검색
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        company = models.Company
        result_data = (
            db.query(company)
            .filter(
                or_(
                    (company.company_ko.like(company_name)),
                    (company.company_en.like(company_name)),
                    (company.company_ja.like(company_name)),
                )
            )
            .first()
        )
        # 검색 결과가 있는 경우 리턴 데이터 생성
        # 헤더의 언어에 따라 리턴 언어 지정
        if result_data:
            result_data_dict = result_data.__dict__
            result_data = {
                "company_name": result_data_dict["company_" + x_wanted_language],
                "tags": result_data_dict["tag_" + x_wanted_language].split("|"),
            }

        return result_data
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def get_company_by_tag(db, tag, x_wanted_language):
    """
    태그로 회사 검색
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        result_data = []
        company = models.Company
        tag_name = "%" + str(tag) + "%"
        result_data = (
            db.query(company)
            .filter(
                or_(
                    (company.tag_ko.like(tag_name)),
                    (company.tag_en.like(tag_name)),
                    (company.tag_ja.like(tag_name)),
                )
            )
            .all()
        )
        result = []
        # 검색 결과가 있는 경우 리턴 데이터 생성
        if result_data:
            # 취득한 회사의 수 만큼 반복
            for row in result_data:
                result_dict = {}
                row_dict = row.__dict__
                # 헤더의 언어로 저장된 이름이 있는 경우
                if row_dict["company_" + x_wanted_language] != None:
                    result_dict["company_name"] = row_dict["company_" + x_wanted_language]
                # 헤더의 언어로 저장된 이름이 없는 경우 다른 언어로 저장된 이름을 리턴
                else:
                    language_list = [
                        i.key for i in list(company.__table__.columns) if "company" in i.key
                    ]
                    # tag가 들어가는 column만큼 반복하여 이름이 있는 경우 추가하고 반복문 종료
                    for con in language_list:
                        if row_dict[con] != None:
                            result_dict["company_name"] = row_dict[con]
                            break
                # 헤더의 언어에 맞는 태그 리턴
                result_dict["tags"] = row_dict["tag_" + x_wanted_language].split("|")
                result.append(result_dict)
        return result
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def delete_company_tag(db, company_name, tag_name, x_wanted_language):
    """
    해당 회사의 지정된 태그 삭제
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        company = models.Company
        # 회사명으로 회사 검색
        searched_company = (
            db.query(company)
            .filter(
                or_(
                    company.company_ko == company_name,
                    company.company_ja == company_name,
                    company.company_en == company_name,
                )
            )
            .first()
        )
        # tag 키워드가 들어있는 컬럼명 추출
        tag_list = [i.key for i in list(company.__table__.columns) if "tag" in i.key]
        update_dict = {}
        # 각 언어에 맞게 태그명 변경
        # ex) 태그_16 -> tag_16, タグ_16
        for i in tag_list:
            if i == "tag_en":
                tag = tag_name.replace(common.TAG_KO, common.TAG_EN)
            elif i == "tag_tw":
                tag = tag_name.replace(common.TAG_KO, common.TAG_TW)
            elif i == "tag_ja":
                tag = tag_name.replace(common.TAG_KO, common.TAG_JA)
            else:
                tag = tag_name
            # 해당 회사의 태그를 리스트화
            # ex) "태그_16|태그_20" -> ["태그_16", "태그_20"], None -> []
            i_list = (
                getattr(searched_company, i).split("|")
                if getattr(searched_company, i) != None
                else []
            )
            # 태그 리스트에서 해당 태그를 제거
            if tag in i_list:
                del i_list[i_list.index(tag)]
            update_dict[getattr(company, i)] = "|".join(list(set(i_list)))
        # 수정된 태그 리스트로 업데이트
        db.query(company).filter(
            or_(
                company.company_ko == company_name,
                company.company_ja == company_name,
                company.company_en == company_name,
            )
        ).update(update_dict)
        db.commit()
        return {
            "company_name": getattr(searched_company, "company_" + x_wanted_language),
            "tags": natsorted(update_dict[getattr(company, "tag_" + x_wanted_language)].split("|")),
        }
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def update_company(db, company_name, tag_dict, x_wanted_language):
    """
    회사의 태그 정보 추가
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        company = models.Company
        # 회사명으로 회사 검색
        searched_company = (
            db.query(company)
            .filter(
                or_(
                    company.company_ko == company_name,
                    company.company_ja == company_name,
                    company.company_en == company_name,
                )
            )
            .first()
        )
        # tag 키워드가 들어있는 컬럼명 추출
        tag_list = [i.key for i in list(company.__table__.columns) if "tag" in i.key]
        update_dict = {}
        # 해당 회사의 태그를 리스트화
        for i in tag_list:
            # ex) "태그_16|태그_20" -> ["태그_16", "태그_20"], None -> []
            value_list = (
                getattr(searched_company, i).split("|")
                if getattr(searched_company, i) != None
                else []
            )
            # 각 언어별 태그 리스트에 해당 태그를 추가
            value_list.extend(tag_dict[i])
            # column형식에 맞게 변경 ["태그_16", "태그_20"] -> "태그_16|태그_20"
            update_dict[getattr(company, i)] = "|".join(list(set(value_list)))
        # 변경사항 업데이트
        db.query(company).filter(
            or_(
                company.company_ko == company_name,
                company.company_ja == company_name,
                company.company_en == company_name,
            )
        ).update(update_dict)
        db.commit()
        return {
            "company_name": getattr(searched_company, "company_" + x_wanted_language),
            "tags": natsorted(update_dict[getattr(company, "tag_" + x_wanted_language)].split("|")),
        }
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def insert_company(db, insert_dict, x_wanted_language):
    """
    회사 추가
    헤더의 언어에 따라 리턴 언어 지정
    """
    try:
        company = models.Company
        # company 테이블의 가장 큰 인덱스 조회
        max_id = db.query(company.id).order_by(company.id.desc()).first()[0]
        insert_dict["id"] = max_id + 1
        # insert_dict에서 tag 키워드가 있는 키를 추출
        tag_list = [i for i in list(insert_dict.keys()) if "tag" in i]
        # tag column형식에 맞게 변경
        for tag in tag_list:
            insert_dict[tag] = "|".join(natsorted(insert_dict[tag]))
        # 해당 데이터 추가
        stmt = insert(company)
        db.execute(stmt, params=insert_dict)
        db.commit()
        return {
            "company_name": insert_dict["company_" + x_wanted_language],
            "tags": natsorted(insert_dict["tag_" + x_wanted_language].split("|")),
        }
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e
