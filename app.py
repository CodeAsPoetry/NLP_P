from flask import Flask
from flask import render_template, Response, request
import jieba
import json
import requests
import sys
import os
import datetime
import random

app = Flask(__name__)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from db.action import UploadFileAction, PdDataAction


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())+''.join([str(random.randint(1,10)) for i in range(5)])


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload_excel')
def upload_file_render():
    return render_template('upload_excel.html')


@app.route('/web_scrapy')
def web_scrapy_render():
    return render_template('web_scrapy.html')


@app.route('/app_scrapy')
def app_scrapy_render():
    return render_template('app_scrapy.html')


@app.route('/data_clean')
def data_clean_render():
    return render_template('data_clean.html')


@app.route('/data_reduction_dimensionality')
def data_reduction_dimensionality_render():
    return render_template('data_reduction_dimensionality.html')


@app.route('/data_visualization')
def data_visualization_render():
    return render_template('data_visualization.html')


@app.route('/classification_label')
def classification_label_render():
    return render_template('classification_label.html')


@app.route('/regression_label')
def regression_label_render():
    return render_template('regression_label.html')


@app.route('/deeplearning_model_train')
def deeplearning_model_train_render():
    return render_template('deeplearning_model_train.html')


@app.route('/machine_learning_model_train')
def machine_learning_model_train_render():
    return render_template('machine_learning_model_train.html')


@app.route('/rule_model_train')
def rule_model_train_render():
    return render_template('rule_model_train.html')


@app.route('/deeplearning_model_deploy')
def deeplearning_model_deploy_render():
    return render_template('deeplearning_model_deploy.html')


@app.route('/machine_learning_model_deploy')
def machine_learning_model_deploy_render():
    return render_template('machine_learning_model_deploy.html')


@app.route('/rule_model_deploy')
def rule_model_deploy_render():
    return render_template('rule_model_deploy.html')


@app.route('/deeplearning_model_compress_acceler')
def deeplearning_model_compress_acceler_render():
    return render_template('deeplearning_model_compress_acceler.html')


@app.route('/magic_tools')
def magic_tools_render():
    return render_template('magic_tools.html')


@app.route('/reference_resource')
def reference_resources_render():
    return render_template('reference_resource.html')


@app.route('/api/cut_word', methods=['POST'])
def cut_word():

    testInfo = {
        "status": "failure",
        "message": "请正确填写正常句子"
    }

    sentence = request.get_json()["sentence"]
    if type(sentence) is str:
        sentence = sentence.strip().replace(" ", "")
        if sentence != "":
            word_list = " ".join(jieba.cut(sentence))

            testInfo = {
                "status": "success",
                "message": "ok",
                "word_list": word_list,
            }

    return Response(json.dumps(testInfo), mimetype='application/json')


@app.route('/api/sentiment_analysis', methods=['POST'])
def sentiment_analysis():

    testInfo = {
        "status": "failure",
        "message": "请正确填写正常句子"
    }

    sentence = request.get_json()["sentence"]
    if type(sentence) is str:
        sentence = sentence.strip().replace(" ", "")
        if sentence != "":
            url_path = "http://localhost:8503/v1/models/sa_triple_classification:predict"
            data = {
                "instances": [
                    {
                        "input_ids_ph": [
                            [101, 872, 703, 4696, 4281, 6873, 8013, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0]],
                        "input_mask_ph": [
                            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0]],
                        "segment_ids_ph": [
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0]]
                    }
                ]
            }

            r = requests.post(url_path, data=json.dumps(data))

            # print(r.json()["predictions"])

            # print(type(json.dumps(r.text)), json.dumps(r.text))

            testInfo = {
                "status": "success",
                "message": "ok",
                "result": r.json(),
            }

    return Response(json.dumps(testInfo), mimetype='application/json')


@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    upload_file = request.files.get('corpus')  # 获取到上传文件的最后一个文件（用于单文件上传）

    tid = tid_maker()
    if upload_file:
        corpus_file_path = "static/corpus/" + tid + upload_file.filename[-4:]
        upload_file.save(corpus_file_path)

        testInfo = {
            "status": "success",
            "message": "ok",
            "file_tid": tid + upload_file.filename[-4:],
        }
    else:
        testInfo = {
            "status": "failure",
            "message": "文件上传失败",
        }

    return Response(json.dumps(testInfo), mimetype='application/json')


@app.route('/api/upload_form', methods=['POST'])
def upload_form():
    # 解析表单数据
    dataIntro = request.get_json()["dataIntro"]
    dataPrivacy = request.get_json()["dataPrivacy"]
    displayFileName = request.get_json()["displayFileName"].split("\\")[-1]
    fileNameId = request.get_json()["fileNameId"]

    print(dataIntro, dataPrivacy, displayFileName, fileNameId)

    # 存入数据库
    uploadFileAction = UploadFileAction()
    uploadFileAction.InsertFileRecord(
        display_file_name=displayFileName,
        file_name_tid=fileNameId,
        data_intro=dataIntro,
        data_privacy=dataPrivacy,
    )

    testInfo = {
        "status": "success",
        "message": "ok",
    }

    return Response(json.dumps(testInfo), mimetype='application/json')


@app.route('/api/list_file_name', methods=['POST'])
def list_file_name():
    # 列出upload_file表中所有记录
    uploadFileAction = UploadFileAction()
    uploadFiles = uploadFileAction.GetAllUploadFileRecord()

    testInfo = {
        "status": "failure",
        "message": "获取上传文件列表失败",
    }

    if uploadFiles:
        upload_files = {}
        if len(uploadFiles) > 0:
            for uploadFile in uploadFiles:
                upload_file_info = []
                # print(uploadFile.id, uploadFile.display_file_name, uploadFile.file_name_tid)
                upload_file_info.append(uploadFile.display_file_name)
                upload_file_info.append(uploadFile.file_name_tid)
                upload_files[uploadFile.id] = upload_file_info

            testInfo = {
                "upload_files": upload_files,
                "status": "success",
                "message": "ok",
            }

    return Response(json.dumps(testInfo), mimetype='application/json')


@app.route('/api/create_data_table', methods=['POST'])
def create_data_table():
    # 返回指定的数据集的所有数据
    file_name_tid = request.get_json()["file_name_tid"]

    uploadFileAction = UploadFileAction()
    pdDataAction = PdDataAction()
    uploadFileId = uploadFileAction.GetUploadFileIdByTid(file_name_tid)
    all_data = pdDataAction.GetSheetAllData(uploadFileId)

    testInfo = {
        "status": "failure",
        "message": "返回指定的数据集失败",
    }
    if all_data:

        testInfo = {
            "dataset": all_data,
            "status": "success",
            "message": "ok",
        }

    return Response(json.dumps(testInfo), mimetype='application/json')


if __name__ == '__main__':
    app.run()
