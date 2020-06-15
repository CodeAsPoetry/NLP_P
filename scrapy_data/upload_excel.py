# -*- coding:utf -*-

import pandas as pd
# import xlrd
from db.action import PdDataAction, UploadFileAction
from db.orm import PdData


# 将指定文件名的Excel或者csv或者tsv文件解析，入库


def storage_data(file_name):
    corpus_file_path = "../static/corpus/" + file_name

    if file_name[-4:] == ".xls":      # .xls文件
        # data = xlrd.open_workbook(corpus_file_path)
        # excelTable = data.sheets()[0]
        # # 获取整行、整列、行数、列数、单元格中的值
        # print(excelTable.row_values(0))   # 获取第一行  list
        # print(excelTable.col_values(0))   # 获取第一列  list
        # print(excelTable.nrows)   # 获取行数
        # print(excelTable.ncols)   # 获取列数
        # print(excelTable.cell(0, 0))  # 获取第一行第一列对应的单元格的值
        data = pd.read_excel(corpus_file_path, header=None)
    elif file_name[-4:] == ".csv":    # .csv文件
        data = pd.read_csv(corpus_file_path, header=None)
    else:                            # .tsv文件
        data = pd.read_csv(corpus_file_path, sep='\t', header=None)
    print(data)
    print(data.shape)      # (401, 1)
    pdDatas = []
    row_num = data.shape[0]
    col_num = data.shape[1]
    pdDataAction = PdDataAction()
    uploadFileAction = UploadFileAction()

    for row_index in range(0, row_num):
        for col_index in range(0, col_num):

            print(data.iloc[row_index, col_index])

            uploadFile = uploadFileAction.GetUploadFileRecordByFileNameTid(file_name_tid=file_name)

            pdData = PdData(
                file_name_id=uploadFile.id,
                sheet_index=0,
                row_index=row_index + 1,
                col_index=col_index + 1,
                unit_value=data.iloc[row_index, col_index],
                invalid=False,
            )
            pdDatas.append(pdData)

    pdDataAction.InsertManyPdData(pdDatas)


if __name__ == "__main__":
    test_file_name = "2020052211511528963382193.csv"
    storage_data(file_name=test_file_name)




