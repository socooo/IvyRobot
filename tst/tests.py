# -*- coding:utf-8 -*-
from django.test import TestCase
from selenium import webdriver

# Create your tests here.
class Selenium_tst():
    def __init__(self):
        rtn = "999999"

    def selenium_tst_baidu1(self):
        driver = webdriver.Firefox()
        driver.get("https://www.baidu.com/")

        driver.find_element_by_id("kw").send_keys("Selenium2")
        driver.find_element_by_id("su").click()
        driver.quit()

    def selenium_tst_sina(self):
        driver = webdriver.Firefox()
        driver.get("https://mail.sina.com.cn/?from=mail")

        driver.find_element_by_id("freename").send_keys("xxxx@sina.com")
        driver.find_element_by_id("freepassword").send_keys("xxxxxx")
        driver.find_element_by_class_name("loginBtn").click()
        driver.quit()


import hashlib as hasher
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    str_sha = str(self.index) + \
                str(self.timestamp) + \
                str(self.data) + \
                str(self.previous_hash)
    str_sha = str_sha.encode("utf8")
    sha.update(str_sha)
    return sha.hexdigest()

import datetime as date
def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)


############################################
# zookeeper watch
############################################
import time
from kazoo.client import KazooClient
from kazoo.client import ChildrenWatch
from kazoo.client import DataWatch

"""
Watcher可以通过两种方式设置，一种是在调用ZK客户端方法的时候传递进去，比如 zk.get_children("/node", watch=FUN),但是这种方法是一次性的
也就是触发一次就没了，如果你还想继续监听一个事件就需要再次注册。
另外一种方法是通过高级API实现，监控数据或者节点变化，它只需要我们注册一次。一次性事件关注是zookeeper默认的即便在JAVA客户端里也是，这种高级别
API在JAVA里是zkclient，而在Python里面就是kazoo。高级API其实是对低级API的封装，对用户来讲更加好用。
"""

__metaclass__ = type


class zkWatcherTest:

    def __init__(self, host, port, timeout=10):
        self._nodename = ''
        self._host = host
        self._port = port
        self._timeout = timeout
        self._zk = KazooClient(hosts=self._host + ':' + self._port, timeout=self._timeout)
        self._zk.start()
        self._lastNodeList = []

    def start(self, zkPath):
        self._lastNodeList = self._zk.get_children(zkPath)
        try:
            ChildrenWatch(client=self._zk, path=zkPath, func=self._NodeChange)

            DataWatch(client=self._zk, path=zkPath, func=self._DataChange)
            # 这里的死循环就是为了不让程序退出，你可以把时间设置长一点观察，其实即便没有到60秒的睡眠时间，如果
            # 子节点或者节点数量发生变化也会收到通知。这里的wathch底层就是在节点上设置监听器，然后捕捉事件，如果有
            # 事件触发就调用你传递的方法来处理。
            while True:
                time.sleep(5)
                print("OK")
        except Exception as err:
            print(err.message)

    def _NodeChange(self, children):
        """
        处理子节点变化
        :param children: 这个参数并不需要你传递进来，因为把这个方法传递进ChiledrenWatcher，会返回一个当前子节点列表
        :return:
        """
        # print children
        # 如果新节点列表长度大于上次获取的节点列表长度，说明有增加
        if len(children) > len(self._lastNodeList):
            for node in children:
                if node not in self._lastNodeList:
                    print("新增加的节点为：", str(node))
                    self._lastNodeList = children
        else:
            for node in self._lastNodeList:
                if node not in children:
                    print("删除的节点为：", str(node))
                    self._lastNodeList = children

    def _DataChange(self, data, stat):
        """
        处理节点的数据变化
        :param data:
        :param stat:
        :return:
        """
        print("数据发生变化")
        print("数据为：", data)
        print("数据长度：", stat.dataLength)
        print("数据版本号version：", stat.version)
        print("cversion：", stat.cversion)
        print("子节点数量：", stat.numChildren)

