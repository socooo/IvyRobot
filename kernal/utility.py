import datetime
import time

import mmap
import contextlib

import redis

from kernal import utility

import logging
logger = logging.getLogger('sourceDns.webdns.views')

myibs_ini="mysite\myibs.ini"

# 比较送入字符类型和现在时间的区别
# 返回大于零则代表现在时间大于参数s
def compare_string_with_now(in_date, in_format):

    if in_format == "days":
        in_format = "%Y-%m-%d"
    elif in_format == "seconds":
        in_format = "%H:%M:%S"
    else:
        return

    in_date = datetime.datetime.strptime(in_date, in_format)
    now = datetime.datetime.strptime(time.strftime(in_format, time.localtime()), in_format)
    delta = now - in_date
    # print(in_date, in_format)
    # print("delta.days", delta.days)
    # print("delta.seconds", delta.seconds)

    return delta


# 读取myibs.ini中的参数
def get_myibs_ini(in_section, in_parm):
    try:
        import configparser
    except:
        from six.moves import configparser

    config = configparser.ConfigParser()
    config.read(myibs_ini)

    try:
        rtn_msg = config.get(in_section, in_parm)
    except Exception:
        rtn_msg = "999999"

    return rtn_msg

# 读取myibs.ini中的参数
def set_myibs_ini(in_section, in_parm, in_value):
    try:
        import configparser
    except:
        from six.moves import configparser

    config = configparser.ConfigParser()
    config.read(myibs_ini)

    try:
        rtn_msg = config.set(in_section, in_parm, in_value)
        config.write(open(myibs_ini, "w"))
    except Exception:
        rtn_msg = "999999"

    return rtn_msg

#手动写入共享内存（单条）
def set_mmap(in_parm_tagname, value):
    rtn_str = None
    try:
        with contextlib.closing(mmap.mmap(-1, 1024, tagname=in_parm_tagname, access=mmap.ACCESS_WRITE)) as m:
            for i in range(1, 2):
                m.seek(0)
                print(i)
                #m.write((str(in_parm_tagname).encode()))
                m.write(str(in_parm_tagname).encode())
                m.flush()
            rtn_str = "000000"
    except Exception:
        rtn_str = None
    finally:
        return rtn_str

#手动写入共享内存（单条）
def get_mmap(in_parm_tagname):
    rtn_str = None
    try:
        with contextlib.closing(mmap.mmap(-1, 1024, tagname=in_parm_tagname, access=mmap.ACCESS_READ)) as m:
            m.seek(0)
            rtn_str = m.read(1024).decode().replace('\x00', '')
            print(rtn_str)
    except Exception:
        rtn_str = None
    finally:
        return rtn_str

# redis
# 以下程序废弃，转移至client.py
class Redis_cli():
    str_return = "999999"

    def __init__(self):
        self.host = utility.get_myibs_ini("redis1", "hostname")
        self.port = int(utility.get_myibs_ini("redis1", "port"))
        self.db = int(utility.get_myibs_ini("redis1", "db"))
        self.password = utility.get_myibs_ini("redis1", "password")
        self.sleeptime_before_retry = int(utility.get_myibs_ini("redis1", "sleeptime_before_retry"))

        self.conn_redis()

    #连接服务器
    def conn_redis(self):
        self.str_return = "999999"
        try:
            rdp = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
            self.r = redis.StrictRedis(connection_pool=rdp)
            self.r.get("test")
            return "000000"
        except Exception as e:
            self.str_return = "002001"

            logger.error("connect redis1 error code, trying redis2:", self.str_return)
            logger.error(e)

            #软负载切换
            self.host = utility.get_myibs_ini("redis2", "hostname")
            self.port = int(utility.get_myibs_ini("redis2", "port"))
            self.db = int(utility.get_myibs_ini("redis2", "db"))
            self.password = utility.get_myibs_ini("redis2", "password")
            self.sleeptime_before_retry = int(utility.get_myibs_ini("redis2", "sleeptime_before_retry"))

            try:
                rdp = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
                self.r = redis.StrictRedis(connection_pool=rdp)
                return "000000"
            except Exception as e:
                logger.error("connect redis1 error code:", self.str_return)
                logger.error(e)

                return "000204"

    #写redis服务器
    def set_redis(self, key, content):
        self.str_return = "999999"
        try:
            self.r.set(key, content)
            self.str_return = "000000"
            return self.str_return
        except Exception as e:
            logger.error("set redis error code:", self.str_return)
            logger.error(e)

            try:
                #一次重新的机会
                time.sleep(self.sleeptime_before_retry)
                self.conn_redis()
                self.r.set(key, content)

                self.str_return = "000000"
                return self.str_return
            except Exception as e:
                self.str_return = "000202"

                logger.error("set redis error code:", self.str_return)
                logger.error(e)

                return self.str_return

    #读redis服务器
    def get_redis(self, key):
        self.str_return = "999999"
        try:
            self.str_return = self.r.get(key)
            return self.str_return
        except Exception as e:
            logger.error("set redis error code:", self.str_return)
            logger.error(e)

            try:
                time.sleep(self.sleeptime_before_retrys)
                self.conn_redis()
                self.str_return = self.r.get(key)
                return self.str_return
            except Exception as e:
                self.str_return = "000203"

                logger.error("set redis error code:", self.str_return)
                logger.error(e)

                return self.str_return

