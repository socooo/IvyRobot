from django.shortcuts import render
import logging
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient
import webbrowser
import time
import random
import requests
import datetime
import hashlib
import base64
import hmac
import json


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
            # 操作步骤
            # 1. 获取token https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx7a6557af9c8c90a2&secret=f64a4963151f3d31f3153806ad5fffdc
            # {"access_token":"37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT","expires_in":7200}
            # 2. 用 curl 命令上传， 获取media id
            # curl -F media=@pic_20200913094903.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT&type=image"
            # {"type":"image","media_id":"pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp","created_at":1599978388,"item":[]}

            # curl -F media=@pic_20200913094903.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT&type=image"
            # curl -F media=@pic_20200913094926.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
            # curl -F media=@pic_20200913094930.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
            # curl -F media=@pic_20200913094936.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
            # curl -F media=@pic_20200913094939.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
            # curl -F media=@pic_20200913094943.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"

            # {"type":"image","media_id":"pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp","created_at":1599978388,"item":[]}
            # {"type":"image","media_id":"7TbNnXyrhQD9KGvOHjBjmELTItqoHidETXicRQI9zDleeYoMA784a6bryv825OSP","created_at":1599981452,"item":[]}
            # {"type":"image","media_id":"82O86-UuA35t3H5YLLJ4T9Gqf6NRXigVIN7OW_cz94L8yHfTY7Llkyjn87LpG9Ie","created_at":1599981452,"item":[]}
            # {"type":"image","media_id":"xSmfJ-ojvLfPDpBV1POkR5oMDKQfBvq1mgJfRYx4jWtbTxpCkJSiVvHqGthMbR-b","created_at":1599981453,"item":[]}
            # {"type":"image","media_id":"cLEOnDtpC9m7BXoidmonprJBhbgA5OgRVgLRDnCjPh92gl7kfHBJznCygT6LZhNF","created_at":1599981453,"item":[]}
            # {"type":"image","media_id":"i6Zue_tEifD9gRW2BuvEW4Yln9EBEX-1ZccqQd4pAMSyGk8pO-60BV9DcDM36Cb-","created_at":1599981455,"item":[]}

            # content = "pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp"
            # replyMsg = PicMsg(toUser, fromUser, content)
            # return replyMsg.send()

            Recognition=""

            #IMAGE_URL = "http://mmbiz.qpic.cn/mmbiz_jpg/CLqPKppc0gnhKzljsNq69ZvrFdjPxNZoHBIlp0JpiaehSSIZB1MaJsiabYTJZcz8PYHtWMMKpmia0GyJRPAhVOkvQ/0"
            picUrl = xmlData.find('PicUrl').text
            imgFile = "E:\workspace_python\mysite\dat\\businesscard1.png"
            from urllib.request import urlretrieve
            urlretrieve(picUrl, imgFile)

            # imgFile = "E:\workspace_python\mysite\dat\\businesscard1.png"
            # #imgFile = picUrl

            #print("111" + imgFile)
            sRtn = baiduOcr(imgFile)
            #print("222" + imgFile)
            content = "你说的是:" + Recognition + "\n" \
                      "处理结果是：" + sRtn
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'voice':
            Recognition = xmlData.find('Recognition').text
            print(Recognition)

            if Recognition.find("怎么用") == 0 or \
                    Recognition.find("菜单") == 0 or \
                    Recognition.find("帮助") == 0 or \
                    Recognition.find("救命") == 0 or \
                    Recognition.find("手册") == 0:
                actStatus = "请查看Ivy robot 使用指南：http://snetlogon20.imwork.net/article/article-detail/15/Ivy-robot-Shi-Yong-Zhi-Nan"

            elif Recognition.find("写工作报告") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-post/")
                actStatus = "请开始处理工作报告: http://snetlogon20.imwork.net/article/article-post/"
            elif Recognition.find("查看工作报告") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-list/")
                actStatus = "请查看工作报告: http://snetlogon20.imwork.net/article/article-list/"
            elif Recognition.find("报修") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-list/")
                actStatus = "请选择正确条目报修: http://snetlogon20.imwork.net/article/article-post/"
            elif Recognition.find("预定工位") == 0:
                webbrowser.open("http://snetlogon20.imwork.net/article/article-list/")
                actStatus = "风水工位，速度抢: http://snetlogon20.imwork.net/article/article-post/"

            elif Recognition.find("客户信息登记") == 0 or Recognition.find("登记客户信息") == 0:
                actStatus = "请至客户信息登记: http://snetlogon20.imwork.net/cif/cifmas_add/"
            elif Recognition.find("客户信息查询") == 0 or Recognition.find("查询客户信息") == 0:
                actStatus = "请至客户信息查询: http://snetlogon20.imwork.net/cif/cifmas_lst/"
            elif Recognition.find("客户信息报表") == 0:
                actStatus = "请查看客户信息: http://snetlogon20.imwork.net/cif/cifmas_echart_0001/"

            elif Recognition.find("词频分析") == 0:
                actStatus = "请查看词频分析: http://snetlogon20.imwork.net/cif/cifmas_echart_0002/"
                #webbrowser.open("http://snetlogon20.imwork.net/cif/cifmas_echart_0002/")
                webbrowser.open("http://snetlogon20.imwork.net/cif/cifmas_echart_0001/")
            elif Recognition.find("回归分析") == 0:
                actStatus = "请查看归分析: http://snetlogon20.imwork.net/cif/cifmas_echart_0003/"
                #webbrowser.open("http://snetlogon20.imwork.net/cif/cifmas_echart_0003/")

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
            elif Recognition.find("风景") == 0 or \
                    Recognition.find("休息一下") == 0 or \
                    Recognition.find("上海风光") == 0 or \
                    Recognition.find("开会小差") == 0:
                # curl -F media=@pic_20200913094903.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT&type=image"
                # curl -F media=@pic_20200913094926.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@pic_20200913094930.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@pic_20200913094936.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@pic_20200913094939.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@pic_20200913094943.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"

                # {"type":"image","media_id":"pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp","created_at":1599978388,"item":[]}
                # {"type":"image","media_id":"7TbNnXyrhQD9KGvOHjBjmELTItqoHidETXicRQI9zDleeYoMA784a6bryv825OSP","created_at":1599981452,"item":[]}
                # {"type":"image","media_id":"82O86-UuA35t3H5YLLJ4T9Gqf6NRXigVIN7OW_cz94L8yHfTY7Llkyjn87LpG9Ie","created_at":1599981452,"item":[]}
                # {"type":"image","media_id":"xSmfJ-ojvLfPDpBV1POkR5oMDKQfBvq1mgJfRYx4jWtbTxpCkJSiVvHqGthMbR-b","created_at":1599981453,"item":[]}
                # {"type":"image","media_id":"cLEOnDtpC9m7BXoidmonprJBhbgA5OgRVgLRDnCjPh92gl7kfHBJznCygT6LZhNF","created_at":1599981453,"item":[]}
                # {"type":"image","media_id":"i6Zue_tEifD9gRW2BuvEW4Yln9EBEX-1ZccqQd4pAMSyGk8pO-60BV9DcDM36Cb-","created_at":1599981455,"item":[]}


                # content = "pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp"
                # replyMsg = PicMsg(toUser, fromUser, content)
                # return replyMsg.send()

                dictPic = {
                        '1': 'pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp',
                        '2': '7TbNnXyrhQD9KGvOHjBjmELTItqoHidETXicRQI9zDleeYoMA784a6bryv825OSP',
                        '3': '82O86-UuA35t3H5YLLJ4T9Gqf6NRXigVIN7OW_cz94L8yHfTY7Llkyjn87LpG9Ie',
                        '4': 'xSmfJ-ojvLfPDpBV1POkR5oMDKQfBvq1mgJfRYx4jWtbTxpCkJSiVvHqGthMbR-b',
                        '5': 'cLEOnDtpC9m7BXoidmonprJBhbgA5OgRVgLRDnCjPh92gl7kfHBJznCygT6LZhNF',
                        '6': 'i6Zue_tEifD9gRW2BuvEW4Yln9EBEX-1ZccqQd4pAMSyGk8pO-60BV9DcDM36Cb-'
                        }
                randPicId = str(random.randint(1, 6))
                print("-----100:" + randPicId)
                content = dictPic[randPicId]
                print("-----101:" + content)
                replyMsg = PicMsg(toUser, fromUser, content)
                return replyMsg.send()

            elif Recognition.find("翻译") == 0:

                # host = "itrans.xfyun.cn"
                # gClass = get_result(host)
                # content = gClass.call_url()
                # print("33333" + content)
                # replyMsg = VoiceMsg(toUser, fromUser, content)
                # return replyMsg.send()
                print("11111111")
                content = Recognition.encode()
                base64_content = base64.b64encode(content)
                actStatus = 'http://snetlogon20.imwork.net/cif/cifmas_amd_translate/3666/?content=' + base64_content
            elif Recognition.find("唱首歌") == 0:
                content = "M63XDVxr_p1KwAS3OlAg__EK0Wf29wlLl5azocbDlGve-e8xYSoxFZJbBzxyisTQ"
                replyMsg = VoiceMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif Recognition.find("讲个笑话") == 0:
                # curl -F media=@3d11-iyywcsz3854025.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@864a-iyywcsz3854630.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@c6b2-iyywcsz0331990.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@af1a-iyywcsz0324003.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@5ec6-iyywcsz0315752.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
                # curl -F media=@1868-iyywcsz0309273.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"

                # {"type":"image","media_id":"D3yY1VUVVeFu2GC8HpCxlzJEKnvBBpZJQ7SSnCgK4JeVRg-UFki19GXjypuCJvo3","created_at":1599982605,"item":[]}
                # {"type":"image","media_id":"bQl1fqnUfJgnienEHUesr2jo4VBoOkBx-zrLDExP-dzI5LmuQpWvOAFsbUDcR2hW","created_at":1599982607,"item":[]}
                # {"type":"image","media_id":"Zzosj6so0iEqYbXx9HftXQ5_bA3UL1rpaYxWFXLMW9h8AW9ocxGa31LcBIjTFM1y","created_at":1599982608,"item":[]}
                # {"type":"image","media_id":"DH_BfCw7Gkx4bD8E_Mwv4bF3uSGumIJ-yiQcgt3RA4O5u0tPp5UMCj1vDYTGoGkT","created_at":1599982767,"item":[]}
                # {"type":"image","media_id":"vVXTM9ibCB40LT5r0kmjzJqzwKAshnNuLsCO-jVUQh0sKDmtALiJr7Hx1yJ5yYmN","created_at":1599982768,"item":[]}
                # {"type":"image","media_id":"52xfSk7_-DOz48lfOzyNpyle1s0hsrMU6FdHgaKuo-oL99spR_lUQ_3ZU1unUgYn","created_at":1599982769,"item":[]}

                dictPic = {
                        '1': 'D3yY1VUVVeFu2GC8HpCxlzJEKnvBBpZJQ7SSnCgK4JeVRg-UFki19GXjypuCJvo3',
                        '2': 'bQl1fqnUfJgnienEHUesr2jo4VBoOkBx-zrLDExP-dzI5LmuQpWvOAFsbUDcR2hW',
                        '3': 'Zzosj6so0iEqYbXx9HftXQ5_bA3UL1rpaYxWFXLMW9h8AW9ocxGa31LcBIjTFM1y',
                        '4': 'DH_BfCw7Gkx4bD8E_Mwv4bF3uSGumIJ-yiQcgt3RA4O5u0tPp5UMCj1vDYTGoGkT',
                        '5': 'vVXTM9ibCB40LT5r0kmjzJqzwKAshnNuLsCO-jVUQh0sKDmtALiJr7Hx1yJ5yYmN',
                        '6': '52xfSk7_-DOz48lfOzyNpyle1s0hsrMU6FdHgaKuo-oL99spR_lUQ_3ZU1unUgYn'
                        }
                randPicId = str(random.randint(1, 6))
                print("-----100:" + randPicId)
                content = dictPic[randPicId]
                print("-----101:" + content)
                replyMsg = PicMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif Recognition.find("小视频") == 0:
                dictPic = {
                        '1': 'rlFrM_m9kEZsNmb7f1tItLqCynq1_du0upBwaW8WnhebX7eoYwJIdIciGk66NR1y'
                        }
                randPicId = str(random.randint(1, 6))
                #print("-----100:" + randPicId)
                content = dictPic['1']
                #print("-----101:" + content)
                replyMsg = VideoMsg(toUser, fromUser, content, '小视频',' 放松一下')
                return replyMsg.send()
            elif Recognition.find("IV") == 0 or \
                Recognition.find("艾薇儿") == 0 or \
                Recognition.find("你好") == 0 or \
                Recognition.find("机器人") == 0:
                print("111")
                if 1 == random.randint(1, 2):
                    dictPic = {
                            '1': "mHqR8jJNxZfKXmvzD7eUq3KRMy4dqpzsDvref_aFrmeaMNhOnGj_nAnvDk91F0a-",
                            '2': "34GskaTiacaItLqenOp1_i4q1MXPJGwYuh_KT_QxD1enRGfLG4CYLu3xjCCfmCUp",
                            '3': "tiYAzYtR_3Ocht9HDnxkPzfx2rwf4EIY-XUKxjTNsphDeooF_i6o4vt5ttZqgNTp"
                            }
                    print("222")
                    content = dictPic[str(random.randint(1, 3))]
                    print("222" + content)
                    replyMsg = VoiceMsg(toUser, fromUser, content)
                    print("333")
                    return replyMsg.send()
                else:
                    print("22211")
                    dictPic = {
                        '1': '1Bvm07BkDYoMQpnNi664kPQr8T3k0dwtuqpRMSdu2wrr7Lv-MmrG_VRFPhqBQ0Yo'
                    }
                    content = dictPic['1']
                    print("222122")
                    replyMsg = VideoMsg(toUser, fromUser, content, '我是 Ivy Robot', '有什么可以帮到你？')
                    return replyMsg.send

            elif Recognition.find("文字识别") == 0:
                imgFile = "E:\workspace_python\mysite\dat\\businesscard.png"
                sRtn = baiduOcr(imgFile)
                content = "你说的是:" + Recognition + "\n" \
                        "处理结果是：" + sRtn
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                #actStatus = "实在不知道你说啥。\n要不看看Ivy robot 使用指南：http://localhost:8001/article/article-detail/15/Ivy-robot-Shi-Yong-Zhi-Nan/"
                actStatus= "实在不知道你说啥。\n 请尝试对Ivy robot 说出以下指令：\n" \
                "1)工作类                     \n" \
                "  写工作报告                     \n" \
                "  查看工作报告                     \n" \
                "  报修                     \n" \
                "2)营运类                     \n" \
                "  客户信息登记                     \n" \
                "  客户信息查询                     \n" \
                "  客户信息报表                     \n" \
                "3)休闲类                     \n" \
                "    小视频                     \n" \
                "    风景                     \n" \
                "    讲个笑话                     \n" \
                "    唱首歌                     \n" \
                "4)工具类                     \n" \
                "  百度                     \n" \
                "  看新闻                     \n" \
                "  外卖                     \n" \
                "  自助下单                     \n" \
                "  美团                     \n" \
                "  饿了吗                     \n" \
                "或者使用指南：http://http://snetlogon20.imwork.net/article/article-detail/15/Ivy-robot-Shi-Yong-Zhi-Nan/"

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
            replyMsg = VideoMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到, 出动Ivy Robot, 乘风破浪也要来接你 谢谢"

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
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['media_id'] = content

    def send(self):
        #print("----301 PicMsg here:" + self.__dict['media_id'])
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
            <MediaId><![CDATA[{media_id}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)


class VideoMsg(Msg):
    def __init__(self, toUserName, fromUserName, content, title, description):
        print("----300 VideoMsg here:" + content)
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['media_id'] = content
        self.__dict['title'] = title
        self.__dict['description'] = description
        print("----301 VideoMsg here:" + content)

    def send(self):
        print("----302 VideoMsg here:" + self.__dict['media_id'])
        XmlForm = """
            <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
              <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
              <CreateTime>{CreateTime}</CreateTime>
              <MsgType><![CDATA[video]]></MsgType>
              <Video>
                <MediaId><![CDATA[{media_id}]]></MediaId>
                <Title><![CDATA[{title}]]></Title>
                <Description><![CDATA[{description}]]></Description>
              </Video>
            </xml>
        """
        print("----304:" + XmlForm)
        return XmlForm.format(**self.__dict)


class VoiceMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        print("----300 VoiceMsg here:" + content)
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['media_id'] = content
        print(self.__dict)

    def send(self):
        #print("----301 VoiceMsg here:" + self.__dict['media_id'])
        XmlForm = """
            <xml>
              <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
              <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
              <CreateTime>12345678</CreateTime>
              <MsgType><![CDATA[voice]]></MsgType>
              <Voice>
                <MediaId><![CDATA[{media_id}]]></MediaId>
              </Voice>
            </xml>
        """
        #print("----303:" + XmlForm)
        return XmlForm.format(**self.__dict)

#定制菜单
#http://snetlogon20.imwork.net/wechat/create_menu/
def create_menu(request):
	# 第一个参数是公众号里面的appID，第二个参数是appsecret
    #20200912
    #client = WeChatClient("wxf1f84216155f1f4f", "60b3a0ed8186ee298050625f08934a85")

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
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": "wx3a9cda89ad5d9781",
            "secret": "bde750fa7404467204f1b967cbcba353",
        }
    ).json()
    #use this new one
    # result = requests.get(
    #     url="https://api.weixin.qq.com/cgi-bin/token",
    #     params={
    #         "grant_type": "client_credential",
    #         "appid": "wx7a6557af9c8c90a2",
    #         "secret": "f64a4963151f3d31f3153806ad5fffdc",
    #     }
    # ).json()

    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendmsg(openid, msg):
    access_token = get_access_token()
    print("111111" + access_token)
    body = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    print("22222")
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            'access_token': access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    print("33333")
    result = response.json()
    print(result)

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

