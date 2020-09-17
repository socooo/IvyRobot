from django.shortcuts import render
import logging
from cif.models import Cif_mas, Cif_mas_tmp, Cif_log
from django.http import HttpResponse
import json

logger = logging.getLogger('sourceDns.webdns.views')
rtn_code = "999999"

def cifmas_lst_inq(request):

    logger.info("-------------------------- started --------------------------")

    rsp_dict = {}

    if request.method == 'GET':
        try:
            logger.info("get method start")

            cifmas_lst = Cif_mas.objects.filter(status="A")

            str_json = "["
            for cifmas in cifmas_lst:
                cifmas_json = cifmas.toJSON()
                print(cifmas_json)
                str_json = str_json + cifmas_json + ","

            str_json = str_json + "]"
            print(str_json)

            logger.info("get method end")
        except Exception as e:
            rtn_code = "010101"
            logger.error("post method:%s", rtn_code)
            logger.error(e)
        finally:
            return HttpResponse(rsp_dict)

    elif request.method == "POST":
        logger.info("post method start")

        logger.info("post method end")
        pass

    logger.info("-------------------------- ended --------------------------")