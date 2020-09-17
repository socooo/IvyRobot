import traceback, datetime, logging, sys
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from kernal.models import Role_mas, Role_mas_tmp, Role_log
from kernal.models import User_role_mas, User_role_mas_tmp, User_role_log
from kernal.models import Menu_mas, Menu_mas_tmp, Menu_log
from django.forms.models import model_to_dict


from django.contrib.auth.models import User

logger = logging.getLogger('sourceDns.webdns.views')

def gv_menu(request):

    logger.info("-------------------------- gv_menu started, username=%s --------------------------", request.user.username)

    print(request.session.get('key'))
    # 在此处先获取session中的信息, 如果沒有登录就跳过，防止因攻击消耗I/O
    if request.user.id == None:
        return {
                }

    # 如果已登录且获取过菜单，就直接从session中获取
    if request.session.get('gs_is_gs_menu_set', None) == 'True':
        auth_role_mas_dict_list = request.session['gs_auth_role_mas_dict_list']
        auth_role_mas_dict_list_lvl3 = request.session['gs_auth_role_mas_dict_list_lvl3']
    # 如果已登录但未获取过菜单，就直接从数据库中获取
    else:
        user_role_mas = User_role_mas.objects.get(user=request.user.id, status='A')
        role_mas = Role_mas.objects.get(id=user_role_mas.role.id)
        auth_role_mas_lst = Role_mas.objects.filter(role_name=role_mas.role_name, status='A').values_list('menu')

        menu_mas_list = Menu_mas.objects.filter(id__in=auth_role_mas_lst, status='A')

        auth_role_mas_dict_list = []
        for menu_mas in menu_mas_list:
            auth_role_mas_dict = {}
            auth_role_mas_dict['id'] = menu_mas.id
            auth_role_mas_dict['menu_parent_id'] = menu_mas.menu_parent_id
            auth_role_mas_dict['menu_name'] = menu_mas.menu_name
            auth_role_mas_dict['status'] = menu_mas.status
            auth_role_mas_dict['menu_lvl'] = menu_mas.menu_lvl
            auth_role_mas_dict['menu_long_desc'] = menu_mas.menu_long_desc
            auth_role_mas_dict['menu_sht_desc'] = menu_mas.menu_sht_desc
            auth_role_mas_dict_list.append(auth_role_mas_dict)

        auth_role_mas_dict_list_lvl3 = auth_role_mas_dict_list

        request.session['gs_is_gs_menu_set'] = 'True'
        request.session['gs_auth_role_mas_dict_list'] = auth_role_mas_dict_list
        request.session['gs_auth_role_mas_dict_list_lvl3'] = auth_role_mas_dict_list_lvl3

    logger.info("-------------------------- gv_menu ended --------------------------")

    return {
            'gs_auth_role_mas_dict_list': auth_role_mas_dict_list,
            'gs_auth_role_mas_dict_list_lvl3': auth_role_mas_dict_list_lvl3,
            }

    logger.info("-------------------------- ended --------------------------")

