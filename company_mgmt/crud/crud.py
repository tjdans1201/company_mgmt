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
    try:
        result_data = []
        company = models.Company
        keyword = "%"+query+"%"
        result_data= db.query(company).filter(or_(
                    (company.company_ko.like(keyword)),
                    (company.company_en.like(keyword)),
                    (company.company_jp.like(keyword)),
                )).all()
        result_data = [{"company_name": row.__dict__["company_"+x_wanted_language]} for row in result_data]
        return result_data
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e    

def select_company_by_name(db, company_name, x_wanted_language):
    try:
        company = models.Company
        result_data= db.query(company).filter(or_(
                    (company.company_ko.like(company_name)),
                    (company.company_en.like(company_name)),
                    (company.company_jp.like(company_name)),
                )).first()
        if result_data:
            result_data_dict = result_data.__dict__
            result_data = {"company_name":result_data_dict["company_"+x_wanted_language], "tags":result_data_dict["tag_"+x_wanted_language].split("|")}
        
        return result_data
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e

def get_company_by_tag(db, tag, x_wanted_language):
    try:
        result_data = []
        company = models.Company
        tag_name = "%" + str(tag) + "%"
        result_data= db.query(company).filter(or_(
                    (company.tag_ko.like(tag_name)),
                    (company.tag_en.like(tag_name)),
                    (company.tag_jp.like(tag_name)),
                )).all()
        result = []
        if result_data:
            for row in result_data:
                result_dict = {}
                row_dict = row.__dict__
                if row_dict["company_"+x_wanted_language] != None:
                    result_dict["company_name"] = row_dict["company_"+x_wanted_language]
                else:
                    language_list = [i.key for i in list(company.__table__.columns) if "company" in i.key]
                    for con in language_list:
                        if row_dict[con] != None:
                            result_dict["company_name"] = row_dict[con]
                            break
                result_dict["tags"] = row_dict["tag_"+x_wanted_language].split("|")
                result.append(result_dict)
            # result_data = [{"company_name":row.__dict__["company_"+x_wanted_language] if row.__dict__["company_"+x_wanted_language] != None else , "tags":row.__dict__["tag_"+x_wanted_language].split("|")} for row in result_data]
        return result
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def select_company(db: Session, filter: dict):
    """ """
    try:
        result_data = []
        company = models.Company
        company_name = "%" + str(filter["name"]) + "%" if filter["name"] != "" else ""
        tag_name = "%" + str(filter["tag"]) + "%" if filter["tag"] != "" else ""
        company_list = db.query(company).filter(
            and_(
                or_(
                    (company.company_ko.like(company_name)),
                    (company.company_en.like(company_name)),
                    (company.company_jp.like(company_name)),
                )
                if company_name != ""
                else True,
                or_(
                    company.tag_ko.like(tag_name),
                    company.tag_en.like(tag_name),
                    company.tag_jp.like(tag_name),
                )
                if tag_name != ""
                else True,
            )
        )
        sql_result = db.execute(company_list)
        for i in sql_result:
            result_data.append(dict(zip(i.keys(), i.values())))
        return result_data
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def delete_company_tag(db,company_name,tag_name,x_wanted_language):
    try:
        company = models.Company
        a= db.query(company).filter(or_(company.company_ko == company_name,company.company_jp == company_name,company.company_en == company_name)).first()
        a_list = [i.key for i in list(company.__table__.columns) if "tag" in i.key]
        update_dict = {}
        for i in a_list:
            if i == "tag_en":
                tag = tag_name.replace(common.TAG_KO, common.TAG_EN)
            elif i == "tag_tw":
                tag = tag_name.replace(common.TAG_KO, common.TAG_TW)
            elif i == "tag_jp":
                tag = tag_name.replace(common.TAG_KO, common.TAG_JP)
            else:
                tag= tag_name
            i_list = getattr(a,i).split("|") if getattr(a,i) != None else []
            if tag in i_list:
                del i_list[i_list.index(tag)]
            update_dict[getattr(company,i)] = "|".join(list(set(i_list)))
        db.query(company).filter(or_(company.company_ko == company_name,company.company_jp == company_name,company.company_en == company_name)).update(update_dict)
        db.commit()
        return {"company_name":getattr(a,"company_"+x_wanted_language), "tags":natsorted(update_dict[getattr(company,"tag_"+x_wanted_language)].split("|"))}
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def update_company(db, company_name, tag_dict,x_wanted_language):
    try:
        company = models.Company
        a= db.query(company).filter(or_(company.company_ko == company_name,company.company_jp == company_name,company.company_en == company_name)).first()
        a_list = [i.key for i in list(company.__table__.columns) if "tag" in i.key]
        update_dict = {}
        for i in a_list:
            value_list = getattr(a,i).split("|") if getattr(a,i) != None else []
            value_list.extend(tag_dict[i])
            update_dict[getattr(company,i)] = "|".join(list(set(value_list)))
        db.query(company).filter(or_(company.company_ko == company_name,company.company_jp == company_name,company.company_en == company_name)).update(update_dict)
        db.commit()
        return {"company_name":getattr(a,"company_"+x_wanted_language), "tags":natsorted(update_dict[getattr(company,"tag_"+x_wanted_language)].split("|"))}
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e


def insert_company(db, insert_dict,x_wanted_language):
    try:
        company = models.Company
        max_id = db.query(company.id).order_by(company.id.desc()).first()[0]
        insert_dict["id"] = max_id+1
        tag_list = [i for i in list(insert_dict.keys()) if "tag" in i]
        for tag in tag_list:
            insert_dict[tag] = "|".join(natsorted(insert_dict[tag]))
        stmt = insert(company)
        db.execute(stmt, params=insert_dict)
        db.commit()
        return {"company_name":insert_dict["company_"+x_wanted_language], "tags":natsorted(insert_dict["tag_"+x_wanted_language].split("|"))}
    except Exception as e:
        db.rollback()
        LOGGER.error(common.print_exception())
        raise e