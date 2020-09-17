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
import traceback,datetime,logging,sys
################################################
# 导入SPARK和人工智能
################################################ 
import sys, os
from pyspark import SparkContext, SparkConf
from operator import add
import  re
################################################
# 导入Myibs内部数据模型
################################################ 
from .forms import Cif_mas_Form, Cif_mas_tmp_Form
from .models import Cif_mas, Cif_mas_tmp, Cif_log

logger = logging.getLogger('sourceDns.webdns.views')
rtn_code="999999"

###############################
# 一级交易
###############################
# Create your views here.
@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_add(request):
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    rtn_code="999999"

    if request.method == "POST":
        logger.info("post method")
        cif_mas_Form = Cif_mas_Form(request.POST)


        if cif_mas_Form.is_valid():
#             print("---",cif_mas_Form.clean)

            cif_mas_Form_cd = cif_mas_Form.cleaned_data
            cif_log = Cif_log()

            try:
                with transaction.atomic():

#                     print("id_type:", cif_mas_Form_cd["id_type"])
#                     print("id_country:", cif_mas_Form_cd["id_country"])
#                     print("id_no:", cif_mas_Form_cd["id_no"])
#                     print("address:", cif_mas_Form_cd["address"])

                    cif_mas = cif_mas_Form.save(commit=False)
                    cif_mas.status=cif_mas_Form_cd["status"]
                    
                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas.ver_no=1
                    cif_mas.prod = "Cif_mas"
                    cif_mas.func = sys._getframe().f_code.co_name
                    cif_mas.maker = request.user.username
                    cif_mas.inp_date = datetime.datetime.now()
                    cif_mas.checker = ""
                    cif_mas.app_date = datetime.datetime.now()  
                    
                    ####################
                    # 系统日志管理字段，自动赋值  #
                    ####################
                    cif_log.id_type = cif_mas.id_type
                    cif_log.id_country = cif_mas.id_country
                    cif_log.id_no = cif_mas.id_no
                    cif_log.customer_id = cif_mas.customer_id
                    cif_log.first_name = cif_mas.first_name
                    cif_log.last_name = cif_mas.last_name
                    cif_log.address = cif_mas.address
                    cif_log.age = cif_mas.age
                    cif_log.balance = cif_mas.balance
                    cif_log.birthday = cif_mas.birthday
                    cif_log.email = cif_mas.email
                    cif_log.handphone = cif_mas.handphone
                    cif_log.status=cif_mas.status
                    cif_log.ver_no=cif_mas.ver_no
                    cif_log.prod =cif_mas.prod
                    cif_log.func =cif_mas.func
                    cif_log.maker =cif_mas.maker
                    cif_log.inp_date =cif_mas.inp_date
                    cif_log.checker = cif_mas.checker
                    cif_log.app_date =cif_mas.app_date
                                  
                    cif_mas.save()
                    cif_log.save()
#                   cif_mas_Form.save()
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    return HttpResponseRedirect('/cif/cifmas_lst/')
            except Exception as e:
                rtn_code="010101"
                logger.error("post method:%s",rtn_code)
                logger.error(e)
