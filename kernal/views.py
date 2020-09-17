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

from .forms import UserForm

################################################
# 导入Myibs内部数据模型
################################################ 

from .models import Parm_mas
from .models import Role_mas, Role_mas_tmp, Role_log
from .models import Menu_mas, Menu_mas_tmp, Menu_log
from .models import User_role_mas, User_role_mas_tmp, User_role_log
from .models import User_mas, User_mas_tmp, User_log

from .forms import Role_mas_form, Role_mas_tmp_form
from .forms import Menu_mas_form, Menu_mas_tmp_form
from .forms import User_role_mas_form, User_role_mas_tmp_form
from .forms import User_mas_form, User_mas_tmp_form

from django.contrib.auth.models import User

logger = logging.getLogger('sourceDns.webdns.views')
# rtn_code = "999999"


###############################
# 一级交易
###############################
# Create your views here.


###############################
# 二级交易 角色管理
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_lst2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    #role_mas_lst = Role_mas.objects.filter(status="A")
    role_mas_lst = Role_mas.objects.filter(status__in=["A", "C", "D"])
    paginator = Paginator(role_mas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        role_mas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        role_mas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        role_mas_lst = current_page.object_list

    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/role_mas_lst2lvl.html", {"role_mas_lst": role_mas_lst, "page": current_page})


@login_required(login_url='/account/login/')
def role_mas_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    role_mas_form = get_object_or_404(Role_mas, id=id)
    logger.info("get method end")

    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/role_mas_dsp.html", {"role_mas_form": role_mas_form})

@login_required(login_url='/account/login/')
def role_mas_dsp_json(request, id):
    from kernal.models import User_role_mas, Menu_log
    from django.http import JsonResponse
    from json import dumps
    from django.core import serializers

    # menu_log = Menu_log.objects.all()
    menu_log = Menu_log.objects.filter(id=1)
    response_data = {}
    try:
        response_data['result'] = 'Success'
        response_data['message'] = serializers.serialize('json', menu_log)
        print(response_data)
    except:
        response_data['result'] = 'Ouch!'

    print(response_data)
    return HttpResponse(JsonResponse(response_data), content_type="application/json")


###############################
# 二级交易
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_add(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        role_mas_tmp_form = Role_mas_tmp_form(request.POST)

        # role_id111 = request.POST.get("role_id111")
        # print(role_id111)

        logger.info("post method")
        if role_mas_tmp_form.is_valid():
            logger.info("post method")

            # Role_mas_tmp_Form_cd = role_mas_tmp_form.cleaned_data
            try:
                with transaction.atomic():

                    role_mas_tmp = role_mas_tmp_form.save(commit=False)
                    role_mas_tmp.status = "A"

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    role_mas_tmp.ver_no = 1
                    role_mas_tmp.prod = "Role_mas"
                    role_mas_tmp.func = sys._getframe().f_code.co_name
                    role_mas_tmp.maker = request.user.username
                    role_mas_tmp.inp_date = datetime.datetime.now()
                    role_mas_tmp.checker = ""
                    role_mas_tmp.app_date = datetime.datetime.now()

                    role_mas_tmp.save()


                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010701"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010702"
            logger.error("post method error code:", rtn_code)
            logger.error(role_mas_tmp_form.errors)

            return render(request, "kernal/role_mas_tmp_add.html",
                          {"role_mas_tmp_form": role_mas_tmp_form, "errors": role_mas_tmp_form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")
        role_mas_tmp_form = Role_mas_tmp_form()
        role_mas_tmp_form.func = "role_mas_tmp_add"

        logger.info("get method end")

        logger.info("-------------------------- ended --------------------------")
        return render(request, "kernal/role_mas_tmp_add.html",
                      {
                          "role_mas_tmp_form": role_mas_tmp_form
                      }
                      )


@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_amd(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    role_mas_tmp = Role_mas_tmp.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        role_mas_tmp_form = Role_mas_tmp_form(request.POST)

        if role_mas_tmp_form.is_valid():
            role_mas_tmp_cd = role_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    role_mas_tmp.role_name = role_mas_tmp_cd["role_name"]
                    role_mas_tmp.role_desc = role_mas_tmp_cd["role_desc"]
                    role_mas_tmp.email = role_mas_tmp_cd["email"]
                    role_mas_tmp.handphone = role_mas_tmp_cd["handphone"]
                    role_mas_tmp.status = role_mas_tmp_cd["status"]

                    ####################
                    # 系统管理字段，自动赋值  #role
                    ####################
                    #role_mas_tmp.ver_no = cif_mas_tmp.ver_no + 1
                    role_mas_tmp.prod = "Cif_mas"
                    role_mas_tmp.func = sys._getframe().f_code.co_name
                    role_mas_tmp.maker = request.user.username
                    role_mas_tmp.inp_date = datetime.datetime.now()
                    role_mas_tmp.checker = ""
                    role_mas_tmp.app_date = datetime.datetime.now()
                    role_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010801"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010802"
            logger.error("post method error code:", rtn_code)
            logger.error(role_mas_tmp_form.errors)

            return render(request, "kernal/role_mas_tmp_amd.html",
                          {"role_mas_tmp_form": role_mas_tmp_form, "errors": role_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        print("=====%s===%s==" % (role_mas_tmp.role_name, role_mas_tmp.role_desc))
        role_mas_tmp_form = Role_mas_tmp_form(initial={
            "id": role_mas_tmp.id,
            "role_name": role_mas_tmp.role_name,
            "role_desc": role_mas_tmp.role_desc,
            "email": role_mas_tmp.email,
            "handphone": role_mas_tmp.handphone,
            "func": sys._getframe().f_code.co_name,
            "status": role_mas_tmp.status
        })
        logger.info("get method end")
        logger.info("-------------------------- ended --------------------------")
        return render(request, "kernal/role_mas_tmp_amd.html",
                      {
                          "role_mas_tmp_form": role_mas_tmp_form
                      })


@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_del(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                role_mas_tmp = Role_mas_tmp.objects.get(id=id)
                role_mas_tmp.delete()

                if func == "role_mas_tmp_lst":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/role_mas_tmp_lst/", rtn_code)
                    return HttpResponseRedirect('/kernal/role_mas_tmp_lst/')
        except Exception as e:
            rtn_code = "0s0901"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_lst(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("get method start")

    role_mas_tmp_lst = Role_mas_tmp.objects.filter(status__in=['D', 'A', 'C'])

    paginator = Paginator(role_mas_tmp_lst, 14)
    page = request.GET.get('page')
    try:

        current_page = paginator.page(page)
        role_mas_tmp_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        role_mas_tmp_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        role_mas_tmp_lst = current_page.object_list

    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/role_mas_tmp_lst.html", {"role_mas_tmp_lst": role_mas_tmp_lst, "page": current_page})


@login_required(login_url='/account/login/')
def role_mas_tmp_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    role_mas_tmp_form = get_object_or_404(Role_mas_tmp, id=id)
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/role_mas_tmp_dsp.html", {"role_mas_tmp_form": role_mas_tmp_form})


@login_required(login_url='/account/login/')
@csrf_exempt
# 从主档中取数据，然后插入临时档
def role_mas_tmp_amd2lvl(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    role_mas = Role_mas.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        role_mas_tmp_form = Role_mas_tmp_form(request.POST)
        role_mas_tmp = Role_mas_tmp()

        if role_mas_tmp_form.is_valid():
            role_mas_tmp_cd = role_mas_tmp_form.cleaned_data
            try:
                with transaction.atomic():

                    role_mas_tmp.role_name = role_mas_tmp_cd["role_name"]
                    role_mas_tmp.role_desc = role_mas_tmp_cd["role_desc"]
                    role_mas_tmp.email = role_mas_tmp_cd["email"]
                    role_mas_tmp.handphone = role_mas_tmp_cd["handphone"]
                    role_mas_tmp.status = role_mas_tmp_cd["status"]
                    # role_mas_tmp = Role_mas_tmp_form.save(commit=False)

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    role_mas_tmp.ver_no = role_mas.ver_no + 1
                    role_mas_tmp.prod = "Role_mas"
                    role_mas_tmp.func = sys._getframe().f_code.co_name
                    role_mas_tmp.maker = request.user.username
                    role_mas_tmp.inp_date = datetime.datetime.now()
                    role_mas_tmp.checker = ""
                    role_mas_tmp.app_date = datetime.datetime.now()

                    role_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011201"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011202"
            logger.error("post method error code:", rtn_code)
            logger.error(role_mas_tmp_form.errors)

            return render(request, "kernal/role_mas_tmp_amd.html",
                          {"role_mas_tmp_form": role_mas_tmp_form, "errors": role_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        role_mas_tmp_form = Role_mas_tmp_form(initial=
        {
            "id": role_mas.id,
            "role_name": role_mas.role_name,
            "role_desc": role_mas.role_desc,
            "email": role_mas.email,
            "handphone": role_mas.handphone,
            "func": sys._getframe().f_code.co_name,
            "status": role_mas.status
        })
        logger.info("get method end")
        return render(request, "kernal/role_mas_tmp_amd.html",
                      {
                          "role_mas_tmp_form": role_mas_tmp_form
                      })
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_del2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                role_mas = Role_mas.objects.get(id=id)
                role_mas_tmp = Role_mas_tmp()

                logger.info("post method")
                # role_mas_tmp.id =
                role_mas_tmp.role_name = role_mas.role_name
                role_mas_tmp.role_desc = role_mas.role_desc
                role_mas_tmp.email = role_mas.email
                role_mas_tmp.handphone = role_mas.handphone
                role_mas_tmp.status = "D"

                ####################
                # 系统管理字段，自动赋值  #
                ####################
                role_mas_tmp.ver_no = int(role_mas.ver_no) + 1

                role_mas_tmp.prod = "Role_mas"
                role_mas_tmp.func = sys._getframe().f_code.co_name
                role_mas_tmp.maker = request.user.username
                role_mas_tmp.inp_date = datetime.datetime.now()
                role_mas_tmp.checker = ""
                role_mas_tmp.app_date = datetime.datetime.now()

                role_mas_tmp.save()

                if func == "role_mas_lst2lvl" or func == "role_mas_dsp":
                    logger.info("======112")
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponse("000000")
                else:
                    logger.info("======113")
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/role_mas_lst/", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponseRedirect('/kernal/role_mas_lst/')
        except Exception as e:
            rtn_code = "011301"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def role_mas_tmp_app(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    role_mas_tmp = Role_mas_tmp.objects.get(id=id)
    role_mas_cnt = Role_mas.objects.filter(role_name=role_mas_tmp.role_name).count()

    logger.info("Role_mas_cnt:%d", role_mas_cnt)

    if role_mas_cnt >= 1:
        role_mas = Role_mas.objects.get(role_name=role_mas_tmp.role_name)
    else:
        role_mas = Role_mas()

    logger.info("Role_mas_cnt:%d", role_mas_cnt)
    role_log = Role_log()

    if request.method == "POST":
        logger.info("post method")

        role_mas_form = Role_mas_form(request.POST)

        if role_mas_form.is_valid():

            # if (Role_mas_tmp.maker == request.user.username):
            #     logger.info("================136")  ################
            #     print(request.user.username)
            #     print(Role_mas_tmp.maker)
            #     return render(request, "kernal/role_mas_tmp_app.html",
            #                   {"Role_mas_tmp_Form": Role_mas_tmp_Form,
            #                    "errors": Role_mas_tmp_Form.errors})
            #     # print("=======================1")

            # Role_mas_tmp_cd = role_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    # 防中间人篡改，复核人员不得修改数据
                    role_mas.role_name = role_mas_tmp.role_name
                    role_mas.role_desc = role_mas_tmp.role_desc
                    role_mas.email = role_mas_tmp.email
                    role_mas.handphone = role_mas_tmp.handphone
                    role_mas.status = role_mas_tmp.status

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    role_mas.ver_no = role_mas_tmp.ver_no
                    role_mas.prod = "Role_mas"
                    role_mas.func = sys._getframe().f_code.co_name
                    role_mas.maker = role_mas_tmp.maker
                    role_mas.inp_date = role_mas_tmp.inp_date
                    role_mas.checker = request.user.username
                    role_mas.app_date = datetime.datetime.now()
                    ############################
                    # 系统日志管理字段，自动赋值  #
                    ############################
                    role_log.role_name = role_mas_tmp.role_name
                    role_log.role_desc = role_mas_tmp.role_desc
                    role_log.email = role_mas_tmp.email
                    role_log.handphone = role_mas_tmp.handphone
                    role_log.logstatus = role_mas_tmp.status
                    role_log.ver_no = role_mas.ver_no
                    role_log.prod = role_mas.prod
                    role_log.func = role_mas.func
                    role_log.maker = role_mas.maker
                    role_log.inp_date = role_mas.inp_date
                    role_log.checker = role_mas.checker
                    role_log.app_date = role_mas.app_date

                    role_mas.save()
                    role_mas_tmp.delete()
                    role_log.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011401"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011402"
            logger.error("post method error code:", rtn_code)
            logger.error(role_mas_form.errors)

            return render(request, "kernal/role_mas_tmp_app.html",
                          {"role_mas_form": role_mas_form, "errors": role_mas_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        role_mas_form = Role_mas_form(initial={
            "id": role_mas_tmp.id,
            "role_name": role_mas_tmp.role_name,
            "role_desc": role_mas_tmp.role_desc,
            "email": role_mas_tmp.email,
            "handphone": role_mas_tmp.handphone,
            "status": role_mas_tmp.status,
            "ver_no": role_mas_tmp.ver_no,
            "prod": role_mas_tmp.prod,
            "func": role_mas_tmp.func,
            "maker": role_mas_tmp.maker,
            "checker": "---",
            "inp_date": role_mas_tmp.inp_date,
            "app_date": role_mas_tmp.app_date
        })
        return render(request, "kernal/role_mas_tmp_app.html",
                      {
                          "role_mas_form": role_mas_form
                      })
    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")

###############################
# 二级交易 菜单管理
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_lst2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    menu_mas_lst = Menu_mas.objects.filter(status__in=["A", "C", "D"])
    paginator = Paginator(menu_mas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        menu_mas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        menu_mas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        menu_mas_lst = current_page.object_list

    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/menu_mas_lst2lvl.html", {"menu_mas_lst": menu_mas_lst, "page": current_page})


@login_required(login_url='/account/login/')
def menu_mas_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    menu_mas_form = get_object_or_404(Menu_mas, id=id)
    #menu_mas = Menu_mas.objects.get(id=id)

    logger.info("get method end")

    logger.info("------------------------- ended --------------------------")
    return render(request, "kernal/menu_mas_dsp.html", {"menu_mas_form": menu_mas_form})

@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_add(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        menu_mas_tmp_form = Menu_mas_tmp_form(request.POST)

        logger.info("post method")
        if menu_mas_tmp_form.is_valid():

            try:
                with transaction.atomic():
                    menu_mas_tmp = menu_mas_tmp_form.save(commit=False)

                    logger.info("==========115")

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    menu_mas_tmp.ver_no = 1
                    menu_mas_tmp.prod = "Menu_mas"
                    menu_mas_tmp.func = sys._getframe().f_code.co_name
                    menu_mas_tmp.maker = request.user.username
                    menu_mas_tmp.inp_date = datetime.datetime.now()
                    menu_mas_tmp.checker = ""
                    menu_mas_tmp.app_date = datetime.datetime.now()
                    menu_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/menu_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010701"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010702"
            logger.error("post method error code:", rtn_code)
            logger.error(menu_mas_tmp_form.errors)

            return render(request, "kernal/menu_mas_tmp_add.html",
                          {"menu_mas_tmp_form": menu_mas_tmp_form, "errors": menu_mas_tmp_form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")
        menu_mas_tmp_form = Menu_mas_tmp_form()
        menu_mas_tmp_form.func = "menu_mas_tmp_add"

        logger.info("get method end")

        logger.info("-------------------------- ended --------------------------")
        return render(request, "kernal/menu_mas_tmp_add.html",
                      {
                          "menu_mas_tmp_form": menu_mas_tmp_form,
                      }
                      )


@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_amd(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    menu_mas_tmp = Menu_mas_tmp.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        menu_mas_tmp_form = Menu_mas_tmp_form(request.POST)

        if menu_mas_tmp_form.is_valid():
            menu_mas_tmp_cd = menu_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    menu_mas_tmp.menu_lvl = menu_mas_tmp_cd["menu_lvl"]
                    menu_mas_tmp.menu_parent_id = menu_mas_tmp_cd["menu_parent_id"]
                    menu_mas_tmp.menu_name = menu_mas_tmp_cd["menu_name"]
                    menu_mas_tmp.menu_sht_desc = menu_mas_tmp_cd["menu_sht_desc"]
                    menu_mas_tmp.menu_long_desc = menu_mas_tmp_cd["menu_long_desc"]
                    menu_mas_tmp.status = menu_mas_tmp_cd["status"]

                    ####################
                    # 系统管理字段，自动赋值  #menu
                    ####################
                    menu_mas_tmp.ver_no = menu_mas_tmp.ver_no + 1
                    menu_mas_tmp.prod = "Menu_mas"
                    menu_mas_tmp.func = sys._getframe().f_code.co_name
                    menu_mas_tmp.maker = request.user.username
                    menu_mas_tmp.inp_date = datetime.datetime.now()
                    menu_mas_tmp.checker = ""
                    menu_mas_tmp.app_date = datetime.datetime.now()
                    menu_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/menu_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010801"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010802"
            logger.error("post method error code:", rtn_code)
            logger.error(menu_mas_tmp_form.errors)

            return render(request, "kernal/menu_mas_tmp_amd.html",
                          {"menu_mas_tmp_form": menu_mas_tmp_form, "errors": menu_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        menu_mas_tmp_form = Menu_mas_tmp_form(initial={
            "id": menu_mas_tmp.id,
            "menu_lvl": menu_mas_tmp.menu_lvl,
            "menu_parent_id": menu_mas_tmp.menu_parent_id,
            "menu_name": menu_mas_tmp.menu_name,
            "menu_sht_desc": menu_mas_tmp.menu_sht_desc,
            "menu_long_desc": menu_mas_tmp.menu_long_desc,
            "status": menu_mas_tmp.status,
            "func": sys._getframe().f_code.co_name,
        })
        logger.info("get method end")
        logger.info("-------------------------- ended --------------------------")
        return render(request, "kernal/menu_mas_tmp_amd.html",
                      {
                          "menu_mas_tmp_form": menu_mas_tmp_form
                      })


@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_del(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                menu_mas_tmp = Menu_mas_tmp.objects.get(id=id)
                menu_mas_tmp.delete()

                if func == "menu_mas_tmp_lst":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/menu_mas_tmp_lst/", rtn_code)
                    return HttpResponseRedirect('/kernal/menu_mas_tmp_lst/')
        except Exception as e:
            rtn_code = "0s0901"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_lst(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("get method start")

    menu_mas_tmp_lst = Menu_mas_tmp.objects.filter(status__in=['D', 'A', 'C'])

    paginator = Paginator(menu_mas_tmp_lst, 14)
    page = request.GET.get('page')
    try:

        current_page = paginator.page(page)
        menu_mas_tmp_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        menu_mas_tmp_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        menu_mas_tmp_lst = current_page.object_list

    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/menu_mas_tmp_lst.html", {"menu_mas_tmp_lst": menu_mas_tmp_lst, "page": current_page})


@login_required(login_url='/account/login/')
def menu_mas_tmp_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    menu_mas_tmp_form = get_object_or_404(Menu_mas_tmp, id=id)
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/menu_mas_tmp_dsp.html", {"menu_mas_tmp_form": menu_mas_tmp_form})


@login_required(login_url='/account/login/')
@csrf_exempt
# 从主档中取数据，然后插入临时档
def menu_mas_tmp_amd2lvl(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    menu_mas = Menu_mas.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        menu_mas_tmp_form = Menu_mas_tmp_form(request.POST)
        menu_mas_tmp = Menu_mas_tmp()

        if menu_mas_tmp_form.is_valid():
            menu_mas_tmp_cd = menu_mas_tmp_form.cleaned_data
            try:
                with transaction.atomic():

                    menu_mas_tmp.menu_lvl = menu_mas_tmp_cd["menu_lvl"]
                    menu_mas_tmp.menu_parent_id = menu_mas_tmp_cd["menu_parent_id"]
                    menu_mas_tmp.menu_name = menu_mas_tmp_cd["menu_name"]
                    menu_mas_tmp.menu_sht_desc = menu_mas_tmp_cd["menu_sht_desc"]
                    menu_mas_tmp.menu_long_desc = menu_mas_tmp_cd["menu_long_desc"]
                    menu_mas_tmp.status = menu_mas_tmp_cd["status"]
                    # menu_mas_tmp = Menu_mas_tmp_form.save(commit=False)

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    menu_mas_tmp.ver_no = menu_mas.ver_no + 1
                    menu_mas_tmp.prod = "Menu_mas"
                    menu_mas_tmp.func = sys._getframe().f_code.co_name
                    menu_mas_tmp.maker = request.user.username
                    menu_mas_tmp.inp_date = datetime.datetime.now()
                    menu_mas_tmp.checker = ""
                    menu_mas_tmp.app_date = datetime.datetime.now()

                    menu_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/menu_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011201"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011202"
            logger.error("post method error code:", rtn_code)
            logger.error(menu_mas_tmp_form.errors)

            return render(request, "kernal/menu_mas_tmp_amd.html",
                          {"menu_mas_tmp_form": menu_mas_tmp_form, "errors": menu_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        menu_mas_tmp_form = Menu_mas_tmp_form(initial=
        {
            "id": menu_mas.id,
            "menu_lvl": menu_mas.menu_lvl,
            "menu_parent_id": menu_mas.menu_parent_id,
            "menu_name": menu_mas.menu_name,
            "menu_sht_desc": menu_mas.menu_sht_desc,
            "menu_long_desc": menu_mas.menu_long_desc,
            "status": menu_mas.status,
            "func": sys._getframe().f_code.co_name,
        })
        logger.info("get method end")
        return render(request, "kernal/menu_mas_tmp_amd.html",
                      {
                          "menu_mas_tmp_form": menu_mas_tmp_form
                      })
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_del2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        logger.info("===================1111")

        try:
            with transaction.atomic():
                menu_mas = Menu_mas.objects.get(id=id)

                logger.info(menu_mas.menu_name)
                menu_mas_tmp_count = Menu_mas_tmp.objects.filter(menu_name=menu_mas.menu_name).count()
                logger.info(menu_mas_tmp_count)

                if menu_mas_tmp_count > 1:
                    rtn_code = "000001"
                    return HttpResponse(rtn_code)

                menu_mas_tmp = Menu_mas_tmp()

                # menu_mas_tmp.id =
                menu_mas_tmp.menu_lvl = menu_mas.menu_lvl
                menu_mas_tmp.menu_parent_id = menu_mas.menu_parent_id
                menu_mas_tmp.menu_name = menu_mas.menu_name
                menu_mas_tmp.menu_sht_desc = menu_mas.menu_sht_desc
                menu_mas_tmp.menu_long_desc = menu_mas.menu_long_desc
                menu_mas_tmp.status = "D"

                ####################
                # 系统管理字段，自动赋值  #
                ####################
                menu_mas_tmp.ver_no = int(menu_mas.ver_no) + 1

                menu_mas_tmp.prod = "Menu_mas"
                menu_mas_tmp.func = sys._getframe().f_code.co_name
                menu_mas_tmp.maker = request.user.username
                menu_mas_tmp.inp_date = datetime.datetime.now()
                menu_mas_tmp.checker = ""
                menu_mas_tmp.app_date = datetime.datetime.now()

                menu_mas_tmp.save()

                logger.info(func)

                if func == "menu_mas_lst2lvl" or func == "menu_mas_dsp":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/menu_mas_lst/", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponseRedirect('/kernal/menu_mas_lst/')
        except Exception as e:
            rtn_code = "011301"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def menu_mas_tmp_app(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    menu_mas_tmp = Menu_mas_tmp.objects.get(id=id)
    menu_mas_cnt = Menu_mas.objects.filter(menu_name=menu_mas_tmp.menu_name).count()

    logger.info("Menu_mas_cnt:%d", menu_mas_cnt)

    if menu_mas_cnt >= 1:
        menu_mas = Menu_mas.objects.get(menu_name=menu_mas_tmp.menu_name)
    else:
        menu_mas = Menu_mas()

    logger.info("Menu_mas_cnt:%d", menu_mas_cnt)
    menu_log = Menu_log()

    if request.method == "POST":
        logger.info("post method")

        menu_mas_form = Menu_mas_form(request.POST)

        if menu_mas_form.is_valid():

            # if (Menu_mas_tmp.maker == request.user.username):
            #     logger.info("================136")  ################
            #     print(request.user.username)
            #     print(Menu_mas_tmp.maker)
            #     return render(request, "kernal/menu_mas_tmp_app.html",
            #                   {"Menu_mas_tmp_Form": Menu_mas_tmp_Form,
            #                    "errors": Menu_mas_tmp_Form.errors})
            #     # print("=======================1")

            # Menu_mas_tmp_cd = menu_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    # 防中间人篡改，复核人员不得修改数据
                    menu_mas.menu_lvl = menu_mas_tmp.menu_lvl
                    menu_mas.menu_parent_id = menu_mas_tmp.menu_parent_id
                    menu_mas.menu_name = menu_mas_tmp.menu_name
                    menu_mas.menu_sht_desc = menu_mas_tmp.menu_sht_desc
                    menu_mas.menu_long_desc = menu_mas_tmp.menu_long_desc
                    menu_mas.status = menu_mas_tmp.status

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    menu_mas.ver_no = menu_mas_tmp.ver_no
                    menu_mas.prod = "Menu_mas"
                    menu_mas.func = sys._getframe().f_code.co_name
                    menu_mas.maker = menu_mas_tmp.maker
                    menu_mas.inp_date = menu_mas_tmp.inp_date
                    menu_mas.checker = request.user.username
                    menu_mas.app_date = datetime.datetime.now()
                    ############################
                    # 系统日志管理字段，自动赋值  #
                    ############################
                    menu_log.menu_lvl = menu_mas_tmp.menu_lvl
                    menu_log.menu_parent_id = menu_mas_tmp.menu_parent_id
                    menu_log.menu_name = menu_mas_tmp.menu_name
                    menu_log.menu_sht_desc = menu_mas_tmp.menu_sht_desc
                    menu_log.menu_long_desc = menu_mas_tmp.menu_long_desc
                    menu_log.status = menu_mas_tmp.status
                    menu_log.ver_no = menu_mas.ver_no
                    menu_log.prod = menu_mas.prod
                    menu_log.func = menu_mas.func
                    menu_log.maker = menu_mas.maker
                    menu_log.inp_date = menu_mas.inp_date
                    menu_log.checker = menu_mas.checker
                    menu_log.app_date = menu_mas.app_date

                    menu_mas.save()
                    menu_mas_tmp.delete()
                    menu_log.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/menu_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011401"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011402"
            logger.error("post method error code:", rtn_code)
            logger.error(menu_mas_form.errors)

            return render(request, "kernal/menu_mas_tmp_app.html",
                          {"menu_mas_form": menu_mas_form, "errors": menu_mas_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        menu_mas_form = Menu_mas_form(initial={
            "id": menu_mas_tmp.id,
            "menu_lvl": menu_mas_tmp.menu_lvl,
            "menu_parent_id": menu_mas_tmp.menu_parent_id,
            "menu_name": menu_mas_tmp.menu_name,
            "menu_sht_desc": menu_mas_tmp.menu_sht_desc,
            "menu_long_desc": menu_mas_tmp.menu_long_desc,
            "status": menu_mas_tmp.status,
            "func": sys._getframe().f_code.co_name
        })
        return render(request, "kernal/menu_mas_tmp_app.html",
                      {
                          "menu_mas_form": menu_mas_form
                      })
    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")

###############################
# 二级交易 用户角色及菜单关系
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_lst2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    user_role_mas_lst = User_role_mas.objects.filter(status__in=["A", "C", "D"])
    paginator = Paginator(user_role_mas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        user_role_mas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        user_role_mas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        user_role_mas_lst = current_page.object_list

    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_role_mas_lst2lvl.html", {"user_role_mas_lst": user_role_mas_lst, "page": current_page})


@login_required(login_url='/account/login/')
def user_role_mas_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    user_role_mas_form = get_object_or_404(User_role_mas, id=id)
    #user_role_mas = User_role_mas.objects.get(id=id)

    logger.info("get method end")

    logger.info("------------------------- ended --------------------------")
    return render(request, "kernal/user_role_mas_dsp.html", {"user_role_mas_form": user_role_mas_form})

@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_add(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        user_role_mas_tmp_form = User_role_mas_tmp_form(request.POST)
        # print(user_role_mas_tmp_form.status)
        # print(user_role_mas_tmp_form.user_role_name)

        var_username = request.POST['username_list']
        var_role_name = request.POST['role_name_list']
        logger.info(var_username)
        logger.info(var_role_name)

        if user_role_mas_tmp_form.is_valid():

            try:
                with transaction.atomic():
                    user_role_mas_tmp = user_role_mas_tmp_form.save(commit=False)
                    #print(user_role_mas_tmp.user_role_name)
                    role_mas = Role_mas.objects.get(role_name=var_role_name)
                    user_role_mas_tmp.role = role_mas

                    user = User.objects.get(username=var_username)
                    user_role_mas_tmp.user = user

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    user_role_mas_tmp.ver_no = 1
                    user_role_mas_tmp.prod = "User_role_mas"
                    user_role_mas_tmp.func = sys._getframe().f_code.co_name
                    user_role_mas_tmp.maker = request.user.username
                    user_role_mas_tmp.inp_date = datetime.datetime.now()
                    user_role_mas_tmp.checker = ""
                    user_role_mas_tmp.app_date = datetime.datetime.now()
                    user_role_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")

                    return HttpResponseRedirect('/kernal/user_role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010701"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010702"
            logger.error("post method error code:", rtn_code)
            logger.error(user_role_mas_tmp_form.errors)

            return render(request, "kernal/user_role_mas_tmp_add.html",
                          {"user_role_mas_tmp_form": user_role_mas_tmp_form, "errors": user_role_mas_tmp_form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")

        # # 0. 初始化菜单
        # user_role_mas = User_role_mas.objects.get(user=request.user.id)
        # role_mas = Role_mas.objects.get(id=user_role_mas.role.id)
        # auth_role_mas_lst = Role_mas.objects.filter(role_name=role_mas.role_name)
        # auth_role_mas_lst_lvl3 = auth_role_mas_lst
        # for role_mas in auth_role_mas_lst:
        #     logger.info(role_mas.menu.menu_name)
        #     logger.info(role_mas.menu.menu_long_desc)


        # 1. 初始化 User_role_mas_tmp_form
        # user_role_mas_tmp_form = User_role_mas_tmp_form()
        # user_role_mas_tmp_form.func = "user_role_mas_tmp_add"
        user_role_mas_tmp_form = User_role_mas_tmp_form(initial={
            "user_role_name": "",
            "status": "A",
            "func": sys._getframe().f_code.co_name,
        })

        # 2. 初始化 role_name
        role_mas_collect = Role_mas.objects.all()
        role_name_list = []
        for role_mas in role_mas_collect:
            role_name_list.append(role_mas.role_name)

        # 3. 初始化 username
        auth_user_collect = User.objects.all()
        username_list = []
        for user in auth_user_collect:
            username_list.append(user.username)

        logger.info("get method end")

        logger.info("-------------------------- ended --------------------------")

        return render(request, "kernal/user_role_mas_tmp_add.html",
                      {
                          "user_role_mas_tmp_form": user_role_mas_tmp_form,
                          "role_name_list": role_name_list,
                          "username_list": username_list,
                      }
                      )

        # return render(request, "kernal/user_role_mas_tmp_add.html",
        #               {
        #                   "user_role_mas_tmp_form": user_role_mas_tmp_form,
        #                   "role_name_list": role_name_list,
        #                   "username_list": username_list,
        #                   "auth_role_mas_lst": auth_role_mas_lst,
        #                   "auth_role_mas_lst_lvl3": auth_role_mas_lst_lvl3,
        #               }
        #               )
        # return render(request, "kernal/user_role_mas_tmp_add.html",
        #               {
        #                   "user_role_mas_tmp_form": user_role_mas_tmp_form
        #               }
        #               )

@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_amd(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_role_mas_tmp = User_role_mas_tmp.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        user_role_mas_tmp_form = User_role_mas_tmp_form(request.POST)
        var_username = request.POST['username_list']
        var_role_name = request.POST['role_name_list']

        if user_role_mas_tmp_form.is_valid():
            user_role_mas_tmp_cd = user_role_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    user_role_mas_tmp.user_role_name = user_role_mas_tmp_cd["user_role_name"]
                    user_role_mas_tmp.status = user_role_mas_tmp_cd["status"]

                    user = User.objects.get(username=var_username)
                    user_role_mas_tmp.user = user

                    role_mas = Role_mas.objects.get(role_name=var_role_name)
                    user_role_mas_tmp.role = role_mas

                    ####################
                    # 系统管理字段，自动赋值  #menu
                    ####################
                    user_role_mas_tmp.ver_no = user_role_mas_tmp.ver_no + 1
                    user_role_mas_tmp.prod = "User_role_mas"
                    user_role_mas_tmp.func = sys._getframe().f_code.co_name
                    user_role_mas_tmp.maker = request.user.username
                    user_role_mas_tmp.inp_date = datetime.datetime.now()
                    user_role_mas_tmp.checker = ""
                    user_role_mas_tmp.app_date = datetime.datetime.now()
                    user_role_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010801"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010802"
            logger.error("post method error code:", rtn_code)
            logger.error(user_role_mas_tmp_form.errors)

            return render(request, "kernal/user_role_mas_tmp_amd.html",
                          {"user_role_mas_tmp_form": user_role_mas_tmp_form, "errors": user_role_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        # 1. 初始化 User_role_mas_tmp_form
        user_role_mas_tmp_form = User_role_mas_tmp_form(initial={
            "id": user_role_mas_tmp.id,
            "user_role_name": user_role_mas_tmp.user_role_name,
            "status": user_role_mas_tmp.status,
            "func": sys._getframe().f_code.co_name,
        })

        # 2. 初始化 role_name
        role_mas_collect = Role_mas.objects.all()
        role_name_list = []
        for role_mas in role_mas_collect:
            role_name_list.append(role_mas.role_name)

        # 3. 初始化 username
        auth_user_collect = User.objects.all()
        username_list = []
        for user in auth_user_collect:
            username_list.append(user.username)

        logger.info("get method end")
        logger.info("-------------------------- ended --------------------------")
        return render(request, "kernal/user_role_mas_tmp_add.html",
                      {
                          "user_role_mas_tmp_form": user_role_mas_tmp_form,
                          "role_name_list": role_name_list,
                          "username_list": username_list
                      }
                      )

        # return render(request, "kernal/user_role_mas_tmp_amd.html",
        #               {
        #                   "user_role_mas_tmp_form": user_role_mas_tmp_form
        #               })


@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_del(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                user_role_mas_tmp = User_role_mas_tmp.objects.get(id=id)
                user_role_mas_tmp.delete()

                if func == "user_role_mas_tmp_lst":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/user_role_mas_tmp_lst/", rtn_code)
                    return HttpResponseRedirect('/kernal/user_role_mas_tmp_lst/')
        except Exception as e:
            rtn_code = "0s0901"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_lst(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("get method start")

    #user_role_mas_tmp_lst = User_role_mas_tmp.objects.filter(status__in=['D', 'A', 'C'])
    user_role_mas_tmp_lst = User_role_mas_tmp.objects.all()

    paginator = Paginator(user_role_mas_tmp_lst, 14)
    page = request.GET.get('page')
    try:

        current_page = paginator.page(page)
        user_role_mas_tmp_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        user_role_mas_tmp_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        user_role_mas_tmp_lst = current_page.object_list

    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_role_mas_tmp_lst.html", {"user_role_mas_tmp_lst": user_role_mas_tmp_lst, "page": current_page})


@login_required(login_url='/account/login/')
def user_role_mas_tmp_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    user_role_mas_tmp_form = get_object_or_404(User_role_mas_tmp, id=id)
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_role_mas_tmp_dsp.html", {"user_role_mas_tmp_form": user_role_mas_tmp_form})


@login_required(login_url='/account/login/')
@csrf_exempt
# 从主档中取数据，然后插入临时档
def user_role_mas_tmp_amd2lvl(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_role_mas = User_role_mas.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        user_role_mas_tmp_form = User_role_mas_tmp_form(request.POST)
        user_role_mas_tmp = User_role_mas_tmp()

        if user_role_mas_tmp_form.is_valid():
            user_role_mas_tmp_cd = user_role_mas_tmp_form.cleaned_data
            try:
                with transaction.atomic():

                    user_role_mas_tmp.menu_lvl = user_role_mas_tmp_cd["menu_lvl"]
                    user_role_mas_tmp.menu_parent_id = user_role_mas_tmp_cd["menu_parent_id"]
                    user_role_mas_tmp.menu_name = user_role_mas_tmp_cd["menu_name"]
                    user_role_mas_tmp.menu_sht_desc = user_role_mas_tmp_cd["menu_sht_desc"]
                    user_role_mas_tmp.menu_long_desc = user_role_mas_tmp_cd["menu_long_desc"]
                    user_role_mas_tmp.status = user_role_mas_tmp_cd["status"]
                    # user_role_mas_tmp = User_role_mas_tmp_form.save(commit=False)

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    user_role_mas_tmp.ver_no = user_role_mas.ver_no + 1
                    user_role_mas_tmp.prod = "User_role_mas"
                    user_role_mas_tmp.func = sys._getframe().f_code.co_name
                    user_role_mas_tmp.maker = request.user.username
                    user_role_mas_tmp.inp_date = datetime.datetime.now()
                    user_role_mas_tmp.checker = ""
                    user_role_mas_tmp.app_date = datetime.datetime.now()

                    user_role_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011201"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011202"
            logger.error("post method error code:", rtn_code)
            logger.error(user_role_mas_tmp_form.errors)

            return render(request, "kernal/user_role_mas_tmp_amd.html",
                          {"user_role_mas_tmp_form": user_role_mas_tmp_form, "errors": user_role_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        user_role_mas_tmp_form = User_role_mas_tmp_form(initial=
        {
            "id": user_role_mas.id,
            "menu_lvl": user_role_mas.menu_lvl,
            "menu_parent_id": user_role_mas.menu_parent_id,
            "menu_name": user_role_mas.menu_name,
            "menu_sht_desc": user_role_mas.menu_sht_desc,
            "menu_long_desc": user_role_mas.menu_long_desc,
            "status": user_role_mas.status,
            "func": sys._getframe().f_code.co_name,
        })
        logger.info("get method end")
        return render(request, "kernal/user_role_mas_tmp_amd.html",
                      {
                          "user_role_mas_tmp_form": user_role_mas_tmp_form
                      })
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_del2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        logger.info("===================1111")

        try:
            with transaction.atomic():
                user_role_mas = User_role_mas.objects.get(id=id)

                logger.info(user_role_mas.menu_name)
                user_role_mas_tmp_count = User_role_mas_tmp.objects.filter(menu_name=user_role_mas.menu_name).count()
                logger.info(user_role_mas_tmp_count)

                if user_role_mas_tmp_count > 1:
                    rtn_code = "000001"
                    return HttpResponse(rtn_code)

                user_role_mas_tmp = User_role_mas_tmp()

                # user_role_mas_tmp.id =
                user_role_mas_tmp.menu_lvl = user_role_mas.menu_lvl
                user_role_mas_tmp.menu_parent_id = user_role_mas.menu_parent_id
                user_role_mas_tmp.menu_name = user_role_mas.menu_name
                user_role_mas_tmp.menu_sht_desc = user_role_mas.menu_sht_desc
                user_role_mas_tmp.menu_long_desc = user_role_mas.menu_long_desc
                user_role_mas_tmp.status = "D"

                ####################
                # 系统管理字段，自动赋值  #
                ####################
                user_role_mas_tmp.ver_no = int(user_role_mas.ver_no) + 1

                user_role_mas_tmp.prod = "User_role_mas"
                user_role_mas_tmp.func = sys._getframe().f_code.co_name
                user_role_mas_tmp.maker = request.user.username
                user_role_mas_tmp.inp_date = datetime.datetime.now()
                user_role_mas_tmp.checker = ""
                user_role_mas_tmp.app_date = datetime.datetime.now()

                user_role_mas_tmp.save()

                logger.info(func)

                if func == "user_role_mas_lst2lvl" or func == "user_role_mas_dsp":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/user_role_mas_lst/", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponseRedirect('/kernal/user_role_mas_lst/')
        except Exception as e:
            rtn_code = "011301"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_role_mas_tmp_app(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_role_mas_tmp = User_role_mas_tmp.objects.get(id=id)
    user_role_mas_cnt = User_role_mas.objects.filter(user=user_role_mas_tmp.user, role=user_role_mas_tmp.role).count()

    logger.info("User_role_mas_cnt:%d", user_role_mas_cnt)

    if user_role_mas_cnt >= 1:
        user_role_mas = User_role_mas.objects.get(user=user_role_mas_tmp.user, role=user_role_mas_tmp.role)
    else:
        user_role_mas = User_role_mas()

    logger.info("User_role_mas_cnt:%d", user_role_mas_cnt)
    user_role_log = User_role_log()

    if request.method == "POST":
        logger.info("post method")

        user_role_mas_form = User_role_mas_form(request.POST)

        if user_role_mas_form.is_valid():

            # if (User_role_mas_tmp.maker == request.user.username):
            #     logger.info("================136")  ################
            #     print(request.user.username)
            #     print(User_role_mas_tmp.maker)
            #     return render(request, "kernal/user_role_mas_tmp_app.html",
            #                   {"User_role_mas_tmp_Form": User_role_mas_tmp_Form,
            #                    "errors": User_role_mas_tmp_Form.errors})
            #     # print("=======================1")

            # User_role_mas_tmp_cd = user_role_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    # 防中间人篡改，复核人员不得修改数据
                    user_role_mas.user = user_role_mas_tmp.user
                    user_role_mas.role = user_role_mas_tmp.role
                    user_role_mas.user_role_name = user_role_mas_tmp.user_role_name
                    user_role_mas.status = user_role_mas_tmp.status

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    user_role_mas.ver_no = user_role_mas_tmp.ver_no
                    user_role_mas.prod = "User_role_mas"
                    user_role_mas.func = sys._getframe().f_code.co_name
                    user_role_mas.maker = user_role_mas_tmp.maker
                    user_role_mas.inp_date = user_role_mas_tmp.inp_date
                    user_role_mas.checker = request.user.username
                    user_role_mas.app_date = datetime.datetime.now()
                    ############################
                    # 系统日志管理字段，自动赋值  #
                    ############################
                    user_role_log.user = user_role_mas_tmp.user
                    user_role_log.role = user_role_mas_tmp.role
                    user_role_log.user_role_name = user_role_mas_tmp.user_role_name
                    user_role_log.status = user_role_mas_tmp.status
                    user_role_log.ver_no = user_role_mas.ver_no
                    user_role_log.prod = user_role_mas.prod
                    user_role_log.func = user_role_mas.func
                    user_role_log.maker = user_role_mas.maker
                    user_role_log.inp_date = user_role_mas.inp_date
                    user_role_log.checker = user_role_mas.checker
                    user_role_log.app_date = user_role_mas.app_date

                    user_role_mas.save()
                    user_role_mas_tmp.delete()
                    user_role_log.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_role_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011401"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011402"
            logger.error("post method error code:", rtn_code)
            logger.error(user_role_mas_form.errors)

            return render(request, "kernal/user_role_mas_tmp_app.html",
                          {"user_role_mas_form": user_role_mas_form, "errors": user_role_mas_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        # 1. 初始化 User_role_mas_form
        user_role_mas_form = User_role_mas_form(initial={
            "id": user_role_mas_tmp.id,
            "user_role_name": user_role_mas_tmp.user_role_name,
            "status": user_role_mas_tmp.status,
            "func": sys._getframe().f_code.co_name
        })
        # 2. 初始化 role_name
        role_mas_collect = Role_mas.objects.all()
        role_name_list = []
        for role_mas in role_mas_collect:
            role_name_list.append(role_mas.role_name)

        # 3. 初始化 username
        auth_user_collect = User.objects.all()
        username_list = []
        for user in auth_user_collect:
            username_list.append(user.username)

        logger.info("get method end")
        return render(request, "kernal/user_role_mas_tmp_app.html",
                      {
                          "user_role_mas_form": user_role_mas_form,
                          "role_name_list": role_name_list,
                          "username_list": username_list
                      }
                      )
        # return render(request, "kernal/user_role_mas_tmp_app.html",
        #               {
        #                   "user_role_mas_form": user_role_mas_form
        #               })

    logger.info("-------------------------- ended --------------------------")


###############################
# 二级交易 用户管理
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_lst2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    user_mas_lst = User_mas.objects.filter(status__in=["A", "C", "D"])
    paginator = Paginator(user_mas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        user_mas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        user_mas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        user_mas_lst = current_page.object_list

    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_mas_lst2lvl.html", {"user_mas_lst": user_mas_lst, "page": current_page})


@login_required(login_url='/account/login/')
def user_mas_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")
    user_mas_form = get_object_or_404(User_mas, id=id)
    #user_mas = User_mas.objects.get(id=id)

    logger.info("get method end")

    logger.info("------------------------- ended --------------------------")
    return render(request, "kernal/user_mas_dsp.html", {"user_mas_form": user_mas_form})

@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_add(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        user_mas_tmp_form = User_mas_tmp_form(request.POST)
        # user_form = UserForm(request.POST)

        # print(s.name)
        # print(user_form.password)
        # var_username = request.POST['username_list']
        # var_role_name = request.POST['role_name_list']
        # logger.info(user_mas_tmp_form.name)
        # logger.info(user_form.password)

        if user_mas_tmp_form.is_valid():

            user_mas_tmp_cd = user_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    user_mas_tmp = user_mas_tmp_form.save(commit=False)

                    # logging(user_mas_tmp.cleaned_data['employee_id'])
                    # logging(user_mas_tmp.cleaned_data['name'])

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    user_mas_tmp.ver_no = 1
                    user_mas_tmp.prod = "User_mas"
                    user_mas_tmp.func = sys._getframe().f_code.co_name
                    user_mas_tmp.maker = request.user.username
                    user_mas_tmp.inp_date = datetime.datetime.now()
                    user_mas_tmp.checker = ""
                    user_mas_tmp.app_date = datetime.datetime.now()
                    user_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")

                    return HttpResponseRedirect('/kernal/user_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010701"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010702"
            logger.error("post method error code:", rtn_code)
            logger.error(user_mas_tmp_form.errors)

            return render(request, "kernal/user_mas_tmp_add.html",
                          {"user_mas_tmp_form": user_mas_tmp_form, "errors": user_mas_tmp_form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")

        # 1. 初始化 User_mas_tmp_form

        user_form = UserForm()
        user_form.func = "user_mas_tmp_add"
        user_form.username = ""
        user_form.password = "12345678"

        user_mas_tmp_form = User_mas_tmp_form(initial={
            "name": "",
            "status": "A",
            "func": sys._getframe().f_code.co_name,
        })

        logger.info("get method end")

        logger.info("-------------------------- ended --------------------------")

        return render(request, "kernal/user_mas_tmp_add.html",
                      {
                          "user_form": user_form,
                          "user_mas_tmp_form": user_mas_tmp_form,
                      }
                      )

@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_amd(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_mas_tmp = User_mas_tmp.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        user_mas_tmp_form = User_mas_tmp_form(request.POST)

        if user_mas_tmp_form.is_valid():
            user_mas_tmp_cd = user_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    user_mas_tmp = user_mas_tmp_form.save(commit=False)

                    ####################
                    # 系统管理字段，自动赋值  #menu
                    ####################
                    user_mas_tmp.ver_no = user_mas_tmp.ver_no + 1
                    user_mas_tmp.prod = "User_mas"
                    user_mas_tmp.func = sys._getframe().f_code.co_name
                    user_mas_tmp.maker = request.user.username
                    user_mas_tmp.inp_date = datetime.datetime.now()
                    user_mas_tmp.checker = ""
                    user_mas_tmp.app_date = datetime.datetime.now()
                    user_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "010801"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010802"
            logger.error("post method error code:", rtn_code)
            logger.error(user_mas_tmp_form.errors)

            return render(request, "kernal/user_mas_tmp_amd.html",
                          {"user_mas_tmp_form": user_mas_tmp_form, "errors": user_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        # 1. 初始化 User_mas_tmp_form
        user_mas_tmp_form = User_mas_tmp_form(initial={
            "id": user_mas_tmp.id,
            "employee_id": user_mas_tmp.employee_id,
            "name": user_mas_tmp.name,
            "on_board_date": user_mas_tmp.on_board_date,
            "address": user_mas_tmp.address,
            "age": user_mas_tmp.age,
            "phone": user_mas_tmp.phone,
            "mobile_phone": user_mas_tmp.mobile_phone,
            "status": user_mas_tmp.status,
            "func": sys._getframe().f_code.co_name,
        })

        logger.info("get method end")
        logger.info("-------------------------- ended --------------------------")

        return render(request, "kernal/user_mas_tmp_amd.html",
                      {
                          "user_mas_tmp_form": user_mas_tmp_form
                      })


@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_del(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                user_mas_tmp = User_mas_tmp.objects.get(id=id)
                user_mas_tmp.delete()

                if func == "user_mas_tmp_lst":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/user_mas_tmp_lst/", rtn_code)
                    return HttpResponseRedirect('/kernal/user_mas_tmp_lst/')
        except Exception as e:
            rtn_code = "0s0901"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_lst(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("get method start")

    #user_mas_tmp_lst = User_mas_tmp.objects.filter(status__in=['D', 'A', 'C'])
    user_mas_tmp_lst = User_mas_tmp.objects.all()

    for user_mas_tmp in user_mas_tmp_lst:
        print(user_mas_tmp.name)

    paginator = Paginator(user_mas_tmp_lst, 14)
    page = request.GET.get('page')
    try:

        current_page = paginator.page(page)
        user_mas_tmp_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        user_mas_tmp_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        user_mas_tmp_lst = current_page.object_list

    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_mas_tmp_lst.html", {"user_mas_tmp_lst": user_mas_tmp_lst, "page": current_page})


@login_required(login_url='/account/login/')
def user_mas_tmp_dsp(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    user_mas_tmp_form = get_object_or_404(User_mas_tmp, id=id)
    logger.info("-------------------------- ended --------------------------")
    return render(request, "kernal/user_mas_tmp_dsp.html", {"user_mas_tmp_form": user_mas_tmp_form})


@login_required(login_url='/account/login/')
@csrf_exempt
# 从主档中取数据，然后插入临时档
def user_mas_tmp_amd2lvl(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_mas = User_mas.objects.get(id=id)

    if request.method == "POST":
        logger.info("post method")

        user_mas_tmp_form = User_mas_tmp_form(request.POST)
        user_mas_tmp = User_mas_tmp()

        if user_mas_tmp_form.is_valid():
            user_mas_tmp_cd = user_mas_tmp_form.cleaned_data
            try:
                with transaction.atomic():
                    #工号不可修改，需要删除auth_user
                    #user_mas_tmp.employee_id = user_mas_tmp_cd["employee_id"]
                    user_mas_tmp.name = user_mas_tmp_cd["name"]
                    user_mas_tmp.on_board_date = user_mas_tmp_cd["on_board_date"]
                    user_mas_tmp.address = user_mas_tmp_cd["address"]
                    user_mas_tmp.age = user_mas_tmp_cd["age"]
                    user_mas_tmp.phone = user_mas_tmp_cd["phone"]
                    user_mas_tmp.mobile_phone = user_mas_tmp_cd["mobile_phone"]
                    user_mas_tmp.status = user_mas_tmp_cd["status"]

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    user_mas_tmp.ver_no = user_mas.ver_no + 1
                    user_mas_tmp.prod = "s"
                    user_mas_tmp.func = sys._getframe().f_code.co_name
                    user_mas_tmp.maker = request.user.username
                    user_mas_tmp.inp_date = datetime.datetime.now()
                    user_mas_tmp.checker = ""
                    user_mas_tmp.app_date = datetime.datetime.now()

                    user_mas_tmp.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011201"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011202"
            logger.error("post method error code:", rtn_code)
            logger.error(user_mas_tmp_form.errors)

            return render(request, "kernal/user_mas_tmp_amd.html",
                          {"user_mas_tmp_form": user_mas_tmp_form, "errors": user_mas_tmp_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        user_mas_tmp_form = User_mas_tmp_form(initial=
        {
            "id": user_mas.id,
            "employee_id": user_mas.employee_id,
            "name": user_mas.name,
            "on_board_date": user_mas.on_board_date,
            "address": user_mas.address,
            "age": user_mas.age,
            "phone": user_mas.phone,
            "mobile_phone": user_mas.mobile_phone,
            "status": user_mas.status,
            "func": sys._getframe().f_code.co_name,
        })
        logger.info("get method end")
        return render(request, "kernal/user_mas_tmp_amd.html",
                      {
                          "user_mas_tmp_form": user_mas_tmp_form
                      })
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_del2lvl(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")

        id = request.POST['id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                user_mas = User_mas.objects.get(id=id)

                user_mas_tmp_count = User_mas_tmp.objects.filter(employee_id=user_mas.employee_id).count()
                logger.info(user_mas_tmp_count)

                if user_mas_tmp_count > 0:
                    rtn_code = "000001"
                    return HttpResponse(rtn_code)

                user_mas_tmp = User_mas_tmp()

                user_mas_tmp.employee_id = user_mas.employee_id
                user_mas_tmp.name = user_mas.name
                user_mas_tmp.on_board_date = user_mas.on_board_date
                user_mas_tmp.address = user_mas.address
                user_mas_tmp.age = user_mas.age
                user_mas_tmp.phone = user_mas.phone
                user_mas_tmp.mobile_phone = user_mas.mobile_phone
                user_mas_tmp.status = user_mas.status

                user_mas_tmp.status = "D"

                ####################
                # 系统管理字段，自动赋值  #
                ####################
                user_mas_tmp.ver_no = int(user_mas.ver_no) + 1

                user_mas_tmp.prod = "User_mas"
                user_mas_tmp.func = sys._getframe().f_code.co_name
                user_mas_tmp.maker = request.user.username
                user_mas_tmp.inp_date = datetime.datetime.now()
                user_mas_tmp.checker = ""
                user_mas_tmp.app_date = datetime.datetime.now()

                user_mas_tmp.save()

                if func == "user_mas_lst2lvl" or func == "user_mas_dsp":
                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponse(rtn_code)
                else:
                    rtn_code = "000000"
                    logger.info("post method:%s /kernal/user_mas_lst/", rtn_code)
                    logger.info("-------------------------- ended --------------------------")
                    return HttpResponseRedirect('/kernal/user_mas_lst/')
        except Exception as e:
            rtn_code = "011301"
            logger.error("post method error code:", rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def user_mas_tmp_app(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    user_mas_tmp = User_mas_tmp.objects.get(id=id)
    user_mas_cnt = User_mas.objects.filter(employee_id=user_mas_tmp.employee_id).count()

    logger.info("User_mas_cnt:%d", user_mas_cnt)

    if user_mas_cnt >= 1:
        user_mas = User_mas.objects.get(employee_id=user_mas_tmp.employee_id)
    else:
        user_mas = User_mas()

    logger.info("User_mas_cnt:%d", user_mas_cnt)
    user_log = User_log()

    if request.method == "POST":
        logger.info("post method")

        user_mas_form = User_mas_form(request.POST)

        if user_mas_form.is_valid():

            # if (User_mas_tmp.maker == request.user.username):
            #     logger.info("================136")  ################
            #     print(request.user.username)
            #     print(User_mas_tmp.maker)
            #     return render(request, "kernal/user_mas_tmp_app.html",
            #                   {"User_mas_tmp_Form": User_mas_tmp_Form,
            #                    "errors": User_mas_tmp_Form.errors})
            #     # print("=======================1")

            # User_mas_tmp_cd = user_mas_tmp_form.cleaned_data

            try:
                with transaction.atomic():
                    # 防中间人篡改，复核人员不得修改数据

                    user_cnt = User.objects.filter(username=user_mas_tmp.employee_id).count()
                    if user_cnt >= 1:  # 如果已存在则获取记录，但没必要修改
                        user = User.objects.get(username=user_mas_tmp.employee_id)
                    else: # 如果是新建，则直接创建
                        user = User()
                        user.username = user_mas_tmp.employee_id
                        user.password = "pbkdf2_sha256$30000$RYFoFp1MJmYn$fqYF7REfhNaJzHwpCvyu0i7yD3pGqbtueqUBqrAjrfM="
                        user.save()

                    user_mas.user = user
                    user_mas.employee_id = user_mas_tmp.employee_id
                    user_mas.name = user_mas_tmp.name
                    user_mas.on_board_date = user_mas_tmp.on_board_date
                    user_mas.address = user_mas_tmp.address
                    user_mas.age = user_mas_tmp.age
                    user_mas.phone = user_mas_tmp.phone
                    user_mas.mobile_phone = user_mas_tmp.mobile_phone
                    user_mas.status = user_mas_tmp.status
                    #此处需要根据status修改 user 对象的状态
                    if user_mas.status == "A":
                        user.is_active = 1  # Active the user
                    else:
                        user.is_active = 0  # Disable the customer
                    user.save()

                    #########################
                    # 系统管理字段，自动赋值  #
                    #########################
                    user_mas.ver_no = user_mas_tmp.ver_no
                    user_mas.prod = "User_mas"
                    user_mas.func = sys._getframe().f_code.co_name
                    user_mas.maker = user_mas_tmp.maker
                    user_mas.inp_date = user_mas_tmp.inp_date
                    user_mas.checker = request.user.username
                    user_mas.app_date = datetime.datetime.now()

                    user_mas.save()

                    ############################
                    # 系统日志管理字段，自动赋值  #
                    ############################
                    user_log.user = user
                    user_log.employee_id = user_mas_tmp.employee_id
                    user_log.name = user_mas_tmp.name
                    user_log.on_board_date = user_mas_tmp.on_board_date
                    user_log.address = user_mas_tmp.address
                    user_log.age = user_mas_tmp.age
                    user_log.phone = user_mas_tmp.phone
                    user_log.mobile_phone = user_mas_tmp.mobile_phone
                    user_log.status = user_mas_tmp.status
                    user_log.ver_no = user_mas.ver_no
                    user_log.prod = user_mas.prod
                    user_log.func = user_mas.func
                    user_log.maker = user_mas.maker
                    user_log.inp_date = user_mas.inp_date
                    user_log.checker = user_mas.checker
                    user_log.app_date = user_mas.app_date

                    # user.save()
                    # user_mas.save()
                    user_log.save()
                    user_mas_tmp.delete()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/kernal/user_mas_tmp_lst/')
            except Exception as e:
                rtn_code = "011401"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "011402"
            logger.error("post method error code:", rtn_code)
            logger.error(user_mas_form.errors)

            return render(request, "kernal/user_mas_tmp_app.html",
                          {"user_mas_form": user_mas_form, "errors": user_mas_form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")

        # 1. 初始化 User_mas_form
        user_mas_form = User_mas_form(initial={
            "employee_id": user_mas_tmp.employee_id,
            "name": user_mas_tmp.name,
            "on_board_date": user_mas_tmp.on_board_date,
            "address": user_mas_tmp.address,
            "age": user_mas_tmp.age,
            "phone": user_mas_tmp.phone,
            "mobile_phone": user_mas_tmp.mobile_phone,
            "status": user_mas_tmp.status,
            "func": sys._getframe().f_code.co_name
        })

        logger.info("get method end")
        return render(request, "kernal/user_mas_tmp_app.html",
                      {
                          "user_mas_form": user_mas_form
                      })

    logger.info("-------------------------- ended --------------------------")

# 404错误
def page_not_found(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("-------------------------- ended --------------------------")
    return render(request, '404.html', {})


# 500错误
def page_error(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        return

    logger.info("-------------------------- ended --------------------------")
    return render(request, '500.html', {})
