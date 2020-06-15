# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils")))

# print(sys.path)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from utils.mysql_connection import engine

Base = declarative_base()


class UploadFile(Base):
    __tablename__ = 'upload_file'

    id = Column(Integer, primary_key=True)
    file_name_tid = Column(String(200), nullable=False)
    display_file_name = Column(String(200), nullable=False)
    data_intro = Column(String(1000), nullable=False)
    data_privacy = Column(String(1000), nullable=False)

    def __init__(self, file_name_tid, display_file_name, data_intro, data_privacy):
        self.file_name_tid = file_name_tid
        self.display_file_name = display_file_name
        self.data_intro = data_intro
        self.data_privacy = data_privacy

    def __repr__(self):
        return '<Post %r>' % self.file_name_tid


class PdData(Base):
    __tablename__ = 'pd_data'

    id = Column(Integer, primary_key=True)
    file_name_id = Column(Integer, ForeignKey("upload_file.id", ondelete="CASCADE"), nullable=False)
    sheet_index = Column(Integer, default=0)
    row_index = Column(Integer, nullable=False)
    col_index = Column(Integer, nullable=False)
    unit_value = Column(String(5000), default="")
    invalid = Column(Boolean, default=False)

    # file_name_id, sheet_index, row_index, col_index, unit_value, invalid

    def __init__(self, file_name_id, sheet_index, row_index, col_index, unit_value, invalid):
        self.file_name_id = file_name_id
        self.sheet_index = sheet_index
        self.row_index = row_index
        self.col_index = col_index
        self.unit_value = unit_value
        self.invalid = invalid


# 父类Base调用所有继承他的子类来创建表结构
Base.metadata.create_all(engine)  # 创建表结构
