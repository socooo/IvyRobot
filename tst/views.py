# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# default liberary to be imported
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db import transaction
from django.forms.utils import ErrorDict
import traceback, datetime, logging, sys
import re
import os

# from .forms import UserForm

################################################
# 导入Myibs内部数据模型
################################################ 

# from kernal.kernal.models import Parm_maskernalfrom kernal.models import Role_mas, Role_mas_tmp, Role_log
from kernal.models import Menu_mas, Menu_mas_tmp, Menu_log
from kernal.models import User_role_mas, User_role_mas_tmp, User_role_log
from kernal.models import User_mas, User_mas_tmp, User_log

from kernal.forms import Role_mas_form, Role_mas_tmp_form
from kernal.forms import Menu_mas_form, Menu_mas_tmp_form
from kernal.forms import User_role_mas_form, User_role_mas_tmp_form
from kernal.forms import User_mas_form, User_mas_tmp_form

from django.contrib.auth.models import User

logger = logging.getLogger('sourceDns.webdns.views')
# rtn_code = "999999"

###############################
# 二级交易 角色管理
###############################
#@login_required(login_url='/account/login/')
#@csrf_exempt
def tst_https_upload(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == 'GET':
        logger.info("get method start")
        return render(request, 'tst/tst_https_upload.html')

    elif request.method == "POST":
        logger.info("post method")

        try:
            obj = request.FILES.get('file_to_upload')
            f = open(os.path.join('D:\\workspace_python\\mysite\\dat', obj.name), 'wb')
            for line in obj.chunks():
                f.write(line)
            f.close()
            return HttpResponse('上传成功')
        except Exception as e:
            print(e)

def tst_smtp_send(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == 'GET':
        logger.info("get method start")
        return render(request, 'tst/tst_smtp_send.html')

    elif request.method == "POST":
        logger.info("post method")

        try:
            from interface import client

            in_parm_dict = {}
            in_parm_dict['to_user'] = "snetlogon20@sina.com"
            import time
            in_parm_dict['msg_subject'] = "subject：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            in_parm_dict['msg_body'] = "This is a message to you."

            # 以下为直接调用, 会因邮件服务器处理速度慢而停顿
            # sftp_client = client.sftp_client()
            # rtn = sftp_client.smtp_send(in_parm_dict)
            # return HttpResponse(rtn)

            #以下为异步调用
            import threading
            sftp_client = client.sftp_client()
            sftp_client_thread = threading.Thread(target=sftp_client.smtp_send, args=(in_parm_dict,))
            sftp_client_thread.start()
            rtn = "000000"
            return HttpResponse(rtn)

        except Exception as e:
            print(e)

def tst_redis(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == 'GET':
        logger.info("get method start")
        return render(request, 'tst/tst_redis.html')

    elif request.method == "POST":
        logger.info("post method")

        try:
            from interface import client
            redis_cli = client.Redis_cli()
            redis_cli.conn_redis()
            rtn = redis_cli.get_redis("a")

            return HttpResponse(rtn)

        except Exception as e:
            print(e)

def tst_mmap(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == 'GET':
        logger.info("get method start")
        return render(request, 'tst/tst_redis.html')

    elif request.method == "POST":
        logger.info("post method")

        try:
            return HttpResponse("000000")

        except Exception as e:
            print(e)

@csrf_exempt
def tst_url(request):
    rtn_code = "999999"

    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    rsp_dict = {}

    if request.method == 'GET':

        #"http://127.0.0.1:8001/tst/tst_url/?para1=a&para2=b"
        logger.info("get method start")

        concat = request.GET
        postBody = request.body
        print(concat)
        print(type(postBody))
        print(postBody)

        print(concat.get('para1'))

        print(request.GET.get('username'))
        print(request.GET.get('password'))

        rsp_rtn_header = {}
        rsp_rtn_header["rep_code"] = "000001"
        rsp_rtn_header["rep_msg"] = "OK"

        rsp_rtn_body = {}
        rsp_rtn_body['username'] = request.GET.get('username')
        rsp_rtn_body['password'] = request.GET.get('password')

        rsp_dict['rsp_header'] = rsp_rtn_header
        rsp_dict['rsp_rtn_body'] = rsp_rtn_body

        try:
            import json
            res_json = json.dumps(rsp_dict).encode(encoding='utf-8')

        except Exception as e:
            print(e)
        #return HttpResponse("000000")
        return HttpResponse(res_json)

    elif request.method == "POST":
        logger.info("post method")

        #先从request POST 对象中获取内容
        concat = request.POST
        postBody = request.body
        print(concat)
        print(type(postBody))
        print(postBody)
        print(request.get_host())
        print(request.path)
        print(request.get_full_path())
        print(concat.getlist('username'))

        #获取URL中的参数
        print(request.GET.get('username', "---"))
        print(request.GET.get('password', "---"))
        print(request.POST.get('username', "---"))
        print(request.POST.get('password', "---"))

        rsp_dict['url_username'] = request.GET.get('username', "---")
        rsp_dict['url_password'] = request.GET.get('password', "---")

        #获取header
        print(request.META.get("CONTENT_LENGTH"))
        print(request.META.get("CONTENT_TYPE"))
        print(request.META.get("HTTP_ACCEPT"))
        print(request.META.get("HTTP_ACCEPT_ENCODING"))
        print(request.META.get("HTTP_ACCEPT_LANGUAGE"))
        print(request.META.get("HTTP_HOST"))
        print(request.META.get("HTTP_REFERER"))
        print(request.META.get("HTTP_USER_AGENT"))
        print(request.META.get("QUERY_STRING"))
        print(request.META.get("REMOTE_ADDR"))
        print(request.META.get("REMOTE_HOST"))
        print(request.META.get("REMOTE_USER"))
        print(request.META.get("REQUEST_METHOD"))
        print(request.META.get("SERVER_NAME"))
        print(request.META.get("SERVER_PORT"))
        #自定义请求头
        print(request.META.get("HTTP_HEADER1"))
        print(request.META.get("HTTP_HEADER2"))
        print(request.META.get("Authorization"))

        rsp_dict['HTTP_HEADER1'] = request.META.get("HTTP_HEADER1")
        rsp_dict['HTTP_HEADER2'] = request.META.get("HTTP_HEADER2")

        #从form body 中以json方式获取参数
        import json
        try:
            str = postBody.decode(encoding='utf-8')
            print(str)
            sjson = json.loads(str)
            print(sjson)
            print(sjson["form_username"])
            print(sjson["form_password"])
        finally:
            pass

        rsp_dict['form_username'] = request.META.get("form_username")
        rsp_dict['form_password'] = request.META.get("form_password")

        rsp_dict['rep_code'] = "000001"

        res_json = json.dumps(rsp_dict).encode(encoding='utf-8')

        try:
            #return HttpResponse("000001" + request.META.get("HTTP_HEADER1"))
            return HttpResponse(res_json)

        except Exception as e:
            print(e)




