import paramiko
from kernal import utility
import logging
import smtplib
from email.mime.text import MIMEText

from kernal import utility
import time
import redis

logger = logging.getLogger('sourceDns.webdns.views')
rtn_dict = {"rtn_code": "999999", "rsp_msg": None}

class sftp_client():

    # def __init__(self):
    #     rtn_dict["rtn_code"] = "999999"
    #     rtn_dict["rsp_msg"] = None

    def sftp_read(self, commands):

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            host = utility.get_myibs_ini("ftp_server1", "host")
            port = int(utility.get_myibs_ini("ftp_server1", "port"))
            username = utility.get_myibs_ini("ftp_server1", "username")
            password = utility.get_myibs_ini("ftp_server1", "password")

            for command in commands:
                ssh.connect(hostname=host, port=port, username=username, password=password)
                stdin, stdout, stderr = ssh.exec_command(command)
                res, err = stdout.read(), stderr.read()
                result = res if res else err
                rtn_str = str(result.decode())
                print(rtn_str)

            rtn_dict["rtn_code"] = "000000"
            rtn_dict["rsp_msg"] = rtn_str

        except Exception as e:
            rtn_dict["rtn_code"] = "000301"
            rtn_dict["rsp_msg"] = None

            logger.error("sftp_read error code:", rtn_dict["rtn_code"])
            logger.error(e)

        finally:
            ssh.close()

        return rtn_dict


    def sftp_get(self, source, target):
        try:
            host = utility.get_myibs_ini("ftp_server1", "host")
            port = int(utility.get_myibs_ini("ftp_server1", "port"))
            username = utility.get_myibs_ini("ftp_server1", "username")
            password = utility.get_myibs_ini("ftp_server1", "password")

            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(source, target)

            rtn_dict["rtn_code"] = "000000"
            rtn_dict["rsp_msg"] = None

        except Exception as e:
            rtn_dict["rtn_code"] = "000302"
            rtn_dict["rsp_msg"] = None

            logger.error("sftp_read error code:", rtn_dict["rtn_code"])
            logger.error(e)

        finally:
            transport.close()

        return rtn_dict

    def sftp_put(self, source, target):
        try:
            host = utility.get_myibs_ini("ftp_server1", "host")
            port = int(utility.get_myibs_ini("ftp_server1", "port"))
            username = utility.get_myibs_ini("ftp_server1", "username")
            password = utility.get_myibs_ini("ftp_server1", "password")

            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(source, target)

            rtn_dict["rtn_code"] = "000000"
            rtn_dict["rsp_msg"] = None
        except Exception as e:
            rtn_dict["rtn_code"] = "000303"
            rtn_dict["rsp_msg"] = None

            logger.error("sftp_read error code:", rtn_dict["rtn_code"])
            logger.error(e)
            return None
        finally:
            transport.close()

        return rtn_dict

class sftp_client():

    def smtp_send(self, in_parm_dict):

        to_user = in_parm_dict["to_user"]
        msg_subject = in_parm_dict["msg_subject"]
        msg_body = in_parm_dict["msg_subject"]

        smtp_server = utility.get_myibs_ini("smtp_service", "smtp_server")
        smtp_server_port = utility.get_myibs_ini("smtp_service", "smtp_server_port")
        _user = utility.get_myibs_ini("smtp_service", "from_user")
        _pwd = utility.get_myibs_ini("smtp_service", "passcode")
        _to = to_user

        msg = MIMEText(msg_body)
        msg["Subject"] = msg_subject
        msg["From"] = _user
        msg["To"] = _to

        try:
            print("connecting SMTP server: %s:%s" % (smtp_server, smtp_server_port))
            s = smtplib.SMTP_SSL(smtp_server, int(smtp_server_port))

            print("login...")
            s.login(_user, _pwd)

            print("sending message")
            s.sendmail(_user, _to, msg.as_string())
            s.quit()

            print("message sent successfully!")

            return "000000"
        except smtplib.SMTPException as e:
            print("message sent falied,%s" % e)

            return None

# redis
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
            self.str_retu = "002001"

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
            print(self.str_return)
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

from interface import client
if __name__ == '__main__':

    # in_parm_dict = {}
    # in_parm_dict['to_user'] = "snetlogon20@sina.com"
    # in_parm_dict['msg_subject'] = "subject@sina.com"
    # in_parm_dict['msg_body'] = "this is a message to you."
    #
    # sftp_client = client.sftp_client()
    # sftp_client.smtp_send(in_parm_dict)

    redis_cli = client.Redis_cli()
    redis_cli.conn_redis()
    redis_cli.get_redis("a")