#                 print("---------------Exception captured here------------------")
#                 traceback.print_exc()
#                 print("---------------Exception captured here------------------")
                return HttpResponse(rtn_code)
        else:
            rtn_code="010101"
            logger.error("post method:%s",rtn_code)
            logger.error(cif_mas_Form.errors)

            return render(request, "cif/cifmas_add.html", {"cif_mas_Form": cif_mas_Form, "errors":cif_mas_Form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")
        cif_mas_Form = Cif_mas_Form()
        cif_mas_Form.func="cifmas_add"
        logger.info("get method end")
        return render(request, "cif/cifmas_add.html",
                      {
                          "cif_mas_Form":cif_mas_Form
                      }
                      )
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_amd(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)

    cif_mas = Cif_mas.objects.get(customer_id=id)
            
    if request.method == "POST":
        logger.info("post method")
        
        cif_mas_Form = Cif_mas_Form(request.POST)

        if cif_mas_Form.is_valid():
            cif_mas_cd = cif_mas_Form.cleaned_data
            
            try:
                with transaction.atomic():
                    cif_mas.id_type = cif_mas_cd["id_type"]
                    cif_mas.id_country = cif_mas_cd["id_country"]
                    cif_mas.id_no = cif_mas_cd["id_no"]
                    cif_mas.customer_id = cif_mas_cd["customer_id"]
                    cif_mas.first_name = cif_mas_cd["first_name"]
                    cif_mas.last_name = cif_mas_cd["last_name"]
                    cif_mas.address = cif_mas_cd["address"]
                    cif_mas.age = cif_mas_cd["age"]
                    cif_mas.balance = cif_mas_cd["balance"]
                    cif_mas.birthday = cif_mas_cd["birthday"]
                    cif_mas.email = cif_mas_cd["email"]
                    cif_mas.handphone = cif_mas_cd["handphone"]
                    cif_mas.status = cif_mas_cd["status"]
#                     cif_mas.inp_date = cif_mas_cd["inp_date"]
#                     cif_mas.app_date = cif_mas_cd["app_date"]
             
                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas.ver_no=cif_mas.ver_no+1
                    cif_mas.prod = "Cif_mas"
                    cif_mas.func = sys._getframe().f_code.co_name
                    cif_mas.maker = request.user.username
                    cif_mas.inp_date = datetime.datetime.now()
                    cif_mas.checker = ""
                    cif_mas.app_date = datetime.datetime.now()     
                               
                    cif_mas.save()

                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    
                    return HttpResponseRedirect('/cif/cifmas_lst/')
            except Exception as e:
                rtn_code="010201"
                logger.error("post method error code:",rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code="010202"
            logger.error("post method error code:",rtn_code)
            logger.error(cif_mas_Form.errors)
             
            return render(request, "cif/cifmas_amd.html", {"cif_mas_Form": cif_mas_Form, "errors":cif_mas_Form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        cif_mas_Form = Cif_mas_Form(initial=
            {
                "id_type":cif_mas.id_type,
                "id_country":cif_mas.id_country,
                "id_no":cif_mas.id_no,
                "customer_id":cif_mas.customer_id,
                "first_name":cif_mas.first_name,
                "last_name":cif_mas.last_name,
                "address":cif_mas.address,
                "age":cif_mas.age,
                "balance":cif_mas.balance,
                "birthday":cif_mas.birthday,
                "email":cif_mas.email,
                "handphone":cif_mas.handphone,
                #"handphone": "3333334444",
                "status":cif_mas.status,
                "func":sys._getframe().f_code.co_name,
                "inp_date":cif_mas.inp_date,
                "app_date":cif_mas.app_date
            })
        logger.info("get method end")
        return render(request, "cif/cifmas_amd.html",
            {
                "cif_mas_Form":cif_mas_Form
            })
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_amd_translate(request, id):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    cif_mas = Cif_mas.objects.get(customer_id=id)

    if request.method == "POST":
        logger.info("post method")

        cif_mas_Form = Cif_mas_Form(request.POST)

        if cif_mas_Form.is_valid():
            cif_mas_cd = cif_mas_Form.cleaned_data

            try:
                with transaction.atomic():
                    cif_mas.id_type = cif_mas_cd["id_type"]
                    cif_mas.id_country = cif_mas_cd["id_country"]
                    cif_mas.id_no = cif_mas_cd["id_no"]
                    cif_mas.customer_id = cif_mas_cd["customer_id"]
                    cif_mas.first_name = cif_mas_cd["first_name"]
                    cif_mas.last_name = cif_mas_cd["last_name"]
                    cif_mas.address = cif_mas_cd["address"]
                    cif_mas.age = cif_mas_cd["age"]
                    cif_mas.balance = cif_mas_cd["balance"]
                    cif_mas.birthday = cif_mas_cd["birthday"]
                    cif_mas.email = cif_mas_cd["email"]
                    cif_mas.handphone = cif_mas_cd["handphone"]
                    cif_mas.status = cif_mas_cd["status"]
                    #                     cif_mas.inp_date = cif_mas_cd["inp_date"]
                    #                     cif_mas.app_date = cif_mas_cd["app_date"]

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas.ver_no = cif_mas.ver_no + 1
                    cif_mas.prod = "Cif_mas"
                    cif_mas.func = sys._getframe().f_code.co_name
                    cif_mas.maker = request.user.username
                    cif_mas.inp_date = datetime.datetime.now()
                    cif_mas.checker = ""
                    cif_mas.app_date = datetime.datetime.now()

                    cif_mas.save()

                    rtn_code = "000000"
                    logger.info("post method:%s", rtn_code)

                    return HttpResponseRedirect('/cif/cifmas_lst/')
            except Exception as e:
                rtn_code = "010201"
                logger.error("post method error code:", rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code = "010202"
            logger.error("post method error code:", rtn_code)
            logger.error(cif_mas_Form.errors)

            return render(request, "cif/cifmas_amd.html", {"cif_mas_Form": cif_mas_Form, "errors": cif_mas_Form.errors})
    else:

        content = request.GET.get('content')
        print(content)

        # content = "今天饭吃了没？" #5LuK5aSp6aWt5ZCD5LqG5rKh77yf
        # bytes_content = content.encode("utf-8")
        # base64_content = base64.b64encode(bytes_content)
        # print(base64_content)
        #
        content = base64.b64decode(content).decode("utf-8")
        print(content)

        host = "itrans.xfyun.cn"
        # 初始化类
        gClass = get_result(host)
        dest = gClass.call_url(content)

        print("----", dest)

        # 返回指定对象
        logger.info("get method start")
        cif_mas_Form = Cif_mas_Form(initial=
        {
            "id_type": cif_mas.id_type,
            "id_country": cif_mas.id_country,
            "id_no": cif_mas.id_no,
            "customer_id": cif_mas.customer_id,
            "first_name": cif_mas.first_name,
            "last_name": cif_mas.last_name,
            "address": cif_mas.address,
            "age": cif_mas.age,
            "balance": cif_mas.balance,
            "birthday": cif_mas.birthday,
            "email": cif_mas.email,
            #"handphone": cif_mas.handphone,
            "handphone": dest,
            "status": cif_mas.status,
            "func": sys._getframe().f_code.co_name,
            "inp_date": cif_mas.inp_date,
            "app_date": cif_mas.app_date
        })
        logger.info("get method end")
        return render(request, "cif/cifmas_amd.html",
                      {
                          "cif_mas_Form": cif_mas_Form
                      })
    logger.info("-------------------------- ended --------------------------")
        
@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_del(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)

    if request.method == "POST":
        logger.info("post method")
        
        customer_id = request.POST['customer_id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                cif_mas = Cif_mas.objects.get(customer_id=customer_id) 
                
                cif_mas.status = "D"
                
                ####################
                # 系统管理字段，自动赋值  #
                ####################
                cif_mas.ver_no=cif_mas.ver_no+1
                cif_mas.prod = "Cif_mas"
                cif_mas.func = sys._getframe().f_code.co_name
                cif_mas.maker = request.user.username
                cif_mas.inp_date = datetime.datetime.now()
                cif_mas.checker = ""
                cif_mas.app_date = datetime.datetime.now()     
                           
                cif_mas.save()
                    
#                 cif_mas.delete()
                
                if (func == "cifmas_list"):
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    return HttpResponse("000000")
                else:
#                     print('/cif/cifmas_lst/')
                    rtn_code="000000"
                    logger.info("post method:%s /cif/cifmas_lst/",rtn_code)
                    return HttpResponseRedirect('/cif/cifmas_lst/')
        except Exception as e:
            rtn_code="010301"
            logger.error("post method error code:",rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")    
        
@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_lst(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        return
    
    logger.info("get method start")
    cifmas_lst = Cif_mas.objects.all()
    #cifmas_lst = Cif_mas.objects.filter(status="A")
    paginator = Paginator(cifmas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)    
        cifmas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        cifmas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        cifmas_lst = current_page.object_list
    
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_lst.html", {"cifmas_lst":cifmas_lst, "page":current_page})


@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_lst2lvl(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")   
    cifmas_lst = Cif_mas.objects.filter(status="A")
    paginator = Paginator(cifmas_lst, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)    
        cifmas_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        cifmas_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        cifmas_lst = current_page.object_list
        
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_lst2lvl.html", {"cifmas_lst":cifmas_lst, "page":current_page})


@login_required(login_url='/account/login/')
def cifmas_dsp(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        pass
    
    logger.info("get method start")
    cif_mas_Form = get_object_or_404(Cif_mas, id=id)
    logger.info("get method end")
    
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_dsp.html", {"cif_mas_Form":cif_mas_Form})



###############################
# 二级交易
###############################
@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_add(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)

    if request.method == "POST":
        logger.info("post method")
        cif_mas_tmp_Form = Cif_mas_tmp_Form(request.POST)

        if cif_mas_tmp_Form.is_valid():
#             print("---",cif_mas_Form.clean)
            cif_mas_tmp_Form_cd = cif_mas_tmp_Form.cleaned_data
            try:
                with transaction.atomic():
#                     print("id_type:", cif_mas_Form_cd["id_type"])
#                     print("id_country:", cif_mas_Form_cd["id_country"])
#                     print("id_no:", cif_mas_Form_cd["id_no"])
#                     print("address:", cif_mas_Form_cd["address"])
                    cif_mas_tmp = cif_mas_tmp_Form.save(commit=False)
                    cif_mas_tmp.status = "A"
                    
                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas_tmp.ver_no=1
                    cif_mas_tmp.prod = "Cif_mas"
                    cif_mas_tmp.func = sys._getframe().f_code.co_name
                    cif_mas_tmp.maker = request.user.username
                    cif_mas_tmp.inp_date = datetime.datetime.now()
                    cif_mas_tmp.checker = ""
                    cif_mas_tmp.app_date = datetime.datetime.now()     
                    
                    cif_mas_tmp.save()

                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    
                    return HttpResponseRedirect('/cif/cifmas_tmp_lst/')
            except Exception as e:
                rtn_code="010701"
                logger.error("post method error code:",rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code="010702"
            logger.error("post method error code:",rtn_code)
            logger.error(cif_mas_tmp_Form.errors)

            return render(request, "cif/cifmas_tmp_add.html", {"cif_mas_tmp_Form": cif_mas_tmp_Form, "errors":cif_mas_tmp_Form.errors})
    else:
        # 返回空对象即可
        logger.info("get method start")
        cif_mas_tmp_Form = Cif_mas_tmp_Form()
        cif_mas_tmp_Form.func = "cifmas_tmp_add"

        logger.info("get method end")
        
        logger.info("-------------------------- ended --------------------------")   
        return render(request, "cif/cifmas_tmp_add.html",
                      {
                          "cif_mas_tmp_Form":cif_mas_tmp_Form
                      }
                      )
        
@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_amd(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)

    cif_mas_tmp = Cif_mas_tmp.objects.get(customer_id=id)

    if request.method == "POST":
        logger.info("post method")
        
        cif_mas_tmp_Form = Cif_mas_tmp_Form(request.POST)

        if cif_mas_tmp_Form.is_valid():
            cif_mas_tmp_cd = cif_mas_tmp_Form.cleaned_data
            
            try:
                with transaction.atomic():
                    cif_mas_tmp.id_type = cif_mas_tmp_cd["id_type"]
                    cif_mas_tmp.id_country = cif_mas_tmp_cd["id_country"]
                    cif_mas_tmp.id_no = cif_mas_tmp_cd["id_no"]
                    cif_mas_tmp.customer_id = cif_mas_tmp_cd["customer_id"]
                    cif_mas_tmp.first_name = cif_mas_tmp_cd["first_name"]
                    cif_mas_tmp.last_name = cif_mas_tmp_cd["last_name"]
                    cif_mas_tmp.address = cif_mas_tmp_cd["address"]
                    cif_mas_tmp.age = cif_mas_tmp_cd["age"]
                    cif_mas_tmp.balance = cif_mas_tmp_cd["balance"]
                    cif_mas_tmp.birthday = cif_mas_tmp_cd["birthday"]
                    cif_mas_tmp.email = cif_mas_tmp_cd["email"]
                    cif_mas_tmp.handphone = cif_mas_tmp_cd["handphone"]
                    cif_mas_tmp.status = cif_mas_tmp_cd["status"]

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas_tmp.ver_no=cif_mas_tmp.ver_no+1
                    cif_mas_tmp.prod = "Cif_mas"
                    cif_mas_tmp.func = sys._getframe().f_code.co_name
                    cif_mas_tmp.maker = request.user.username
                    cif_mas_tmp.inp_date = datetime.datetime.now()
                    cif_mas_tmp.checker = ""
                    cif_mas_tmp.app_date = datetime.datetime.now()    
                    cif_mas_tmp.save()
                    
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    
                    return HttpResponseRedirect('/cif/cifmas_tmp_lst/')
            except Exception as e:
                rtn_code="010801"
                logger.error("post method error code:",rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code="010802"
            logger.error("post method error code:",rtn_code)
            logger.error(cif_mas_tmp_Form.errors)
             
            return render(request, "cif/cifmas_tmp_amd.html", {"cif_mas_tmp_Form": cif_mas_tmp_Form, "errors":cif_mas_tmp_Form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        cif_mas_tmp_Form = Cif_mas_tmp_Form(initial=
            {
                "id_type":cif_mas_tmp.id_type,
                "id_country":cif_mas_tmp.id_country,
                "id_no":cif_mas_tmp.id_no,
                "customer_id":cif_mas_tmp.customer_id,
                "first_name":cif_mas_tmp.first_name,
                "last_name":cif_mas_tmp.last_name,
                "address":cif_mas_tmp.address,
                "age":cif_mas_tmp.age,
                "balance":cif_mas_tmp.balance,
                "birthday":cif_mas_tmp.birthday,
                "email":cif_mas_tmp.email,
                "handphone":cif_mas_tmp.handphone,
                "func":sys._getframe().f_code.co_name,
                "status":cif_mas_tmp.status,
                "inp_date":cif_mas_tmp.inp_date,
                "app_date":cif_mas_tmp.app_date
            })
        logger.info("get method end")
        logger.info("-------------------------- ended --------------------------")
        return render(request, "cif/cifmas_tmp_amd.html",
            {
                "cif_mas_tmp_Form":cif_mas_tmp_Form
            })

@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_del(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)

    if request.method == "POST":
        logger.info("post method")
        
        customer_id = request.POST['customer_id']
        func = request.POST['func']
        
        try:
            with transaction.atomic():
                cif_mas_tmp = Cif_mas_tmp.objects.get(customer_id=customer_id) 
                cif_mas_tmp.delete()
                
                if (func == "cifmas_list"):
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    return HttpResponse(rtn_code)
                else:
                    rtn_code="000000"
                    logger.info("post method:%s /cif/cifmas_tmp_lst/",rtn_code)
                    return HttpResponseRedirect('/cif/cifmas_tmp_lst/')
        except Exception as e:
            rtn_code="010901"
            logger.error("post method error code:",rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")

@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_lst(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        return
    
#     cifmas_tmp_lst = Cif_mas_tmp.objects.filter(status="A")
    logger.info("get method start")
    
    cifmas_tmp_lst = Cif_mas_tmp.objects.filter(status__in=['D', 'A'])

    paginator = Paginator(cifmas_tmp_lst, 14)
    page = request.GET.get('page')
    try:

        current_page = paginator.page(page)    
        cifmas_tmp_lst = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        cifmas_tmp_lst = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        cifmas_tmp_lst = current_page.object_list
    
    logger.info("get method end")    
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_tmp_lst.html", {"cifmas_tmp_lst":cifmas_tmp_lst, "page":current_page})


@login_required(login_url='/account/login/')
def cifmas_tmp_dsp(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        return
    
    cif_mas_tmp_Form = get_object_or_404(Cif_mas_tmp, id=id)
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_tmp_dsp.html", {"cif_mas_tmp_Form":cif_mas_tmp_Form})


@login_required(login_url='/account/login/')
@csrf_exempt
#从主档中取数据，然后插入临时档
def cifmas_tmp_amd2lvl(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    cif_mas = Cif_mas.objects.get(customer_id=id)
    cif_mas_tmp = Cif_mas_tmp()
    
    if request.method == "POST":
        logger.info("post method")
        
        cif_mas_tmp_Form = Cif_mas_tmp_Form(request.POST)
        cif_mas_tmp = Cif_mas.objects.get(customer_id=id)

        if cif_mas_tmp_Form.is_valid():
            cif_mas_tmp_cd = cif_mas_tmp_Form.cleaned_data
            
            try:
                with transaction.atomic():
#                     cif_mas_tmp.id_type         =cif_mas_tmp_cd["id_type"]
#                     cif_mas_tmp.id_country    =cif_mas_tmp_cd["id_country"]
#                     cif_mas_tmp.id_no            =cif_mas_tmp_cd["id_no"]
#                     cif_mas_tmp.customer_id=cif_mas_tmp_cd["customer_id"]
#                     cif_mas_tmp.first_name   =cif_mas_tmp_cd["first_name"]
#                     cif_mas_tmp.last_name   =cif_mas_tmp_cd["last_name"]
#                     cif_mas_tmp.address       =cif_mas_tmp_cd["address"]
#                     cif_mas_tmp.age             =cif_mas_tmp_cd["age"]
#                     cif_mas_tmp.balance       =cif_mas_tmp_cd["balance"]
#                     cif_mas_tmp.birthday       =cif_mas_tmp_cd["birthday"]
#                     cif_mas_tmp.email           =cif_mas_tmp_cd["email"]
#                     cif_mas_tmp.handphone =cif_mas_tmp_cd["handphone"]
#                     cif_mas_tmp.inp_date       =cif_mas_tmp_cd["inp_date"]
#                     cif_mas_tmp.app_date      =cif_mas_tmp_cd["app_date"]
#                     
#                     cif_mas_tmp.save()

                    cif_mas_tmp = cif_mas_tmp_Form.save(commit=False)
#                     cif_mas_tmp.status = "A"
                    
                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas_tmp.ver_no=cif_mas_tmp.ver_no+1
                    cif_mas_tmp.prod = "Cif_mas"
                    cif_mas_tmp.func = sys._getframe().f_code.co_name
                    cif_mas_tmp.maker = request.user.username
                    cif_mas_tmp.inp_date = datetime.datetime.now()
                    cif_mas_tmp.checker = ""
                    cif_mas_tmp.app_date = datetime.datetime.now()
                    
                    cif_mas_tmp.save()

                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    
                    return HttpResponseRedirect('/cif/cifmas_tmp_lst/')
            except Exception as e:
                rtn_code="011201"
                logger.error("post method error code:",rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code="011202"
            logger.error("post method error code:",rtn_code)
            logger.error(cif_mas_tmp_Form.errors)
             
            return render(request, "cif/cifmas_tmp_amd.html", {"cif_mas_tmp_Form": cif_mas_tmp_Form, "errors":cif_mas_tmp_Form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        cif_mas_tmp_Form = Cif_mas_Form(initial=
            {
                "id_type":cif_mas.id_type,
                "id_country":cif_mas.id_country,
                "id_no":cif_mas.id_no,
                "customer_id":cif_mas.customer_id,
                "first_name":cif_mas.first_name,
                "last_name":cif_mas.last_name,
                "address":cif_mas.address,
                "age":cif_mas.age,
                "balance":cif_mas.balance,
                "birthday":cif_mas.birthday,
                "email":cif_mas.email,
                "handphone":cif_mas.handphone,
                "status":cif_mas.status,
                "inp_date":cif_mas.inp_date,
                "app_date":cif_mas.app_date
            })
        logger.info("get method end")
        return render(request, "cif/cifmas_tmp_amd.html",
            {
                "cif_mas_tmp_Form":cif_mas_tmp_Form
            })
    logger.info("-------------------------- ended --------------------------")

@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_del2lvl(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        
        customer_id = request.POST['customer_id']
        func = request.POST['func']

        try:
            with transaction.atomic():
                cif_mas = Cif_mas.objects.get(customer_id=customer_id) 
                cif_mas_tmp = Cif_mas_tmp()

                cif_mas_tmp.id_type = cif_mas.id_type         
                cif_mas_tmp.id_country = cif_mas.id_country    
                cif_mas_tmp.id_no = cif_mas.id_no            
                cif_mas_tmp.customer_id = cif_mas.customer_id
                cif_mas_tmp.first_name = cif_mas.first_name 
                cif_mas_tmp.last_name = cif_mas.last_name 
                cif_mas_tmp.address = cif_mas.address     
                cif_mas_tmp.age = cif_mas.age            
                cif_mas_tmp.balance = cif_mas.balance     
                cif_mas_tmp.birthday = cif_mas.birthday     
                cif_mas_tmp.email = cif_mas.email          
                cif_mas_tmp.handphone = cif_mas.handphone
                cif_mas_tmp.inp_date = cif_mas.inp_date      
                cif_mas_tmp.app_date = cif_mas.app_date     
                cif_mas_tmp.status = "D"

                ####################
                # 系统管理字段，自动赋值  #
                ####################
                cif_mas_tmp.ver_no=cif_mas_tmp.ver_no+1
                cif_mas_tmp.prod = "Cif_mas"
                cif_mas_tmp.func = sys._getframe().f_code.co_name
                cif_mas_tmp.maker = request.user.username
                cif_mas_tmp.inp_date = datetime.datetime.now()
                cif_mas_tmp.checker = ""
                cif_mas_tmp.app_date = datetime.datetime.now()
                    
                cif_mas_tmp.save()

                if (func == "cifmas_list"):
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    return HttpResponse("000000")
                else:
                    rtn_code="000000"
                    logger.info("post method:%s /cif/cifmas_lst/",rtn_code)
                    return HttpResponseRedirect('/cif/cifmas_lst/')
        except Exception as e:
            rtn_code="011301"
            logger.error("post method error code:",rtn_code)
            logger.error(e)
            return HttpResponse(rtn_code)
    logger.info("-------------------------- ended --------------------------")
        

@login_required(login_url='/account/login/')
@csrf_exempt
def cifmas_tmp_app(request, id):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    cif_mas_tmp = Cif_mas_tmp.objects.get(customer_id=id)
    cif_mas_cnt = Cif_mas.objects.filter(customer_id=id).count()

    logger.info("cif_mas_cnt:%d",cif_mas_cnt)
    if (cif_mas_cnt >= 1):
        cif_mas = Cif_mas.objects.get(customer_id=id)
    else:
        cif_mas = Cif_mas()

    logger.info("cif_mas_cnt:%d", cif_mas_cnt)
    cif_log = Cif_log()
    
    if request.method == "POST":
        logger.info("post method")

        logger.info("================111")  ################
        
        cif_mas_tmp_Form = Cif_mas_tmp_Form(request.POST)

        if cif_mas_tmp_Form.is_valid():
            # logger.info("================115")  ################
            # a = 1
            # if (a == 1):
            #     logger.info("================136")  ################
            #     print(request.user.username)
            #     print(cif_mas_tmp.maker)
            #     return render(request, "cif/cifmas_tmp_app.html",
            #                   {"cif_mas_tmp_Form": cif_mas_tmp_Form,
            #                    "errors": cif_mas_tmp_Form.errors})
            #     # print("=======================1")

            cif_mas_tmp_cd = cif_mas_tmp_Form.cleaned_data

            try:
                with transaction.atomic():

#                     cif_mas.id_type = cif_mas_tmp_cd["id_type"]
#                     cif_mas.id_country = cif_mas_tmp_cd["id_country"]
#                     cif_mas.id_no = cif_mas_tmp_cd["id_no"]
#                     cif_mas.customer_id = cif_mas_tmp_cd["customer_id"]
#                     cif_mas.first_name = cif_mas_tmp_cd["first_name"]
#                     cif_mas.last_name = cif_mas_tmp_cd["last_name"]
#                     cif_mas.address = cif_mas_tmp_cd["address"]
#                     cif_mas.age = cif_mas_tmp_cd["age"]
#                     cif_mas.balance = cif_mas_tmp_cd["balance"]
#                     cif_mas.birthday = cif_mas_tmp_cd["birthday"]
#                     cif_mas.email = cif_mas_tmp_cd["email"]
#                     cif_mas.handphone = cif_mas_tmp_cd["handphone"]
#                     cif_mas.status=cif_mas_tmp_cd["status"]
#                     cif_mas.status = cif_mas_tmp.status

                    #防中间人篡改，复核人员不得修改数据
                    cif_mas.id_type = cif_mas_tmp.id_type
                    cif_mas.id_country = cif_mas_tmp.id_country
                    cif_mas.id_no = cif_mas_tmp.id_no
                    cif_mas.customer_id = cif_mas_tmp.customer_id
                    cif_mas.first_name = cif_mas_tmp.first_name
                    cif_mas.last_name = cif_mas_tmp.last_name
                    cif_mas.address = cif_mas_tmp.address
                    cif_mas.age = cif_mas_tmp.age
                    cif_mas.balance = cif_mas_tmp.balance
                    cif_mas.birthday = cif_mas_tmp.birthday
                    cif_mas.email = cif_mas_tmp.email
                    cif_mas.handphone = cif_mas_tmp.handphone
                    cif_mas.status=cif_mas_tmp.status

                    ####################
                    # 系统管理字段，自动赋值  #
                    ####################
                    cif_mas.ver_no=cif_mas.ver_no+1
                    cif_mas.prod = "Cif_mas"
                    cif_mas.func = sys._getframe().f_code.co_name
                    cif_mas.maker = cif_mas_tmp.maker
                    cif_mas.inp_date = cif_mas_tmp.inp_date
                    cif_mas.checker = request.user.username
                    cif_mas.app_date = datetime.datetime.now()
                    ####################
                    # 系统日志管理字段，自动赋值  #
                    ####################
                    cif_log.id_type = cif_mas.id_type
                    cif_log.id_country = cif_mas.id_country
                    cif_log.id_no = cif_mas.id_no
                    cif_log.customer_id = cif_mas.customer_id
                    cif_log.first_name = cif_mas.first_name
                    cif_log.last_name = cif_mas.last_name
                    cif_log.address = cif_mas.address
                    cif_log.age = cif_mas.age
                    cif_log.balance = cif_mas.balance
                    cif_log.birthday = cif_mas.birthday
                    cif_log.email = cif_mas.email
                    cif_log.handphone = cif_mas.handphone
                    cif_log.status=cif_mas.status
                    cif_log.ver_no=cif_mas.ver_no
                    cif_log.prod =cif_mas.prod
                    cif_log.func =cif_mas.func
                    cif_log.maker =cif_mas.maker
                    cif_log.inp_date =cif_mas.inp_date
                    cif_log.checker = cif_mas.checker
                    cif_log.app_date =cif_mas.app_date
                    
                    cif_mas.save()
                    cif_mas_tmp.delete()
                    cif_log.save()
                    
                    rtn_code="000000"
                    logger.info("post method:%s",rtn_code)
                    
                    return HttpResponseRedirect('/cif/cifmas_tmp_lst/')
            except Exception as e:
                rtn_code="011401"
                logger.error("post method error code:",rtn_code)
                logger.error(e)
                return HttpResponse(rtn_code)
        else:
            rtn_code="011402"
            logger.error("post method error code:",rtn_code)
            logger.error(cif_mas_tmp_Form.errors)
              
            return render(request, "cif/cifmas_tmp_app.html", {"cif_mas_tmp_Form": cif_mas_tmp_Form, "errors":cif_mas_tmp_Form.errors})
    else:
        # 返回指定对象
        logger.info("get method start")
        cif_mas_tmp_Form = Cif_mas_tmp_Form(initial=
            {
                "id_type":cif_mas_tmp.id_type,
                "id_country":cif_mas_tmp.id_country,
                "id_no":cif_mas_tmp.id_no,
                "customer_id":cif_mas_tmp.customer_id,
                "first_name":cif_mas_tmp.first_name,
                "last_name":cif_mas_tmp.last_name,
                "address":cif_mas_tmp.address,
                "age":cif_mas_tmp.age,
                "balance":cif_mas_tmp.balance,
                "birthday":cif_mas_tmp.birthday,
                "email":cif_mas_tmp.email,
                "handphone":cif_mas_tmp.handphone,
                "status":cif_mas_tmp.status,
                "func":cif_mas_tmp.func,
                "inp_date":cif_mas_tmp.inp_date,
                "app_date":cif_mas_tmp.app_date
            })
        return render(request, "cif/cifmas_tmp_app.html",
            {
                "cif_mas_tmp_Form":cif_mas_tmp_Form
            })
    logger.info("get method end")
    logger.info("-------------------------- ended --------------------------")


@login_required(login_url='/account/login/')
@csrf_exempt
# 客户余额统计
def cifmas_echart_0001(request):  

    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        pass
    
    logger.info("get method start")
    last_name = list(Cif_mas.objects.values_list('last_name', flat=True))
    age = list(Cif_mas.objects.values_list('age', flat=True))
    logger.info("get method end")
    
    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_echart_0001.html", {"names":last_name, "values":age})   

@login_required(login_url='/account/login/')
@csrf_exempt
# 词频分析
def cifmas_echart_0002(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")

    import os, sys
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    try:
        import configparser
    except:
        from six.moves import configparser

    config = configparser.ConfigParser()
    config.read("mysite\myibs.ini")
    gv_SPARK_HOME = config.get("baseconf", "SPARK_HOME")

    #此处的设置基本无用，具体看 un --> Edit configuration-->点击Enviroment variables后面的三个点 +  然后点击 + ，输入key：SPARK_HOME， value： D:\spark-1.6.0-bin-hadoop2.6
    os.environ['SPARK_HOME'] = gv_SPARK_HOME
    SPARK_HOME = os.environ['SPARK_HOME']
    # HADOOP_HOME = 'D:\workspace_scala\Lib\hadoop-common-2.2.0-bin-master'
    PY4J_DIR = os.path.normpath(SPARK_HOME + '/python/build')
    PYSPARK_DIR = os.path.normpath(SPARK_HOME + '/python')
    sys.path.insert(0, PY4J_DIR)
    sys.path.insert(0, PYSPARK_DIR)


    try:
        sc = SparkContext(appName="wordsCount")

        lines = sc.textFile('D:\\workspace_python\\mysite\\dat\\wordcount.txt')
        counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
        output = counts.collect()
        #         print(output)
        #         for (word, count) in output:
        #             print (word, count)

        loop = 0
        word_list = []
        count_list = []
        for (word) in output:
            word_list.append(word[0])
            count_list.append(word[1])
            loop = loop + 1
    except Exception as e:
        rtn_code = "011501"
        logger.error("post method: %s", rtn_code)
        logger.error(e)
        sc.stop()
        return HttpResponse(rtn_code)
    finally:
        sc.stop()

    logger.info("get method end")

    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_echart_0002.html", {"names": word_list, "values": count_list})

@login_required(login_url='/account/login/')
@csrf_exempt
# 词频分析
def cifmas_echart_0003(request):
    rtn_code = "999999"
    logger.info("-------------------------- started, username=%s --------------------------", request.user.username)

    if request.method == "POST":
        logger.info("post method")
        pass

    logger.info("get method start")

    import os, sys
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    try:
        import configparser
    except:
        from six.moves import configparser

    config = configparser.ConfigParser()
    config.read("mysite\myibs.ini")
    gv_SPARK_HOME = config.get("baseconf", "SPARK_HOME")

    # os.environ['SPARK_HOME']='C:\\spark-1.6.0-bin-hadoop2.6'
    os.environ['SPARK_HOME'] = gv_SPARK_HOME
    SPARK_HOME = os.environ['SPARK_HOME']
    PY4J_DIR = os.path.normpath(SPARK_HOME + '/python/build')
    PYSPARK_DIR = os.path.normpath(SPARK_HOME + '/python')
    sys.path.insert(0, PY4J_DIR)
    sys.path.insert(0, PYSPARK_DIR)

    sc = SparkContext(appName="wordsCount")

    from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel

    def parsePoint(line):
        values = [float(x) for x in line.replace(',', ' ').split(' ')]
        return LabeledPoint(values[0], values[1:])

    try:
        data = sc.textFile("D:\\workspace_python\\mysite\dat\\linear_regression_2.dat")
        print(data.collect()[0])
        parsedData = data.map(parsePoint)

        # Build the model 建立模型
        # model = LinearRegressionWithSGD.train(parsedData, iterations=1000, step=0.1)
        model = LinearRegressionWithSGD.train(parsedData, iterations=5, step=0.1)

        # Evaluate the model on training data 评估模型在训练集上的误差
        valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
        print(valuesAndPreds.collect()[0])

        loop = 0
        list_sample = []
        list_prediction = []
        list_sequence = []
        for iterator in valuesAndPreds.collect():
            # print(iterator[0], iterator[1])
            list_sample.append(iterator[0])
            list_prediction.append(round(iterator[1], 4))
            list_sequence.append(loop)
            loop = loop + 1

        MSE = valuesAndPreds \
                  .map(lambda vp: (vp[0] - vp[1]) ** 2) \
                  .reduce(lambda x, y: x + y) / valuesAndPreds.count()
        print("Mean Squared Error = " + str(MSE))
    except Exception as e:
        rtn_code = "011601"
        logger.error("post method: %s", rtn_code)
        logger.error(e)
        sc.stop()
        return HttpResponse(rtn_code)
    finally:
        sc.stop()

    logger.info("get method end")

    logger.info("-------------------------- ended --------------------------")
    return render(request, "cif/cifmas_echart_0003.html", {"samples": list_sample, "predictions": list_prediction, "sequence": list_sequence})


# 404错误
def page_not_found(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        return
    
    logger.info("-------------------------- ended --------------------------")
    return render(request, 'article/404.html', {})


# 500错误
def page_error(request):
    rtn_code="999999"
    logger.info("-------------------------- started, username=%s --------------------------",request.user.username)
    
    if request.method == "POST":
        logger.info("post method")
        return
    
    logger.info("-------------------------- ended --------------------------")
    return render(request, 'article/500.html', {})


import requests
import datetime
import hashlib
import base64
import hmac
import json

class get_result(object):
    def __init__(self, host):
        # 应用ID（到控制台获取）
        self.APPID = "5f5c4f75"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey = "7a3136e4cac2160adb122031351fe0a4"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "0672724ff7d71dc8fbbdcf98614aedb1"

        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/its"
        # 设置url
        # print(host)
        self.url = "https://" + host + self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置业务参数
        # 语种列表参数值请参照接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html
        # self.Text = "你好吗"
        self.Text = "语种列表参数值请参照接口文档"
        self.BusinessArgs = {
            "from": "cn",
            "to": "en",
        }

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        # print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        # print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        content = str(base64.b64encode(self.Text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        # print(body)
        return body

    def call_url(self, content):
        self.Text = content
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body = self.get_body()
            headers = self.init_header(body)
            print(self.url)
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            print(response.content)
            if status_code != 200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                print(respData)
                respData1=respData.get("data").get("result")
                print(respData1)
                respData1 = respData1.get("trans_result")
                dest=respData1.get("dst")
                print("111" + dest)

                # 以下仅用于调试
                code = str(respData["code"])
                if code != '0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")

                return dest