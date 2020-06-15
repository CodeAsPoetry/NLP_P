# -*- coding:utf-8 -*-
import os
import sys

import time
from utils.mysql_connection import session_scope
from db.orm import PdData, UploadFile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils")))


# 将当前时间转换为时间字符串，默认为2017-10-01 13:37:04格式
def now_to_date(format_string="%Y-%m-%d %H:%M:%S"):
    time_stamp = int(time.time())
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


class UploadFileAction(object):

    # 针对数据库记录的操作

    def InsertFileRecord(self, file_name_tid, display_file_name, data_intro, data_privacy):
        with session_scope() as session:
            uploadFile = UploadFile(file_name_tid=file_name_tid,
                                    display_file_name=display_file_name,
                                    data_intro=data_intro,
                                    data_privacy=data_privacy,)
            session.add(uploadFile)

    def GetFileRecord(self, id=None):
        with session_scope() as session:
            return session.query(UploadFile).filter(UploadFile.id == id).first()

    def GetUploadFileRecordByFileNameTid(self, file_name_tid):
        with session_scope() as session:
            return session.query(UploadFile).filter(UploadFile.file_name_tid == file_name_tid).first()

    def DeleteFileRecord(self, id):
        with session_scope() as session:
            uploadFile = session.query(UploadFile).filter(UploadFile.id == id).first()
            if uploadFile:
                session.delete(uploadFile)

    def UpdateFileRecord(self, id, uploadFile_):
        with session_scope() as session:
            uploadFile = session.query(UploadFile).filter(UploadFile.id == id).first()
            if not uploadFile:
                return
            uploadFile.data_intro = uploadFile_.data_intro
            uploadFile.data_privacy = uploadFile_.data_privacy
            uploadFile.file_name_tid = uploadFile_.file_name_tid
            uploadFile.display_file_name = uploadFile_.display_file_name
            return uploadFile

    # 针对业务场景对记录中字段进行微操

    # 查
    # 列出数据库中所有的文件，{id: [display_file_name, file_name_tid]}
    def GetAllUploadFileRecord(self):
        with session_scope() as session:
            uploadFiles = session.query(UploadFile).filter().all()
            return uploadFiles

    # 根据 tid 查询 id
    def GetUploadFileIdByTid(self, file_name_tid):
        with session_scope() as session:
            uploadFiles = session.query(UploadFile).filter(UploadFile.file_name_tid == file_name_tid).first()
            return uploadFiles.id


class PdDataAction(object):

    # 针对数据库记录的操作

    def InsertPdData(self, file_name_id, sheet_index, row_index, col_index, unit_value):
        with session_scope() as session:
            pdData = PdData(file_name_id=file_name_id,
                            sheet_index=sheet_index,
                            row_index=row_index,
                            col_index=col_index,
                            unit_value=unit_value,)
            session.add(pdData)

    def InsertManyPdData(self, pdDataReords):
        with session_scope() as session:
            session.add_all(pdDataReords)

    def GetPdData(self, id=None):
        with session_scope() as session:
            return session.query(PdData).filter(PdData.id == id).first()

    def DeletePdData(self, id):
        with session_scope() as session:
            pdData = session.query(PdData).filter(PdData.id == id).first()
            if pdData:
                session.delete(pdData)

    def UpdatePdData(self, id, pdData_):
        with session_scope() as session:
            pdData = session.query(PdData).filter(PdData.id == id).first()
            if not pdData:
                return
            pdData.file_name_id = pdData_.file_name_id
            pdData.sheet_index = pdData_.sheet_index
            pdData.row_index = pdData_.row_index
            pdData.col_index = pdData_.col_index
            pdData.unit_value = pdData_.unit_value
            pdData.invalid = pdData_.invalid
            return pdData

    # 针对业务场景对记录中字段进行微操

    # 查
    # 指定文件名id和对应的sheet索引(如果有的话)，获取该文件此sheet行数、列数 int
    def GetShape(self, file_name_id, sheet_index=0):
        with session_scope() as session:
            results = session.query(PdData.row_index, PdData.col_index).filter(PdData.sheet_index == sheet_index, PdData.file_name_id == file_name_id).all()
        row_index_list = []
        col_index_list = []
        for result in results:
            row_index_list.append(result[0])

        for result in results:
            col_index_list.append(result[1])

        # print(max(row_index_list), max(col_index_list))

        return max(row_index_list), max(col_index_list)

    # 指定文件名id和对应的sheet索引(如果有的话)，获取该文件sheet整个数据 map[map[]]
    def GetSheetAllData(self, file_name_id, sheet_index=0):
        with session_scope() as session:
            records = session.query(PdData).filter(PdData.sheet_index == sheet_index, PdData.file_name_id == file_name_id).all()

        all_data = {}
        for record in records:
            temp = {}
            temp[record.col_index] = record.unit_value
            all_data[record.row_index] = temp

        # print(all_data)
        return all_data

    # 指定文件名id、对应的sheet索引(如果有的话)和对应的行索引，获取该整行数据 map[col_index]

    # 指定文件名id、对应的sheet索引(如果有的话)和对应的列索引，获取该整列数据 map[row_index]

    # 指定文件名id、对应的sheet索引(如果有的话)和对应的行、列索引，获取该单元格的值 string

    # 改
    # 指定文件名id、对应的sheet索引(如果有的话)和对应的行索引，对该行数据设置无效

    # 指定文件名id、对应的sheet索引(如果有的话)和对应的列索引，对该列数据设置无效

    # 指定文件名id、对应的sheet索引(如果有的话)和对应的行、列索引，修改该单元格的值 string


if __name__ == "__main__":

    pdDataAction = PdDataAction()

    pdDataAction.GetSheetAllData(1)

    # uploadFileAction = UploadFileAction()
    #
    # uploadFileAction.GetAllUploadFileRecord()

    # 测试
    # 解析一个

    # pdDataAction.InsertPdData()


