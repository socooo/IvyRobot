from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^role_mas_tmp_add/$', views.role_mas_tmp_add, name="role_mas_tmp_add"),
    url(r'^role_mas_tmp_lst/$', views.role_mas_tmp_lst, name="role_mas_tmp_lst"),
    url(r'^role_mas_lst2lvl/$', views.role_mas_lst2lvl, name="role_mas_lst2lvl"),
    url(r'^role_mas_dsp/(?P<id>\d+)/$', views.role_mas_dsp, name="role_mas_dsp"),
    url(r'^role_mas_tmp_dsp/(?P<id>\d+)/$', views.role_mas_tmp_dsp, name="role_mas_tmp_dsp"),
    url(r'^role_mas_tmp_amd/(?P<id>\d+)/$', views.role_mas_tmp_amd, name="role_mas_tmp_amd"),
    url(r'^role_mas_tmp_amd2lvl/(?P<id>\d+)/$', views.role_mas_tmp_amd2lvl, name="role_mas_tmp_amd2lvl"),
    url(r'^role_mas_tmp_del/$', views.role_mas_tmp_del, name="role_mas_tmp_del"),
    url(r'^role_mas_tmp_del2lvl/$', views.role_mas_tmp_del2lvl, name="role_mas_tmp_del2lvl"),
    url(r'^role_mas_tmp_app/(?P<id>\d+)/$', views.role_mas_tmp_app, name="role_mas_tmp_app"),

    url(r'^menu_mas_tmp_add/$', views.menu_mas_tmp_add, name="menu_mas_tmp_add"),
    url(r'^menu_mas_tmp_lst/$', views.menu_mas_tmp_lst, name="menu_mas_tmp_lst"),
    url(r'^menu_mas_lst2lvl/$', views.menu_mas_lst2lvl, name="menu_mas_lst2lvl"),
    url(r'^menu_mas_dsp/(?P<id>\d+)/$', views.menu_mas_dsp, name="menu_mas_dsp"),
    url(r'^menu_mas_tmp_dsp/(?P<id>\d+)/$', views.menu_mas_tmp_dsp, name="menu_mas_tmp_dsp"),
    url(r'^menu_mas_tmp_amd/(?P<id>\d+)/$', views.menu_mas_tmp_amd, name="menu_mas_tmp_amd"),
    url(r'^menu_mas_tmp_amd2lvl/(?P<id>\d+)/$', views.menu_mas_tmp_amd2lvl, name="menu_mas_tmp_amd2lvl"),
    url(r'^menu_mas_tmp_del/$', views.menu_mas_tmp_del, name="menu_mas_tmp_del"),
    url(r'^menu_mas_tmp_del2lvl/$', views.menu_mas_tmp_del2lvl, name="menu_mas_tmp_del2lvl"),
    url(r'^menu_mas_tmp_app/(?P<id>\d+)/$', views.menu_mas_tmp_app, name="menu_mas_tmp_app"),

    url(r'^user_role_mas_tmp_add/$', views.user_role_mas_tmp_add, name="user_role_mas_tmp_add"),
    url(r'^user_role_mas_tmp_lst/$', views.user_role_mas_tmp_lst, name="user_role_mas_tmp_lst"),
    url(r'^user_role_mas_lst2lvl/$', views.user_role_mas_lst2lvl, name="user_role_mas_lst2lvl"),
    url(r'^user_role_mas_dsp/(?P<id>\d+)/$', views.user_role_mas_dsp, name="user_role_mas_dsp"),
    url(r'^user_role_mas_tmp_dsp/(?P<id>\d+)/$', views.user_role_mas_tmp_dsp, name="user_role_mas_tmp_dsp"),
    url(r'^user_role_mas_tmp_amd/(?P<id>\d+)/$', views.user_role_mas_tmp_amd, name="user_role_mas_tmp_amd"),
    url(r'^user_role_mas_tmp_amd2lvl/(?P<id>\d+)/$', views.user_role_mas_tmp_amd2lvl, name="user_role_mas_tmp_amd2lvl"),
    url(r'^user_role_mas_tmp_del/$', views.user_role_mas_tmp_del, name="user_role_mas_tmp_del"),
    url(r'^user_role_mas_tmp_del2lvl/$', views.user_role_mas_tmp_del2lvl, name="user_role_mas_tmp_del2lvl"),
    url(r'^user_role_mas_tmp_app/(?P<id>\d+)/$', views.user_role_mas_tmp_app, name="user_role_mas_tmp_app"),

    url(r'^user_mas_tmp_add/$', views.user_mas_tmp_add, name="user_mas_tmp_add"),
    url(r'^user_mas_tmp_lst/$', views.user_mas_tmp_lst, name="user_mas_tmp_lst"),
    url(r'^user_mas_lst2lvl/$', views.user_mas_lst2lvl, name="user_mas_lst2lvl"),
    url(r'^user_mas_dsp/(?P<id>\d+)/$', views.user_mas_dsp, name="user_mas_dsp"),
    url(r'^user_mas_tmp_dsp/(?P<id>\d+)/$', views.user_mas_tmp_dsp, name="user_mas_tmp_dsp"),
    url(r'^user_mas_tmp_amd/(?P<id>\d+)/$', views.user_mas_tmp_amd, name="user_mas_tmp_amd"),
    url(r'^user_mas_tmp_amd2lvl/(?P<id>\d+)/$', views.user_mas_tmp_amd2lvl, name="user_mas_tmp_amd2lvl"),
    url(r'^user_mas_tmp_del/$', views.user_mas_tmp_del, name="user_mas_tmp_del"),
    url(r'^user_mas_tmp_del2lvl/$', views.user_mas_tmp_del2lvl, name="user_mas_tmp_del2lvl"),
    url(r'^user_mas_tmp_app/(?P<id>\d+)/$', views.user_mas_tmp_app, name="user_mas_tmp_app"),

    url(r'^role_mas_dsp_json/(?P<id>\d+)/$', views.role_mas_dsp_json, name="role_mas_dsp_json"),
]

