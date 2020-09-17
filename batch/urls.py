from django.conf.urls import url
from . import views
from kernal import utility

#留给Batch手工启动/停止/排序及job清单查看使用
urlpatterns = [
    #url(r'^user_mas_tmp_app/(?P<id>\d+)/$', views.user_mas_tmp_app, name="user_mas_tmp_app"),
]

from apscheduler.scheduler import Scheduler
import time
import logging
logger = logging.getLogger('sourceDns.webdns.views')

# 定时任务，采用 apscheduler
# 最好使用django-crontab, 可是不支持Windows有啥办法呢？
sched = Scheduler()
batch_job_001_internal_time = utility.get_myibs_ini("batch", "batch_job_001_internal_time")
@sched.interval_schedule(seconds=int(batch_job_001_internal_time))
def batch_job_001():

    logger.info("-------------------------- batch job started --------------------------")

    views.batch_job_001()

    logger.info("--------------------------  batch job ended  --------------------------")
sched.start()

sched1 = Scheduler()
batch_job_002_internal_time = utility.get_myibs_ini("batch", "batch_job_002_internal_time")
@sched.interval_schedule(seconds=int(batch_job_002_internal_time))
def batch_job_002():

    logger.info("-------------------------- batch job started --------------------------")

    views.batch_job_002()

    logger.info("--------------------------  batch job ended  --------------------------")
sched1.start()

#Redis 后台服务器刷新
sched003 = Scheduler()
batch_job_003_internal_time = utility.get_myibs_ini("batch", "batch_job_003_internal_time")
@sched.interval_schedule(seconds=int(batch_job_003_internal_time))
def batch_job_003():

    logger.info("-------------------------- batch job started --------------------------")

    views.batch_job_003()

    logger.info("--------------------------  batch job ended  --------------------------")
sched003.start()


#共享内存服务器
sched004 = Scheduler()
batch_job_004_internal_time = utility.get_myibs_ini("batch", "batch_job_004_internal_time")
@sched.interval_schedule(seconds=int(batch_job_004_internal_time))
def batch_job_004():

    logger.info("-------------------------- batch job started --------------------------")

    views.batch_job_004()

    logger.info("--------------------------  batch job ended  --------------------------")
sched004.start()