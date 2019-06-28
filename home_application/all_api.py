# -*- coding:utf-8 -*-
import datetime

from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from common.log import logger
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN


# 获取平台所有模型
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
                {"bk_biz_id": i["bk_biz_id"], "bk_biz_name": i["bk_biz_name"]} for i in result["data"]["info"]
                if request.user.username in i["bk_biz_maintainer"].split(",")
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
    data = [
        {'name': 'Windows服务器', 'data': [1]},
        {'name': 'AD服务器', 'data': [3], 'color': "#4cb5b0"},
        {'name': 'TEST服务器', 'data': [5]}
    ]

    return render_json({'result':True,'data':data})



# 导入csv文件
# 导入cvs文件
# def up_cvs(request):
#     try:
#         username = request.user.username
#         up_data = json.loads(request.body)
#         auth = []
#         success = 0
#         faild = ''
#         if username:
#             auth.append(username)
#         for data in up_data:
#             try:
#                 template = Screen.objects.create(name=data['name'],config=data['config'],background_img=data['back_img'], adapter_type=data['adapter_type'], width=data['width'], height=data['height'], cover=data['cover'],when_created=u.get_time_now_str(),is_tmpl=True, auth=auth,creator=username
#                                       )
#                 for inst in eval(data['control_inst']):
#                     try:
#                         control = Control.objects.get(code=inst['control_code'])
#                     except Exception as e:
#                         break
#                     if inst['line_nodes']:
#                         ControlInst.objects.create(size_posi=json.dumps(inst['size_posi']), config=json.dumps(inst["config"]), static_data=json.dumps(inst['static_data']), control=control, screen=template, line_nodes=json.dumps(inst['line_nodes']))
#                     else:
#                         ControlInst.objects.create(size_posi=json.dumps(inst['size_posi']), config=json.dumps(inst["config"]),
#                                                    static_data=json.dumps(inst['static_data']), control=control,
#                                                    screen=template)
#                 success += 1
#             except Exception as e:
#                 faild = "导入失败"
#                 continue
#         if success == len(up_data):
#             return u.render_success_json()
#         else:
#             return u.render_fail_json(faild)
#     except Exception as e:
#         logger.exception('upload cvs error:{0}'.format(e.message))
#         return u.render_fail_json("csv文件上传失败!!")



#导出文件
# def download_file(file_path, file_name):
#     try:
#         file_path = file_path
#         file_buffer = open(file_path, 'rb').read()
#         response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
#         response['Content-Disposition'] = 'attachment; filename=' + file_name
#         response['Content-Length'] = os.path.getsize(file_path)
#         return response
#     except Exception as e:
#         logger.exception("download file error:{0}".format(e.message))
#
#
# def down_cvs(request):
#     try:
#         template_id = request.GET.get("template_id")
#         temp_list = template_id.split(',')
#         data_list = []
#         for temp in temp_list:
#             try:
#                 template = Screen.objects.get(id=temp)
#             except Exception as e:
#                 return HttpResponse("id为{0}的模板不存在!!".format(temp))
#             control_inst = ControlInst.objects.filter(screen_id=temp)
#             inst_list = []
#             for inst in control_inst:
#                 inst_list.append({
#                     "size_posi": json.loads(inst.size_posi),
#                     "config": json.loads(inst.config),
#                     "static_data": json.loads(inst.static_data),
#                     "control_code": inst.control.code,
#                     "line_nodes": json.loads(inst.line_nodes) if inst.line_nodes else ""
#                 })
#
#             data_list.append([
#                 template.name, template.background_img, template.adapter_type, template.config, template.width, template.height, template.cover, inst_list
#             ])
#         f = codecs.open('Template-Info.csv', 'wb', "gbk")
#         writer = csv.writer(f)
#         writer.writerow([u"模板名称",u"背景图", u"自适应方式",u"配置", u"宽度", u"高度", "cover", "control_inst"])
#         writer.writerows(data_list)
#         f.close()
#         file_path = "{0}/Template-Info.csv".format(PROJECT_ROOT).replace("\\", "/")
#         file_name = "Template-Info.csv"
#         return download_file(file_path, file_name)
#
#     except Exception as e:
#         logger.exception('download cvs file error:{0}'.format(e.message))
#         return HttpResponse('导出失败！')