def baiduOcr(imgFile):

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = "0uoYudojH10xplnUwX5QLUCo"
    client_secret = "jX02hDQ0EGpm1hFxr5hMblZRye6vnUGT"
    #imgFile = "E:\workspace_python\mysite\dat\\businesscard.png"

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    #if response:
        #print(response.json())
    dictResp = response.json()

    '''
    通用文字识别
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(imgFile, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = dictResp.get("access_token")
    request_url = request_url + "?access_token=" + access_token
    #print(request_url)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    # if response:
    #     print(response.json())
    dictResp = response.json()
    wordList=dictResp.get("words_result")
    print("1111")
    sRtn=""
    for word in wordList:
        wordDict = word
        print(wordDict.get("words"))
        sRtn = sRtn + wordDict.get("words")
    return sRtn



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

    def call_url(self):
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

                # 以下仅用于调试
                code = str(respData["code"])
                if code != '0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")

                sRtn=respData.get("data").get("result")
                sRtn = sRtn.get("trans_result")
                sRtn = sRtn.get("dst")
                return sRtn

#sendmsg('oSLKY00WkGfHfCLaEIHUw8qwip9s','111111111111hihhihi')

#https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx7a6557af9c8c90a2&secret=f64a4963151f3d31f3153806ad5fffdc
#{"access_token":"37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT","expires_in":7200}

#curl -F media=@pic_20200913094903.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_Xsx15KPtCLOsglWuHHnScLVsdVSVNb4YqZzrD9hYDd9G0tAy_EP8IX3CIaFQ0el0cVXU-7p_oXThKuWjNOgZzO_5tFYXJaypXErKHs2vG0VvBgGyieVnzox2Spffd5wZTpP4p5OIHNPaItH7NNMhAJAUUT&type=image"
#curl -F media=@pic_20200913094926.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@pic_20200913094930.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@pic_20200913094936.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@pic_20200913094939.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@pic_20200913094943.jpg "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"

#{"type":"image","media_id":"pT6emwXlcj_nWAtApu0PDez9eW9ZH_1Frstnjj-lM5TYdInCWlZCRTX9jixfNqYp","created_at":1599978388,"item":[]}
#{"type":"image","media_id":"7TbNnXyrhQD9KGvOHjBjmELTItqoHidETXicRQI9zDleeYoMA784a6bryv825OSP","created_at":1599981452,"item":[]}
#{"type":"image","media_id":"82O86-UuA35t3H5YLLJ4T9Gqf6NRXigVIN7OW_cz94L8yHfTY7Llkyjn87LpG9Ie","created_at":1599981452,"item":[]}
#{"type":"image","media_id":"xSmfJ-ojvLfPDpBV1POkR5oMDKQfBvq1mgJfRYx4jWtbTxpCkJSiVvHqGthMbR-b","created_at":1599981453,"item":[]}
#{"type":"image","media_id":"cLEOnDtpC9m7BXoidmonprJBhbgA5OgRVgLRDnCjPh92gl7kfHBJznCygT6LZhNF","created_at":1599981453,"item":[]}
#{"type":"image","media_id":"i6Zue_tEifD9gRW2BuvEW4Yln9EBEX-1ZccqQd4pAMSyGk8pO-60BV9DcDM36Cb-","created_at":1599981455,"item":[]}


#curl -F media=@3d11-iyywcsz3854025.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@864a-iyywcsz3854630.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@c6b2-iyywcsz0331990.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@af1a-iyywcsz0324003.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@5ec6-iyywcsz0315752.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"
#curl -F media=@1868-iyywcsz0309273.gif "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_lymjNwa5pTZz2pkX_6LT-KXJVWpAQ8bmDUWqCabX8w_WavOhiBu4LO-2XVSf5hFLdbrDBSqNISXF6LIBhL9F0G2wzO_Ci2ivd9adalb-Mv40m8A3zNitHuJM5NIHBQa_ysC3ZKY9EcMz_MI1QAJcAIAGQZ&type=image"

#{"type":"image","media_id":"D3yY1VUVVeFu2GC8HpCxlzJEKnvBBpZJQ7SSnCgK4JeVRg-UFki19GXjypuCJvo3","created_at":1599982605,"item":[]}
#{"type":"image","media_id":"bQl1fqnUfJgnienEHUesr2jo4VBoOkBx-zrLDExP-dzI5LmuQpWvOAFsbUDcR2hW","created_at":1599982607,"item":[]}
#{"type":"image","media_id":"Zzosj6so0iEqYbXx9HftXQ5_bA3UL1rpaYxWFXLMW9h8AW9ocxGa31LcBIjTFM1y","created_at":1599982608,"item":[]}
#{"type":"image","media_id":"DH_BfCw7Gkx4bD8E_Mwv4bF3uSGumIJ-yiQcgt3RA4O5u0tPp5UMCj1vDYTGoGkT","created_at":1599982767,"item":[]}
#{"type":"image","media_id":"vVXTM9ibCB40LT5r0kmjzJqzwKAshnNuLsCO-jVUQh0sKDmtALiJr7Hx1yJ5yYmN","created_at":1599982768,"item":[]}
#{"type":"image","media_id":"52xfSk7_-DOz48lfOzyNpyle1s0hsrMU6FdHgaKuo-oL99spR_lUQ_3ZU1unUgYn","created_at":1599982769,"item":[]}


#voice
'''
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx7a6557af9c8c90a2&secret=f64a4963151f3d31f3153806ad5fffdc
{"access_token":"37_TQHp-XM5XaackCIfoOt2m4LyE8-1qzNFPhkgu9vW2sdzJxXc87jHxuwb8dUjVrnZEcytz8s1gpbJG-NJ-BfAKoPw 8zyBM13v6wzARTGmAyA","expires_in":7200}

