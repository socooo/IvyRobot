import socket
import random
import datetime, time
import logging
import json

from kernal.models import Parm_mas
from kernal import utility

logger = logging.getLogger('sourceDns.webdns.views')

#############################
# 多线程分布式异步处理模型
#############################
# 业务逻辑
def parm_mas_add(key, random_id):
    try:
        parm_mas=Parm_mas()
        #id = models.AutoField("参数序号", primary_key=True, )
        parm_mas.key_grp = random_id
        parm_mas.key = key
        parm_mas.value = key
        parm_mas.key_desc = key
        parm_mas.value_desc = key
        parm_mas.status = "A"
        parm_mas.ver_no = 1
        parm_mas.prod = "parm_mas"
        parm_mas.func = "parm_mas_add"
        parm_mas.maker = ""
        parm_mas.inp_date = datetime.datetime.now()
        parm_mas.checker = ""
        parm_mas.app_date = datetime.datetime.now()
        parm_mas.save()

        msg_head = {}
        msg_head['service_code'] = 'parm_mas'
        msg_head['tx_code'] = 'parm_mas_add'
        msg_head['msg_code'] = 'parm_mas_add_JSON_01'
        msg_head['tx_mode'] = '02'          #00 正交易  01 冲正交易 02 回复报文
        msg_head['inter_consumer_code'] = 'client_xxx'
        msg_head['original_consumer_code'] = 'app_client_xxx'
        msg_head['institution_id'] = 'FI0123456789'
        msg_head['consumer_sys_date'] = ''
        msg_head['req_tx_timestampe'] = '2018-11-11 11:11:11'
        msg_head['user_id'] = 'USR0123456789'
        msg_head['is_sftp_req'] = '0'       #0 联机报文  1 FTP报文
        msg_head['sftp_req_path'] = '/usr/myibs/ftp/app_client_xxx/out'
        msg_head['rsp_code'] = '000000'
        msg_head['rsp_msg'] = 'OK'
        msg_head['rsp_tx_timestampe'] = str(datetime.datetime.now())

        msg_app_head = {}
        msg_app_head['req_seq_no'] = 'id201801010000000001'
        msg_app_head['record_no_this_page'] = '1'
        msg_app_head['total_record'] = '1'
        msg_app_head['page_no'] = '1'
        msg_app_head['total_page_no'] = '1'
        msg_app_head['page_up_or_down'] = '0'   # 0 不翻页 1 上翻  2 下翻

        msg_body = {}
        msg_body_rcd = {}

        for num in range(1, 3):
            msg_body_rcd['id'] = parm_mas.id
            msg_body_rcd['key_grp'] = parm_mas.key_grp
            msg_body_rcd['key'] = parm_mas.key
            msg_body_rcd['value'] = parm_mas.value
            msg_body_rcd['value_desc'] = parm_mas.value_desc
            msg_body_rcd['inp_date'] = str(parm_mas.inp_date)
            msg_body_rcd['app_date'] = str(parm_mas.app_date)
            msg_body['msg_body_rcd_' + str(num)] = msg_body_rcd

        msg_rsp = {}
        msg_rsp['msg_head'] = msg_head
        msg_rsp['msg_app_head'] = msg_app_head
        msg_rsp['msg_body'] = msg_body

        obj_json = json.dumps(msg_rsp)

        return obj_json
    except Exception as e:
        logger.error("post method error code:")
        logger.error(e)

        return "999999"
    finally:
        pass


#交易登记服务端S，实时回复收妥
def tcpServer():

    port = int(utility.get_myibs_ini("asyn_TCP_server_001", "port"))
    timeout = int(utility.get_myibs_ini("asyn_TCP_server_001", "timeout"))
    msg_length = int(utility.get_myibs_ini("asyn_TCP_server_001", "msg_length"))
    con_connection = int(utility.get_myibs_ini("asyn_TCP_server_001", "con_connection"))

    rtn_code = "999999"

    try:
        s = socket.socket()
        host = socket.gethostname()
        s.bind((host, port))
        s.listen(con_connection)
        print('Listening')
        logger.debug('Listening: ' + str(port))

        while True:
            c, addr = s.accept()
            c.settimeout(timeout)
            # print('Got connection from', addr)
            logger.debug('Got connection from: ' + str(addr))

            req = c.recv(msg_length).decode()
            print('Message received: %s' % req)
            logger.info('Message received: ' + str(req))

            # if req == ":shutdown":
            #     c.send(":shuttingdown_down".encode())
            #     c.close()
            #     logger.debug("server shut down.")
            #     break

            rep = parm_mas_add(req, random.randint(1, 10))
            print("response message: " + str(rep))
            logger.info('response message: ' + str(rep))

            c.send(rep.encode())
            # print("response message sent: ")
            logger.debug("response message sent: ")

            rtn_code = "000000"

    except Exception as e:
        logger.error("post method error code:" + str(rtn_code))
        logger.error(e)

        rtn_code = "999999"
    finally:
        c.close()
        print("server connection closed")
        logger.info("server connection closed")

    return rtn_code

def tcpClient(msg):

    server = utility.get_myibs_ini("asyn_TCP_client_001", "server")
    port = int(utility.get_myibs_ini("asyn_TCP_client_001", "port"))
    timeout = int(utility.get_myibs_ini("asyn_TCP_client_001", "timeout"))
    msg_length = int(utility.get_myibs_ini("asyn_TCP_client_001", "msg_length"))
    sleep_time = float(utility.get_myibs_ini("asyn_TCP_client_001", "sleep_time"))
    float_msg = 1

    print(msg)

    try:
        while True:
            print('Ready to create socket')
            s = socket.socket()
            print('Connecting')
            s.connect((server, port))
            print('Connected')
            s.settimeout(timeout)

            float_msg = float_msg+0.000001
            req = str(float_msg)

            # if req ==':exit':
            #     s.close()
            #     break

            s.send(req.encode())
            print('Waiting for the message from server...')

            rep = s.recv(msg_length).decode()
            print('Message received: %s' % rep)

            time.sleep(sleep_time)

    except Exception as e:
        print(e)
    finally:
        s.close()