def spark_streaming():
    import os, sys
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # config = configparser.ConfigParser()
    # config.read("mysite\myibs.ini")
    gv_SPARK_HOME = "D:\\workspace_python\\mysite\\spark-1.6.0-bin-hadoop2.6"
    #gv_SPARK_HOME = "D:\\workspace_python\\mysite\\spark-2.3.0-bin-hadoop2.7"

    os.environ["PYSPARK_PYTHON"] = "C:\\Python35\python"

    print(gv_SPARK_HOME)

    # os.environ['SPARK_HOME']='C:\\spark-1.6.0-bin-hadoop2.6'
    os.environ['SPARK_HOME'] = gv_SPARK_HOME
    SPARK_HOME = os.environ['SPARK_HOME']
    #HADOOP_HOME = 'D:\\workspace_scala\\Lib\\hadoop-common-2.2.0-bin-master'
    PY4J_DIR = os.path.normpath(SPARK_HOME + '/python/build')
    PYSPARK_DIR = os.path.normpath(SPARK_HOME + '/python')
    sys.path.insert(0, PY4J_DIR)
    sys.path.insert(0, PYSPARK_DIR)

    import sys, os
    from pyspark import SparkContext, SparkConf
    from operator import add
    import re
    from pyspark.streaming import StreamingContext

    sc = SparkContext(appName="wordsCount")
    ssc = StreamingContext(sc, 10) #10秒监听一次

    try:
        #lines = ssc.textFileStream('file:///D:\\workspace_python\\mysite\\log\\myibs.log')
        #lines = ssc.textFileStream('D:\\workspace_python\\mysite\\log\\myibs.log')
        lines = ssc.textFileStream('D:\\workspace_python\\mysite\\log')
        print("1", lines)
        words = lines.flatMap(lambda line: line.split(' '))
        print("2", words)
        wordCounts = words.map(lambda word: (word, 1)).reduceByKey(add)
        print("3=============================")
        wordCounts.pprint()
        print("4==============================")
        print(wordCounts)
        print("5")
        ssc.start()
        ssc.awaitTermination()
    except Exception as e:
        rtn_code = "011501"
        print(e)
    finally:
        sc.stop()

def URL_monitoring(url):


    try:

        f = open(r'D:\\workspace_python\\mysite\\dat\\monitor.log', "a+", encoding="utf-8")
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n")
        f.write("getting===>: " + url + "\n")
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("getting===>: " + url + "\n")

        import pygame
        pygame.mixer.init()
        track = pygame.mixer.music.load("D:\workspace_python\mysite\dat\Alarm10.wav")

        import re
        import urllib.request
        import ssl
        import sys

        ssl._create_default_https_context = ssl._create_unverified_context
        #url = "https://ebanking.fubonchina.com/pweb/prelogin.do"


        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode('utf-8')
        print(html)

        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"\n")
        f.write("\n" + html)

        rtn = html.find("9DhefwqGPrzGxEp9hPaoag")
        print(rtn)

        #if rtn >= 1 and len(html) >= 10000 :
        if len(html) >= 10000:
            print("ok")
            f.write("\nok\n")
        else:

            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"\n")
            print("connection error\n")
            f.write("connection error\n")

            x = range(0, 10)
            for y in x:
                pygame.mixer.music.play()
                time.sleep(3)
                sys.stdout.flush()
                print(y, end=">")
                sys.stdout.flush()
            print()

    except Exception as e:
        # rtn_code = "010101"
        # logger.error("post method:%s", rtn_code)
        # logger.error(e)
        print("connection error\n")
        x = range(0, 10)
        for y in x:
            pygame.mixer.music.play()
            time.sleep(3)
            print(y, end=">")
            sys.stdout.flush()
        print()

        print(e)
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"\n")
        f.write(str(e))
    finally:
        f.write("\n")
        f.close()

    time.sleep(1)

