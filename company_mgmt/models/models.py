import sys
from sqlalchemy import (
    BigInteger,
    Column,
    String,
    Sequence,
)
from sqlalchemy.ext.declarative import declarative_base

sys.dont_write_bytecode = True

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = "company"

    id = Column(BigInteger, Sequence("company_id_seq"), primary_key=True, nullable=False)
    company_ko = Column(String, nullable=True)
    company_en = Column(String, nullable=True)
    company_jp = Column(String, nullable=True)
    company_tw = Column(String, nullable=True)
    tag_ko = Column(String, nullable=True)
    tag_en = Column(String, nullable=True)
    tag_jp = Column(String, nullable=True)
    tag_tw = Column(String, nullable=True)
