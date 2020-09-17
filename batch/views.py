# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# default liberary to be imported
import time
import logging
import threading
import sys

from kernal import utility
from batch import asyn_TCP_server_001
from batch import asyn_TCP_server

logger = logging.getLogger('sourceDns.webdns.views')
rtn_code = "999999"

from interface import client
import configparser
myibs_ini = "mysite\myibs.ini"

# batch_job_001, excuted on very 5 seconds
def batch_job_001():

    logger.info("starting batch_job_001...")

    if_batch_start = utility.get_myibs_ini("batch", "batch_job_001_start")
    batch_start_date = utility.get_myibs_ini("batch", "batch_job_001_start_date")
    batch_start_time = utility.get_myibs_ini("batch", "batch_job_001_start_time")
    batch_job_001_internal_time = utility.get_myibs_ini("batch", "batch_job_001_internal_time")
    batch_job_001_job = utility.get_myibs_ini("batch", "batch_job_001_job")

    log_string = "interval (" + batch_job_001_internal_time + "s):" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " +\
                 if_batch_start + " " + \
                 batch_start_date + " " + \
                 batch_start_time
    logger.info(log_string)

    if if_batch_start == "True":
        pass
    else:
        return "000001"

    rtn = utility.compare_string_with_now(batch_start_date, "days")
    if rtn.days < 0:
        logger.info("day<0, exit")
        return "000002"
    else:
        logger.info("day>=0, go on")

    rtn = utility.compare_string_with_now(batch_start_time, "seconds")
    if rtn.days < 0:
        logger.info("time.days<0, exit")
        return "000003"

    if rtn.seconds <= 0:
        logger.info("time.seconds<0, exit")
        return "000004"
    else:
        logger.info("time.seconds>0, go on")
        pass

    ###########################
    # scheduled job start here
    ###########################
    # redis_cli = utility.Redis_cli()
    # for i in range(1, 100):
    #     rtn = redis_cli.set_redis(i, i)
    #
    # from interface import client
    # sftp = client.sftp_client()
    # commands = ['ls ~', 'ls /', 'ls /tmp', 'get /tmp/kernal_parm_mas_tst.sql e:\\tmp\\kernal_parm_mas_tst.sql']
    # rtn_dict = sftp.sftp_read(commands)
    # print(rtn_dict, rtn_dict["rtn_code"], rtn_dict["rsp_msg"])
    # rtn_dict = sftp.sftp_get('/tmp/kernal_parm_mas_tst.sql', 'e:\\tmp\\hadoop-root-datanode.pid')
    # print(rtn_dict)
    # rtn_dict = sftp.sftp_put('e:\\tmp\\hadoop-root-datanode.pid', '/tmp/hadoop-root-datanode.pid')
    # print(rtn_dict)


    # 1. 先查看进程状态
    thread_list = []
    threads = threading.enumerate()
    batch_job_001_status = "---"

    server_name = batch_job_001_job

    for thread in threads:
        # stack = sys._current_frames()[thread.ident]
        thread_list.append("\nThread ID: %s, Name: %s\n" % (thread.ident, thread.name))
        # print(thread.name)
        if thread.name == server_name:
            batch_job_001_status = "STARTED"
            break

    # 2. 如进程已启动就不必再启动了, 确保只有一个服务端启动
    if batch_job_001_status == "STARTED":
        print("Try to start the TCP server. However server started, quit.")
        logger.info("try to start the TCP server. However server started, quit.")
        pass
    else:
        logger.info("scheduled job start here.....")

        # 3. 采用工厂模式装配对象
        asyn_tcp_server = asyn_TCP_server.async_TCP_Server_Factory().create_async_TCP_Server(server_name)

        # 4. 采用异步方式调起后台socket进程
        t = threading.Thread(target=asyn_tcp_server.tcpServer(), name=server_name, args=(server_name,))

        print("Thread " + server_name + " starting here")
        logger.info("Thread " + server_name + " starting...")

        t.start()

        print("Thread " + server_name + " started.")
        logger.info("Thread " + server_name + " started.")

    return rtn_code


# batch_job_002, excuted on very 60 seconds
def batch_job_002():
    if_batch_start = utility.get_myibs_ini("batch", "batch_job_002_start")
    batch_start_date = utility.get_myibs_ini("batch", "batch_job_002_start_date")
    batch_start_time = utility.get_myibs_ini("batch", "batch_job_002_start_time")
    batch_job_001_internal_time = utility.get_myibs_ini("batch", "batch_job_002_internal_time")

    log_string = "interval (" + batch_job_001_internal_time + "s):" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " +\
                 if_batch_start + " " + \
                 batch_start_date + " " + \
                 batch_start_time
    logger.info(log_string)

    if if_batch_start == "True":
        pass
    else:
        return "000001"

    rtn = utility.compare_string_with_now(batch_start_date, "days")
    if rtn.days < 0:
        logger.info("day<0, exit")
        return "000002"
    else:
        logger.info("day>=0, go on")

    rtn = utility.compare_string_with_now(batch_start_time, "seconds")
    if rtn.days < 0:
        logger.info("time.days<0, exit")
        return "000003"

    if rtn.seconds <= 0:
        logger.info("time.seconds<0, exit")
        return "000004"
    else:
        logger.info("time.seconds>0, go on")
        pass

    ###########################
    # scheduled job start here
    ###########################
    # 1. 先查看进程状态
    thread_list = []
    threads = threading.enumerate()
    batch_job_002_status = "---"
    for thread in threads:
        thread_list.append("Thread ID: %s, Name: %s" % (thread.ident, thread.name))
        # print(thread.name)
        if thread.name == "asyn_TCP_client_001":
            batch_job_002_status = "STARTED"
            break

    # 2. 如进程已启动就不必再启动了, 确保只有一个服务端启动
    if batch_job_002_status == "STARTED":
        print("Try to start the TCP client. However client started, quit.")
        logger.info("Try to start the TCP client. However client started, quit.")
        pass
    else:

        logger.info("scheduled job start here.....")

        # 采用异步方式调起后台socket进程
        msg="abcde"
        t = threading.Thread(target=asyn_TCP_server_001.tcpClient, name='asyn_TCP_client_001', args=(msg,))

        print("Thread asyn_TCP_client_001 starting here")
        logger.info("Thread asyn_TCP_client_001 starting...")

        t.start()

        print("Thread asyn_TCP_client_001 started.")
        logger.info("Thread asyn_TCP_client_001 started.")

    return rtn_code