import random
class Tst_class_tst():
    lang = "Java"

    def __init__(self, name):
        self.lang = "python"
        self.name = name
        self.__weight = "ton1000"

    @classmethod
    def get_class_attr(cls):
        return cls.lang

    @staticmethod
    def select(n):
        a = random.randint(1,100)
        return a-n > 0

    @property  # 使用property对象调用私有变量，用函数调用
    def weight(self):
        return self.__weight

    def __priviateFun(self):
        return "__priviateFun"

    def pubFun(self):
        return self.__priviateFun()
#继承
class Tst_class_tst_1(Tst_class_tst):

    length = 1000
    @classmethod
    def get_length(self):
        return self.length

    #############################
    # Test Case1: selenium tst
    #############################
    # selenium_tst = Selenium_tst()
    # selenium_tst.selenium_tst_baidu1()

    #############################
    # Test Case2: Block Chain
    #############################
    # blockchain = [create_genesis_block()]
    # previous_block = blockchain[0]
    #
    # # How many blocks should we add to the chain
    # # after the genesis block
    # num_of_blocks_to_add = 20
    #
    # # Add blocks to the chain
    # for i in range(0, num_of_blocks_to_add):
    #   block_to_add = next_block(previous_block)
    #   blockchain.append(block_to_add)
    #   previous_block = block_to_add
    #   # Tell everyone about it!
    #   print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    #   print("Hash: {}\n".format(block_to_add.hash))

    #############################
    # Test Case3: zooKeeper watch
    #############################
    # try:
    #     zkwt = zkWatcherTest(host="192.168.179.160", port="2181")
    #     zkwt.start("/zktest")
    #
    #     # zkc.create('/zktest/tst222', b'test999') # 节点发生变化
    #     # zkc.set('/zktest/', b'test9992')         # 节点数据发生变化
    # except Exception as err:
    #     print(err)

    #############################
    # Test Case4: mmap
    #############################
    # from kernal import utility
    # print("---------")
    #
    # rtn_code = utility.set_mmap("aa", "bb")
    # print(rtn_code)
    #
    # rtn_code = utility.get_mmap("aa")
    # print(rtn_code)

    #############################
    # Test Case5: spark streaming
    #############################
    #spark_streaming()

    #############################
    # Test Case6: URL monitoring
    #############################
    # while 1 > 0:
    #     #URL_monitoring("https://ebanktest.fubonchina.com:602/eweb/")
    #     #URL_monitoring("https://ebanktest.fubonchina.com:602/pweb/")
    #     URL_monitoring("https://ebanking.fubonchina.com/pweb/prelogin.do")
    #     URL_monitoring("https://ebanking.fubonchina.com/eweb/prelogin.do")
    #     #URL_monitoring("https://ebanking.fubonchina2.com/eweb/prelogin1.do")
    #     time.sleep(60*3)

    # tst_class_tst = Tst_class_tst("girlA-Marry")
    # print(tst_class_tst.lang)
    # print(tst_class_tst.name)
    # print(tst_class_tst.get_class_attr())
    # print("<<<%s>>>" % (tst_class_tst.weight))
    # # tst_class_tst.__weight 无法调用私有类
    # # tst_class_tst.__privateFun() 无法调用私有类
    # print("tst_class_tst.pubFun：", tst_class_tst.pubFun())
    #
    # print( Tst_class_tst.select(5))
    #
    # tst_class_tst_1 = Tst_class_tst_1("boyB-Tom")
    # print(tst_class_tst_1.name)
    # print(tst_class_tst_1.get_length())


def drawGraphRelation():
    from pyecharts import Graph

    nodes = [{"name": "结点1", "symbolSize": 10},
             {"name": "结点2", "symbolSize": 20},
             {"name": "结点3", "symbolSize": 30},
             {"name": "结点4", "symbolSize": 40},
             {"name": "结点5", "symbolSize": 50},
             {"name": "结点6", "symbolSize": 40},
             {"name": "结点7", "symbolSize": 30},
             {"name": "结点8", "symbolSize": 20}]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get('name'), "target": j.get('name')})
    graph = Graph("关系图-力引导布局示例")
    graph.add("", nodes, links, repulsion=8000)
    graph.render()

