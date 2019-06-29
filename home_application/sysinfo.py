# -*- coding:utf-8 -*-
import datetime
import json

from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from common.log import logger
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN
from home_application.models import Host, Server


def test(request):

    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "target_app_code": 'lhf',


        }
        result = client.bk_paas.get_app_info(kwargs)
        my_dict = {}
        if result["result"]:
            my_dict['message'] = result['message']
            my_dict['code'] = result['code']
            my_dict['data'] = [{'bk_app_code':result['data'][0]['bk_app_code'], "introduction": "lhf", "creator": "lhf","bk_app_name": result['data'][0]['bk_app_name'],"developer": "lhf"}]
            my_dict['result'] = result['result']
            my_dict['request_id'] = result['request_id']

        return render_json(my_dict)
    except Exception as e:
        logger.error(e)



TYPE = {"1": u"运维开发工程师","2": u"运维自动化工程师"}

def search_sys_info(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)


        host = Host.objects.filter(name__contains=request_data['name'], address__contains=request_data['address'], type__contains=request_data['type'], owner__contains=request_data['owner'])
        return_data = []
        for h in host:
            return_data.append({
            "id": h.id,
            "name": h.name,
            "type": TYPE.get(h.type,""),
            "status": h.status,
            "address": h.address,
            "biz_name": h.biz_name,
            "owner": h.owner,
            "when_created": h.when_created,
            "phone": h.phone,
            "title": h.title

            })

        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})



def search_detail(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        data = {}

        h = Host.objects.get(id=request_data['id'])
        data = {
            "id": h.id,
            "name": h.name,
            "type": TYPE.get(h.type,""),
            "status": h.status,
            "address": h.address,
            "biz_name": h.biz_name,
            "owner": h.owner,
            "when_created": h.when_created,
            "phone": h.phone,
            "title": h.title

            }

        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})


def search_kao_info(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        return_data = []

        h = Host.objects.get(id=request_data['id'])
        servers = Server.objects.filter(host=h)

        for k in servers:
            return_data.append({
                "id": k.id,
                "name": k.name,
                "depart": k.depart,
                "score": k.score,
                "result": k.result,
                "comment": k.comment
            })

        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})

def add_sys(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        bizs = request_data['bizL']
        biz_name = ''
        for i in bizs:
            if str(i['id']) == request_data['biz']:
                biz_name = i['text']

        data = {

            "name": request_data['name'],
            "type": request_data['type'],
            "status": u"未开始",
            "address": request_data['address'],
            "biz_name": biz_name,
            "owner": request_data['owner'],
            "when_created": request_data['start_time'],
            "phone": request_data['phone'],
            "title": request_data['title']

        }

        kaoshi = Host.objects.create(**data)
        data['id'] = kaoshi.id
        data['type'] = TYPE.get(kaoshi.type,"")
        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})


def modify_sys(request):
    try:
        request_data = json.loads(request.body)
        username = request.user.username
        data = {
            "id": "1",
            "sys_name": request_data['sys_name'],
            "sys_code": request_data['sys_code'],
            "owners": "dkdkdkd",
            "is_control": request_data['is_control'],
            "department": "dd",
            "comment": "dja",
            "first_owner": request_data['first_owner']
        }

        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"添加信息失败!!"]})


def delete_sys(request):
    try:
        request_data = json.loads(request.body)
        username = request.user.username

        Host.objects.filter(id=request_data['id']).delete()

        return render_json({"result": True, "data": {}})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"添加信息失败!!"]})