curl -F media=@E:\workspace_python\mysite\dat\ivy1.mp3 "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_FQZUwzPSACkrH8tILeLwnZ7hH0FbLPvJYxzihI5coEYDmmYqmWS8O9d5JT12yUVhRrrtC9s7tJKtEZn5MkqszY4d6YAW2MZsnuMMSGyEuSy2GSJJAaFtGjwOIjrG1tp9777jfEZ2iEqM4oETXYOiACAJKA&type=voice"
curl -F media=@E:\workspace_python\mysite\dat\ivy2.mp3 "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_FQZUwzPSACkrH8tILeLwnZ7hH0FbLPvJYxzihI5coEYDmmYqmWS8O9d5JT12yUVhRrrtC9s7tJKtEZn5MkqszY4d6YAW2MZsnuMMSGyEuSy2GSJJAaFtGjwOIjrG1tp9777jfEZ2iEqM4oETXYOiACAJKA&type=voice"
curl -F media=@E:\workspace_python\mysite\dat\ivy3_en.mp3 "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_FQZUwzPSACkrH8tILeLwnZ7hH0FbLPvJYxzihI5coEYDmmYqmWS8O9d5JT12yUVhRrrtC9s7tJKtEZn5MkqszY4d6YAW2MZsnuMMSGyEuSy2GSJJAaFtGjwOIjrG1tp9777jfEZ2iEqM4oETXYOiACAJKA&type=voice"
curl -F media=@E:\workspace_python\mysite\dat\IvyVideo.mp4 "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=37_FQZUwzPSACkrH8tILeLwnZ7hH0FbLPvJYxzihI5coEYDmmYqmWS8O9d5JT12yUVhRrrtC9s7tJKtEZn5MkqszY4d6YAW2MZsnuMMSGyEuSy2GSJJAaFtGjwOIjrG1tp9777jfEZ2iEqM4oETXYOiACAJKA&type=video"

{"type":"voice","media_id":"mHqR8jJNxZfKXmvzD7eUq3KRMy4dqpzsDvref_aFrmeaMNhOnGj_nAnvDk91F0a-","created_at":1600175905,"item":[]}
{"type":"voice","media_id":"34GskaTiacaItLqenOp1_i4q1MXPJGwYuh_KT_QxD1enRGfLG4CYLu3xjCCfmCUp","created_at":1600175909,"item":[]}
{"type":"voice","media_id":"tiYAzYtR_3Ocht9HDnxkPzfx2rwf4EIY-XUKxjTNsphDeooF_i6o4vt5ttZqgNTp","created_at":1600175911,"item":[]}
{"type":"voice","media_id":"p9YRDGwJBLuE3rDuB09n41jIpurVdvfWP-MxJN-IJsVws6ImrFufIXHed3eeoD0A","created_at":1600175915,"item":[]}
{"type":"video","media_id":"1Bvm07BkDYoMQpnNi664kPQr8T3k0dwtuqpRMSdu2wrr7Lv-MmrG_VRFPhqBQ0Yo","created_at":1600176424,"item":[]}
'''