def drawGraphRelation1():
    from pyecharts import Graph

    nodes = [{"name": "结点1", "symbolSize": 10},
             {"name": "结点2", "symbolSize": 20},
             {"name": "结点3", "symbolSize": 30},
             {"name": "结点4", "symbolSize": 40},
             {"name": "结点5", "symbolSize": 50},
             {"name": "结点6", "symbolSize": 40},
             {"name": "结点7", "symbolSize": 30},
             {"name": "结点8", "symbolSize": 20}]
    links = []
    for i in nodes:
        for j in nodes:
            links.append({"source": i.get('name'), "target": j.get('name')})
    graph = Graph("关系图-环形布局示例")
    graph.add(
        "",
        nodes,
        links,
        is_label_show=True,
        graph_repulsion=8000,
        graph_layout="circular",
        label_text_color=None,
    )
    graph.render()

def drawGraphRelation2():
    from pyecharts import Graph

    nodes = [
                {"name": "rule1", "symbolSize": 20},
                {"name": "rule2", "symbolSize": 20},
                {"name": "rule3", "symbolSize": 20},
                {"name": "rule4", "symbolSize": 20},
                {"name": "rule5", "symbolSize": 20},
                {"name": "rule6", "symbolSize": 20},
                {"name": "rule7", "symbolSize": 20},
                {"name": "rule8", "symbolSize": 20},
                {"name": "rule9", "symbolSize": 20},
                {"name": "rule1_1", "symbolSize": 10},
                {"name": "rule1_2", "symbolSize": 10},
                {"name": "rule1_3", "symbolSize": 10},
                {"name": "rule2_1", "symbolSize": 10},
                {"name": "rule2_2", "symbolSize": 10},
                {"name": "rule2_1_1", "symbolSize": 10},
                {"name": "rule2_1_2", "symbolSize": 10},
                {"name": "rule2_1_3", "symbolSize": 10},
                {"name": "rule2_2_1", "symbolSize": 10},
                {"name": "rule3_1", "symbolSize": 10},
                {"name": "rule3_2", "symbolSize": 10},
                {"name": "rule0", "symbolSize": 30}
            ]
    links = []

    links.append({"source": "rule0", "target": "rule1"})
    links.append({"source": "rule0", "target": "rule2"})
    links.append({"source": "rule0", "target": "rule3"})
    links.append({"source": "rule0", "target": "rule4"})
    links.append({"source": "rule0", "target": "rule5"})
    links.append({"source": "rule0", "target": "rule6"})
    links.append({"source": "rule0", "target": "rule7"})
    links.append({"source": "rule0", "target": "rule8"})
    links.append({"source": "rule0", "target": "rule9"})
    links.append({"source": "rule1", "target": "rule1_1"})
    links.append({"source": "rule1", "target": "rule1_2"})
    links.append({"source": "rule1", "target": "rule1_3"})
    links.append({"source": "rule2", "target": "rule2_1"})
    links.append({"source": "rule2", "target": "rule2_2"})
    links.append({"source": "rule2_1", "target": "rule2_1_1"})
    links.append({"source": "rule2_1", "target": "rule2_1_2"})

    links.append({"source": "rule2_1", "target": "rule2_2_1"})
    links.append({"source": "rule3", "target": "rule3_1"})
    links.append({"source": "rule3", "target": "rule3_2"})

    graph = Graph("Demo of Pyechart - Rule relationship")
    graph.add(
        "",
        nodes,
        links,
        is_label_show=True,
        #graph_repulsion=8000,
        graph_repulsion=80000,
        line_curve=0.2,
        graph_layout="circular",
        label_text_color=None,
    )
    graph.render()