# from apscheduler.scheduler import Scheduler
# import time
# import logging
# logger = logging.getLogger('sourceDns.webdns.views')
# #定时任务
# sched = Scheduler()
# @sched.interval_schedule(seconds=5)
# def my_task1():
#
#     logger.debug("-------------------------- batch job started --------------------------")
#
#     try:
#         import configparser
#     except:
#         from six.moves import configparser
#     config = configparser.ConfigParser()
#     config.read("mysite\myibs.ini")
#     if_batch_start = config.get("batch", "sched_start")
#     batch_start_date = config.get("batch", "sched_start_date")
#     batch_start_time = config.get("batch", "sched_start_time")
#
#     from kernal import utility
#
#     if if_batch_start == "True":
#         pass
#     else:
#         return "000001"
#
#     rtn = utility.compare_string_with_now(batch_start_date, "days")
#     if rtn.days < 0:
#         print("day<=0")
#         return "000002"
#     else:
#         print("day>=0")
#
#     rtn = utility.compare_string_with_now(batch_start_time, "seconds")
#     if rtn.days < 0:
#         print("time<=0")
#         return "000002"
#
#     if rtn.seconds <= 0:
#         return "000003"
#     else:
#         print("time>=0")
#         pass
#
#     log_string = "interval (5s):" + time.strftime('%Y-%m-%d %H:%M:%S',
#             time.localtime(time.time())) + " " + if_batch_start + " " + batch_start_date + " " + batch_start_time
#     print(log_string)
#     logger.debug(log_string)
#
#     logger.infor("--------------------------  batch job ended  --------------------------")
# sched.start()
#
# sched1 = Scheduler()
# @sched1.interval_schedule(seconds=60)
# def my_task2():
#     logger.debug("-------------------------- batch job started --------------------------")
#     print("interval (60s):", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#     logger.debug("interval (60s):" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#     logger.debug("--------------------------  batch job ended  --------------------------")
# sched1.start()