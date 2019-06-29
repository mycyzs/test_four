# -*- coding:utf-8 -*-
import codecs
import csv
import datetime
import json
import os

import httplib2
from django.http import HttpResponse

from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from common.log import logger
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST, PROJECT_ROOT

# 获取平台所有模型
from home_application.models import Host, Server


def search_init(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        result = client.cc.search_classifications(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_classification_id'],
                    "text": i['bk_classification_name']
                })
        return render_json({'result':True,'data':data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型分类下的所有模型
def search_objects(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_classification_id':'database'
        }
        result = client.cc.search_all_objects(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_obj_id'],
                    "text": i['bk_obj_name']
                })
        return render_json({'result':True,'data':data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型下所有的实例
def search_inst(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_obj_id':'mssql',
            'condition':{},
            'bk_supplier_account':'0'
        }
        result = client.cc.search_inst(param)
        inst_data = {}
        if result['result']:
            inst_data = {'inst_id':result['data']['info'][0]['bk_inst_id']}
        return render_json({'result':True,'data':inst_data})
    except Exception as e:
        logger.error(e)


# 根据实例名获取实例详情
def search_inst_detail(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_obj_id": "mssql",
            "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
            "fields": {},
            "condition": {'bk_inst_name': 'mssql-192.168.169.22'}
        }
        result = client.cc.search_inst_by_object(param)
        inst_data = {}
        if result['result']:
            inst_data = {'inst_id':result['data']['info'][0]['bk_inst_id']}
        return render_json({'result':True,'data':inst_data})
    except Exception as e:
        logger.error(e)


# 查询所有的业务
def search_buseness(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        result = client.cc.search_business(param)
        user_business_list = []
        if result["result"]:
            user_business_list = [
                {"id": i["bk_biz_id"], "text": i["bk_biz_name"]} for i in result["data"]["info"]

            ]
        return render_json({"result": True, "data": user_business_list})
    except Exception as e:
        logger.error(e)


# 查询业务下的所有主机
def search_app_host(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},

            "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                # 根据业务ID查询主机
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": 2
                    }
                ]
            }
        ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'text':i['host']['bk_host_innerip'],
                    'app_id': i['biz'][0]['bk_biz_id'],
                    'cloud_id': i['host']['bk_cloud_id'][0]['id']
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 查询不属于该业务下所有主机
def search_all_host(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    # 根据业务ID查询主机
                    "condition": [{"field":"bk_biz_id","operator":"$nin","value":6}]
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'text':i['host']['bk_host_innerip']
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)

os_type = {'1':'Linux','2':'Windows'}


# 根据ip查询主机信息
def search_host_by_ip(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": ['192.168.165.51']},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    "condition": []
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        d={}
        if result["result"]:
            d = {}

        return render_json({"result": True, "data": d})
    except Exception as e:
        logger.error(e)


# 饼图
def get_count_obj(request):
    data_list = [
        {'name':"test1",'y':10},
        {'name':"test2",'y':20}
    ]

    return render_json({'result':True,'data':data_list})


# 折线图
def get_count(request):
    date_now = datetime.datetime.now() + datetime.timedelta(hours=-1)
    time_now = datetime.datetime.now()
    when_created__gt = str(date_now).split(".")[0]
    time_n = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    # 存的时候
    # when_created = str(datetime.datetime.now()).split(".")[0]
    # 数据库读取的时候
    # when_created__gt = str(date_now).split(".")[0]

    install_list = [
        {"name": u"本月MySQL新增数", "data": [3,6,8,9]},
        {"name": u"本月Oracle新增数", "data": [1,4,7,10]}
    ]
    return render_json({'result':True,'data':install_list,'cat':['1','2','3','4']})



def get_count_zhu(request):

    request_data = json.loads(request.body)
    host = Host.objects.get(id=request_data['id'])
    servers = Server.objects.filter(host=host)
    depart = set([i.depart for i in servers])
    data = []

    for de in depart:
        sec = Server.objects.filter(result=u'通过').count()
        fail = Server.objects.filter(result=u'未通过').count()
        data.append({'name': de, 'data':[sec, fail]})
    # data = [
    #     {'name': 'Windows服务器', 'data': [1,2]},
    #     {'name': 'AD服务器', 'data': [3], 'color': "#4cb5b0"},
    #     {'name': 'TEST服务器', 'data': [5]}
    # ]

    return render_json({'result':True,'data':data})



# 导入csv文件
#导入cvs文件
def up_cvs(request):
    try:
        username = request.user.username
        up_data = json.loads(request.body)
        kaoshi_id = up_data[0]['kaoshi_id']
        host = Host.objects.get(id=kaoshi_id)
        for data in up_data:
            Server.objects.create(name=data['name'], depart=data['depart'], score=data['score'], result=data['result'], comment=data['comment'], host=host)
        return render_json({"result": True})
    except Exception as e:
        return render_json({'result': False})



#导出文件
def download_file(file_path, file_name):
    try:
        file_path = file_path
        file_buffer = open(file_path, 'rb').read()
        response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = os.path.getsize(file_path)
        return response
    except Exception as e:
        logger.exception("download file error:{0}".format(e.message))
#
#
def down_cvs(request):
    try:
        template_id = request.GET.get("template_id")
        data_list = []
        host = Host.objects.get(id=template_id)

        data_list = [host.name, host.address, host.when_created, host.owner]
        f = codecs.open('exam.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow([u"考试名称",u"考试地点", u"考试时间",u"负责人"])
        writer.writerows(data_list)
        f.close()
        file_path = "{0}/exam.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "exam.csv"
        return download_file(file_path, file_name)

    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return HttpResponse('导出失败！')


def get_all_user(request):
    try:
        http = httplib2.Http()
        http.disable_ssl_certificate_validation = True
        url = BK_PAAS_HOST + "/api/c/compapi/v2/bk_login/get_all_users/"
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": "admin"
        }
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(param))
        if response['status'] == "200":
            res_data = json.loads(content)
            user_list = [{'id': i['bk_username'], 'text': i['bk_username']} for i in
                        res_data['data']]
            return render_json({'result': True, 'data': user_list})
        else:
            return render_json({'result': True, 'data': []})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
