from django.shortcuts import render
import logging
from django.http.response import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient
import requests
import json
import webbrowser
import time

logger = logging.getLogger('sourceDns.webdns.views')

# Create your views here.
@csrf_exempt
def check_signature(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        token = '100ArcticFox'

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        print('[token, timestamp, nonce]', hashlist)
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        print('hashstr befor sha1', hashstr)
        hashstr = hashlib.sha1(hashstr).hexdigest()
        print('hashstr sha1', hashstr)

        if hashstr ==signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    else:
        # return HttpResponse('chenggong')

        othercontent = autoreply(request)
        return HttpResponse(othercontent)


#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET
def autoreply(request):
    try:
        webData = request.body
        print(webData)
        xmlData = ET.fromstring(webData)

        # root = xmlData.getroot()
        # for child in root:
        #     print(child.tag, child.attrib)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        # CreateTime = xmlData.find('CreateTime').text
        # MsgType = xmlData.find('MsgType').text
        # MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            Content = xmlData.find('Content').text
            if Content == "aa":
                content = "<html><body>1111</body></html>"
                replyMsg = TextMsg(toUser, fromUser, content)
                print ("成功了!!!!!!!!!!!!!!!!!!!")
                print (replyMsg)
                return replyMsg.send()
            elif Content.upper() == "OCR":
                sendOCR()
            else:
                sendmsg('oSLKY00WkGfHfCLaEIHUw8qwip9s', Content)
                content = "未知指令, 请登录 http://snetlogon20.imwork.net/article/article-list/ 查询"
                replyMsg = TextMsg(toUser, fromUser, content)

                print("成功了!!!!!!!!!!!!!!!!!!!")
                print(replyMsg)
                return replyMsg.send()

        elif msg_type == 'image':
            content = "pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp"
            print("-----100 PicMsg")
            replyMsg = PicMsg(toUser, fromUser, content)
            print("-----101 PicMsg")
            return replyMsg.send()
        elif msg_type == 'voice':
            Recognition = xmlData.find('Recognition').text
            print(Recognition)

            if Recognition.find("写工作报告") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-post/")
                actStatus = "请开始处理工作报告: http://snetlogon20.imwork.net/article/article-post/"
            elif Recognition.find("查看工作报告") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-list/")
                actStatus = "请查看工作报告: http://snetlogon20.imwork.net/article/article-list/"
            elif Recognition.find("百度") == 0:
                webbrowser.open("www.baidu.com")
                actStatus = "请点击链接: www.baidu.com"
            elif Recognition.find("看新闻") == 0:
                webbrowser.open("www.sina.com")
                actStatus = "请点击链接: www.qq.com"
            elif Recognition.find("外卖") == 0 or Recognition.find("自助下单") == 0 :
                webbrowser.open("www.meituan.com")
                actStatus = "Ivy robot 提示你自行下单：http://snetlogon20.imwork.net/cif/cifmas_add/"
            elif Recognition.find("美团") == 0:
                webbrowser.open("www.meituan.com")
                actStatus = "IIvy robot 已下单 - 美团"
            elif Recognition.find("饿了吗") == 0:
                webbrowser.open("www.meituan.com")
                actStatus = "Ivy robot 已下单 - 饿了吗"
            else:
                actStatus = "实在不知道你说啥。\n要不看看Ivy robot 使用指南：http://snetlogon20.imwork.net/article/article-detail/14/Ivy-robot-Shi-Yong-Zhi-Nan/"


            content = "你说的是:" + Recognition + "\n" \
                      "处理结果是：" + actStatus
            replyMsg = TextMsg(toUser, fromUser, content)

            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到, 马上来接你 谢谢"

            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'event':
            event = xmlData.find('Event').text
            event_key = xmlData.find('EventKey').text

            print(event, event_key)

            if event == "CLICK":
                if event_key == 'cifmas_lst2lvl':
                    content = "cifmas_lst2lvl"

                    from cif.models import Cif_mas, Cif_mas_tmp, Cif_log
                    cifmas_lst = Cif_mas.objects.filter(status="A")
                    content = ":"
                    for cifmas in cifmas_lst:
                        content = content + cifmas.id_no + "," + cifmas.first_name + "," + cifmas.last_name + "\n"

                    replyMsg = TextMsg(toUser, fromUser, content)
                elif event_key == 'user_mas_lst2lvl':
                    content = "user_mas_lst2lvl"
                    replyMsg = TextMsg(toUser, fromUser, content)
                else:
                    content = "没有这个菜单"
                    replyMsg = TextMsg(toUser, fromUser, content)

            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception as e:
        return e

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)


class PicMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        print("----201 PicMsg init " + content)
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['media_id'] = content

    def send(self):
        print("----301 PicMsg here:" + self.__dict['media_id'])
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
            <MediaId><![CDATA[pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp]]></MediaId>
        </Image>
        </xml>
        """
        #XmlForm.replace("<![CDATA[media_id]]>", "<![CDATA[pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp]]>")

        print("---302" + XmlForm.format(**self.__dict))
        return XmlForm.format(**self.__dict)

#定制菜单
#http://snetlogon20.imwork.net/wechat/create_menu/
def create_menu(request):
	# 第一个参数是公众号里面的appID，第二个参数是appsecret
    #20200912
    #client = WeChatClient("wxf1f84216155f1f4f", "60b3a0ed8186ee298050625f08934a85")

    #测试账号
    #client = WeChatClient("wx3a9cda89ad5d9781", "bde750fa7404467204f1b967cbcba353")
    #client = WeChatClient("wxd8adb366cf6afb91", "4c0faa3a007df74b0664da87ad2887b8") #on book

    #20200913 刘姥姥家的黄石公修改
    client = WeChatClient("wx7a6557af9c8c90a2", "f64a4963151f3d31f3153806ad5fffdc")


    client.menu.create({
         "button": [
            {
                "type": "click",
                "name": "客户信息",
                "key": "cifmas_lst2lvl"
            },
            {
                "type": "click",
                "name": "用户信息",
                "key": "user_mas_lst2lvl"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "登录MYIBS",
                        "url": "https://ebanktest.fubonchina.com/article/article-column/"
                    },
                    {
                        "type": "view",
                        "name": "登录MYIBS",
                        "url": "https://www.baidu.com"
                    },
                    {
                        "type": "view",
                        "name": "点赞",
                        "url": "http://snetlogon20.imwork.net/account/login"
                    }
                ]
            }
        ],
        "matchrule": {
            "group_id": "2",
            "sex": "1",
            "country": "中国",
            "province": "广东",
            "city": "广州",
            "client_platform_type": "2"
        }
    })
    return HttpResponse('ok')

#发送短消息
def get_access_token():
    #commented on 20200913
    # result = requests.get(
    #     url="https://api.weixin.qq.com/cgi-bin/token",
    #     params={
    #         "grant_type": "client_credential",
    #         "appid": "wxf1f84216155f1f4f",
    #         "secret": "60b3a0ed8186ee298050625f08934a85",
    #     }
    # ).json()
    #use this new on
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": "wx7a6557af9c8c90a2",
            "secret": "f64a4963151f3d31f3153806ad5fffdc",
        }
    ).json()

    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendOCR():
    access_token = get_access_token()

    response = requests.post(
        url="http://api.weixin.qq.com/cv/ocr/bizlicense",
        params={
            'ENCODE_URL': "https://pmoed23a4-pic39.websiteonline.cn/upload/sq20.png",
            'access_token': access_token
        }
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)

def sendmsg(openid, msg):
    access_token = get_access_token()

    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)

#sendmsg('oSLKY00WkGfHfCLaEIHUw8qwip9s','111111111111hihhihi')