def drawGrahBar():
    #from pyecharts import Bar
    from pyecharts.charts.bar import Bar
    # // 设置行名
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    #// 设置数据
    data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
    #// 设置柱状图的主标题与副标题
    bar = Bar("柱状图", "一年的降水量与蒸发量")
    #// 添加柱状图的数据及配置项
    bar.add("降水量", columns, data1, mark_line=["average"], mark_point=["max", "min"])
    bar.add("蒸发量", columns, data2, mark_line=["average"], mark_point=["max", "min"])
    #// 生成本地文件（默认为.html文件）
    bar.render()

def genTestDataMaster(recCnt, flushCnt):
    import random

    print('this message is from genTestData')

    rcdLst = []

    #自动生成测试数据
    for i_loop in range(0, recCnt):
        dictionary = "央广网天津月日消息记者苏平自贸区是国家制度创新的试验田依靠制度创新推动贸易自由化便利化年天津自贸试验区挂牌成立五周年五年来天津自贸区取得了许多先进经验与发展成果日前央广网记者参加行走自贸区活动走进天津自贸区参观中铁工程装备集团（天津）有限公司天津海特飞机工程有限公司用视频Vlog记录天津自贸区创新发展故事美国大选临近要尽己所能助拜登当选的特朗普侄女玛丽又跑出来曝叔叔黑料了月日她又在节目上曝光了一段自己秘密录制的特朗普岁姐姐玛丽安特朗普巴里的最新录音巴里在录音中吐槽特朗普自私小气至极没有原则还嘲讽特朗普的子女说其二儿子埃里克是白痴女儿伊万卡是迷你特朗普等等月日起乌鲁木齐城市公共交通服务将逐步有序恢复其中先行恢复条公交线路辆公交车占总车数的 % 同时辆出租车投入运营　　记者从乌鲁木齐市交通运输局了解到先行恢复的条公交线路首班时间：末班时间：发车间隔根据客流量适时调整根据要求恢复上线运营的从业人员将一律进行核酸检测对车辆技术状况进行安全检查及时消除安全隐患确保运营车辆状况良好后期将根据社区分区分级管控要求有序恢复BRT快速公交社区巴士和其余常规公交线路适时开通多样化公交线路出租车运力也将逐步增加为保证上线运营车辆达到疫情防控的要求从业人员将对车辆和场站进行全方位消毒特别是乘客接触的扶手车窗开关把手地板等加大消毒频次保证车厢内部和出租车内干净卫生司机出车前必须进行体温测量佩戴口罩运输过程中做到车内通风"

        s_no = str(i_loop)
        s_name = ""

        for i_loop_name in range(0, 3):
            s_rand_name = " "
            i_random=random.randint(0, 600)
            s_rand_name = dictionary[i_random]
            s_name = s_name + s_rand_name

        s_year = "20" + str(random.randint(0, 10)).zfill(2)
        s_month = str(random.randint(1, 12)).zfill(2)
        s_day = str(random.randint(1, 31)).zfill(2)
        s_birth = s_year + "-" + s_month + "-" + s_day

        s_age = str(random.randint(0, 30))

        i_sex = random.randint(0, 1)
        if i_sex == 1:
            s_sex = 'M'
        else:
            s_sex = 'F'

        s_score = str(random.randint(60, 100))

        s_desc = str(random.randint(0, 1000))

        s_rcd = s_no + "," + \
                s_name + "," + \
                s_birth + "," + \
                s_age + "," + \
                s_sex + "," + \
                s_score + "," + \
                s_desc
        rcdLst.append(s_rcd)

    save_file = "D:\workspace_python\practice\student_tb_txt.txt"
    with open(save_file, 'w+', encoding="utf-8") as file:
        iLoop = 0
        for rcd in rcdLst:
            file.write(rcd + "\n")
            if 1 == iLoop % flushCnt:
                print("flushing...", iLoop)
                file.flush()
            iLoop = iLoop + 1

