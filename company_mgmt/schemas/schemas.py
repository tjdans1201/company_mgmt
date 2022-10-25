from fastapi.param_functions import Depends
from pydantic import BaseModel, validator, Field
from schemas import validatorMethod
import sys


sys.dont_write_bytecode = True


class update_company(BaseModel):
    json_list: list

    class Config:
        schema_extra = {
            "example": {
                "json_list": ["태그_4", "태그_20", "태그_16"],
            }
        }

    # validator
    _validator_for_tag_list: classmethod = validator("json_list", allow_reuse=True, pre=True)(
        validatorMethod.check_list
    )


class update_company(BaseModel):
    company_name: dict
    tags: list

    class Config:
        schema_extra = {
            "example": {
                "company_name": {
                    "ko": "라인 프레쉬",
                    "tw": "LINE FRESH",
                    "en": "LINE FRESH",
                },
                "tags": [
                    {
                        "tag_name": {
                            "ko": "태그_1",
                            "tw": "tag_1",
                            "en": "tag_1",
                        }
                    },
                    {
                        "tag_name": {
                            "ko": "태그_8",
                            "tw": "tag_8",
                            "en": "tag_8",
                        }
                    },
                    {
                        "tag_name": {
                            "ko": "태그_15",
                            "tw": "tag_15",
                            "en": "tag_15",
                        }
                    },
                ],
            }
        }

    # validator
    _validator_for_tag_list: classmethod = validator("company_name", allow_reuse=True, pre=True)(
        validatorMethod.check_dict
    )
    _validator_for_tag_list: classmethod = validator("tags", allow_reuse=True, pre=True)(
        validatorMethod.check_list
    )