# 读取参数，每X秒刷新Redis
def batch_job_003():
    if_batch_start = utility.get_myibs_ini("batch", "batch_job_003_start")
    batch_start_date = utility.get_myibs_ini("batch", "batch_job_003_start_date")
    batch_start_time = utility.get_myibs_ini("batch", "batch_job_003_start_time")
    batch_job_001_internal_time = utility.get_myibs_ini("batch", "batch_job_003_internal_time")

    log_string = "interval (" + batch_job_001_internal_time + "s):" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " +\
                 if_batch_start + " " + \
                 batch_start_date + " " + \
                 batch_start_time
    logger.info(log_string)

    if if_batch_start == "True":
        pass
    else:
        return "000001"

    rtn = utility.compare_string_with_now(batch_start_date, "days")
    if rtn.days < 0:
        logger.info("day<0, exit")
        return "000002"
    else:
        logger.info("day>=0, go on")

    rtn = utility.compare_string_with_now(batch_start_time, "seconds")
    if rtn.days < 0:
        logger.info("time.days<0, exit")
        return "000003"

    if rtn.seconds <= 0:
        logger.info("time.seconds<0, exit")
        return "000004"
    else:
        logger.info("time.seconds>0, go on")
        pass

    ###########################
    # scheduled job start here
    ###########################
    logger.info("Connecting Redis...")
    redis_cli = client.Redis_cli()
    rtn_code=redis_cli.conn_redis()
    if  rtn_code == "000000":
        logger.info("Redis connected...")
    else:
        logger.error("Redis connected Refused...")
        return

    conf = configparser.ConfigParser()
    logger.info("Loading configuration...")
    conf.read(myibs_ini)

    sections = conf.sections()
    for section in sections:
        items = conf.items(section)
        for item in items:
            logger.info("myibs.ini" + ":" + section + ":" + item[0] + "=" + item[1])
            rtn_code = redis_cli.set_redis("myibs.ini" + ":" + section + ":" + item[0], item[1])
            if rtn_code == "999999":
                # 如有问题可以修改为异步通知微信
                pass
            else:
                pass

    logger.info("Configuration loaded.")

    return rtn_code

# 读取参数，每X秒刷新共享内存
def batch_job_004():
    if_batch_start = utility.get_myibs_ini("batch", "batch_job_004_start")
    batch_start_date = utility.get_myibs_ini("batch", "batch_job_004_start_date")
    batch_start_time = utility.get_myibs_ini("batch", "batch_job_004_start_time")
    batch_job_internal_time = utility.get_myibs_ini("batch", "batch_job_004_internal_time")
    batch_job_started = utility.get_myibs_ini("batch", "batch_job_004_status")

    if batch_job_started == "STARTED":
        print("Try to start the TCP server. However server started, quit.")
        logger.info("try to start the TCP server. However server started, quit.")
        return

    log_string = "interval (" + batch_job_internal_time + "s):" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " +\
                 if_batch_start + " " + \
                 batch_start_date + " " + \
                 batch_start_time
    logger.info(log_string)

    if if_batch_start == "True":
        pass
    else:
        return "000001"

    rtn = utility.compare_string_with_now(batch_start_date, "days")
    if rtn.days < 0:
        logger.info("day<0, exit")
        return "000002"
    else:
        logger.info("day>=0, go on")

    rtn = utility.compare_string_with_now(batch_start_time, "seconds")
    if rtn.days < 0:
        logger.info("time.days<0, exit")
        return "000003"

    if rtn.seconds <= 0:
        logger.info("time.seconds<0, exit")
        return "000004"
    else:
        logger.info("time.seconds>0, go on")
        pass


    ###########################
    # scheduled job start here
    ###########################
    conf = configparser.ConfigParser()
    logger.info("Loading configuration...")
    conf.read(myibs_ini)

    rtn_str = None

    import mmap
    import contextlib

    utility.set_myibs_ini("batch", "batch_job_004_status", "STARTED")
    with contextlib.closing(mmap.mmap(-1, 1024*1024, tagname="myibs.ini", access=mmap.ACCESS_WRITE)) as m:
        sections = conf.sections()
        dict_myibs_ini = {}

        dict_sections = {}
        for section in sections:

            items = conf.items(section)
            dict_items = {}
            for item in items:
                in_parm_tagname = "myibs.ini" + ":" + section + ":" + item[0] + "=" + item[1]
                logger.info(in_parm_tagname)
                print(in_parm_tagname)

                dict_items[item[0]] = item[1]
                #print(dict_items)
                dict_sections[section] = dict_items
                #print(dict_sections)

        import json
        obj_json = json.dumps(dict_sections)
        print("dict->json", obj_json)

        try:
            m.seek(0)
            m.write(str(obj_json).encode())
            m.flush()
            rtn_str = "000000"
        except Exception as e:
            rtn_code = None
            logger.error(e)
            print(e)

        logger.info("Configuration loaded.")
        #time.sleep(100000)
        print(obj_json)
        return rtn_str

    return rtn_code