def genTestDataTxn(recCnt, flushCnt):
    import random

    print('this message is from genTestData')

    rcdLst = []

    #自动生成测试数据
    for i_loop in range(0, recCnt):

        s_no = str(i_loop)

        for i_innerLoop in range(0, random.randint(1, 3)):
            s_txamt = str(round(random.uniform(0, 10000), 2))

            s_year = "20" + str(random.randint(0, 10)).zfill(2)
            s_month = str(random.randint(1, 12)).zfill(2)
            s_day = str(random.randint(1, 31)).zfill(2)
            s_txdate = s_year + "-" + s_month + "-" + s_day

            s_rcd = s_no + "," + \
                     s_txamt + "," + \
                     s_txdate

            rcdLst.append(s_rcd)

    save_file = "D:\workspace_python\practice\student_tb_score_txt.txt"
    with open(save_file, 'w+', encoding="utf-8") as file:
        iLoop = 0
        for rcd in rcdLst:
            file.write(rcd + "\n")
            if 1 == iLoop % flushCnt:
                print("flushing...", iLoop)
                file.flush()
            iLoop = iLoop + 1

def main():
    print('this message is from main function')
    # Graph()

# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
#  语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html
#  webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
#  语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
#  设置热词
#  注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
#  语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
#  可添加语种或方言，添加后会显示该方言的参数值
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat",
                             "language": "zh_cn",
                             "accent": "mandarin",
                             "vinfo":1,
                             "vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket消息的处理
def on_message(ws, message):
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

        else:
            data = json.loads(message)["data"]["result"]["ws"]
            # print(json.loads(message))
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]
            print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
    except Exception as e:
        print("receive msg,but parse exception:", e)



# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        frameSize = 8000  # 每一帧的音频大小
        intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open(wsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:

                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())


def xfTst():
    # 测试时候在此处正确填写相关信息即可运行
    time1 = datetime.now()

    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    time2 = datetime.now()
    print(time2-time1)


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
                respData1=respData.get("data").get("result")
                print(respData1)
                respData1 = respData1.get("trans_result")
                print("111" + respData1.get("dst"))

                # 以下仅用于调试
                code = str(respData["code"])
                if code != '0':
                    print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")



# wsParam = Ws_Param(APPID='5f5c4f75',
#                    APIKey='7a3136e4cac2160adb122031351fe0a4',
#                    APISecret='0672724ff7d71dc8fbbdcf98614aedb1',
#                    AudioFile=r'E:\workspace_python\mysite\dat\iat_pcm_16k.pcm')

wsParam = Ws_Param(APPID='5f5c4f75',
                   APIKey='7a3136e4cac2160adb122031351fe0a4',
                   APISecret='0672724ff7d71dc8fbbdcf98614aedb1',
                   AudioFile=r'E:\workspace_python\mysite\dat\iat_pcm_8k.pcm')


# wsParam = Ws_Param(APPID='5f5c4f75',
#                    APIKey='7a3136e4cac2160adb122031351fe0a4',
#                    APISecret='0672724ff7d71dc8fbbdcf98614aedb1',
#                    AudioFile=r'E:\workspace_python\mysite\dat\202009121357.mp3')

# wsParam = Ws_Param(APPID='5f5c4f75',
#                    APIKey='7a3136e4cac2160adb122031351fe0a4',
#                    APISecret='0672724ff7d71dc8fbbdcf98614aedb1',
#                    AudioFile=r'E:\workspace_python\mysite\dat\iat_mp3_8k.mp3')

if __name__ == '__main__':
    #main()
    #drawGrahBar()
    #drawGraphRelation()
    #drawGraphRelation1()
    #drawGraphRelation2()
    #genTestData(1000000, 50000)
    #genTestDataMaster(1000000, 50000)
    #genTestDataTxn(1000000, 50000)

    #xfTst()

    ##示例:  host="itrans.xfyun.cn"域名形式
    host = "itrans.xfyun.cn"
    # 初始化类
    gClass = get_result(host)
    gClass.call_url()

