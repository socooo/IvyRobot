# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import math
#from django.template import loader
#from pyecharts import Line3D
#from pyecharts import Bar, Geo
# from pyecharts.constants import DEFAULT_HOST

# Create your views here.
# @login_required(login_url='/account/login/')
# def article_column(request):
#     columns = ArticleColumn.objects.filter(user=request.user)
#     return render(request, "article/column/article_column.html", {"columns":columns})


@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns_list = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        
        paginator = Paginator(columns_list, 14)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)    
            columns = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            columns = current_page
        except EmptyPage:
            current_page = paginator.page(page)
            columns = current_page.object_list
        return render(request, "article/column/article_column.html", {"columns":columns, "column_form":column_form,"page":current_page})
    
    if request.method == "POST":
        column_name = request.POST['column_name']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')

# @login_required(login_url='/account/login/')
# def article_column(request, id):
#      column = get_object_or_404(ArticleColumn, id=id)
#      return render(request, "article/column/article_list.html", {"column":column})
 
@login_required(login_url='/account/login/')
# @require_POST
@csrf_exempt
def rename_article_column(request):

    if request.method == "POST":
        column_name = request.POST['column_name']
        column_id = request.POST['column_id']
        
        try:
            line = ArticleColumn.objects.get(id=column_id) 
            line.column = column_name
            line.save()
    
            return HttpResponse('1')
        except:
            return HttpResponse('0')


@login_required(login_url='/account/login/')
# @require_POST
@csrf_exempt
def del_article_column(request):

    if request.method == "POST":
        column_id = request.POST['column_id']
        
        try:
            line = ArticleColumn.objects.get(id=column_id) 
            line.delete()
    
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            
            print ("1")
            
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except Exception as e:
                
#                 print 'str(Exception):\t', str(Exception)
#                 print 'str(e):\t\t', str(e)
#                 print 'repr(e):\t', repr(e)
#                 print 'e.message:\t', e.message
#                 print 'traceback.print_exc():'; traceback.print_exc()
#                 print 'traceback.format_exc():\n%s' % traceback.format_exc()
    
                return HttpResponse("2")
        else:
            
            print ("4")
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", {"article_post_form":article_post_form, "article_columns":article_columns})

@login_required(login_url='/account/login/')
@csrf_exempt
def article_translate(request):

    if request.method == "POST":
        print("")
    else:
        content = request.GET.get('content')
        print(content)

        content="今天饭吃了没？"

        host = "itrans.xfyun.cn"
        # 初始化类
        gClass = get_result(host)
        dest = gClass.call_url(content)

        print("----", dest)

        article_translate_form = ArticlePostForm()
        article_translate_form.title = "title"
        article_translate_form.body = "cifmas_add"
        article_columns = request.user.article_column.all()
        return render(request,
                      "article/column/article_translate.html",
                      {"article_translate_form": article_translate_form,
                       "article_columns": article_columns,
                       "translate:": dest}
                      )



@login_required(login_url='/account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)    
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles":articles, "page":current_page})


@login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article":article})

@login_required(login_url='/account/login/')
def column_detail(request, id):    
    articles_list = ArticlePost.objects.filter(column=id)
    paginator = Paginator(articles_list, 14)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)    
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page
    except EmptyPage:
        current_page = paginator.page(page)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles":articles, "page":current_page})

@login_required(login_url='/account/login/')
# @require_POST
@csrf_exempt
def article_pyechart1(request):
#     from pyecharts.constants import DEFAULT_HOST
    a="Mon"
    names=[a, a, a, a, a, a, a]
    values=[11,121,31,14,15,61,17]
    return render(request, "article/column/article_pyechart1.html",{"names":names, "values":values})
        
# 404错误
def page_not_found(request):
    print ("----")
    return render(request,'article/404.html',{})
# 500错误
def page_error(request):
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