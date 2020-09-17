from django import forms
from .models import Parm_mas
from .models import Role_mas, Role_mas_tmp, Role_log
from .models import Menu_mas, Menu_mas_tmp, Menu_log
from .models import User_role_mas, User_role_mas_tmp
from .models import User_mas, User_mas_tmp
from django.forms import ValidationError
from django.contrib.admin import widgets
import logging
from django.contrib.auth.models import User

STATUS = (
    ('A', '正常'),
    ('D', '关闭'),
    ('S', '挂起'),
)

MENU_LVL     = (
    ('1', '一级菜单'),
    ('2', '二级菜单'),
    ('3', '三级菜单'),
)

logger = logging.getLogger('sourceDns.webdns.views')

#class Parm_mas_form()(forms.ModelForm):

class Role_mas_form(forms.ModelForm):
    role_name = forms.CharField(
                            required=True,
                            label="角色",
                            min_length=1,
                            max_length=20,
                            error_messages={
                                'required': '此字段为必输项',
                                'min_length': "此字段至少需输入至少1位",
                                'max_length': "此字段不可超过20位"
                            }
                          )
    role_desc = forms.CharField(
                            required=True,
                            label="角色描述",
                            min_length=1,
                            max_length=20,
                            error_messages={
                                'required': '此字段为必输项',
                                'min_length': "此字段至少需输入至少1位",
                                'max_length': "此字段不可超过20位"
                            }
                          )
    status = forms.ChoiceField(
                            required=True,
                            choices=STATUS,
                            label="角色状态",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    ver_no = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )
    func = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )
    prod = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )
    maker = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )
    checker = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )
    inp_date = forms.CharField(
                            required=True,
                            widget=forms.TextInput(attrs={'readonly': 'readonly'})
                          )

    class Meta:
        model = Role_mas
        fields = ("id", "role_name", "role_desc", "email", "handphone", "status", "func")
        # fields='__all__'
        
    def clean(self):
        cleaned_data = super(Role_mas_form, self).clean()

        var_role_name = cleaned_data.get("role_name")
        var_func = cleaned_data.get("func")
        cleaned_data

        #####################
        # 检查重复记录
        #####################
        if var_func == "role_mas_tmp_add":
            role_mas_lst = Role_mas.objects.filter(role_name=var_role_name)
            if role_mas_lst.count()>=1:
                raise ValidationError("该角色已在主表中存在，请仔细检查。")

        return cleaned_data


class Role_mas_role_name_form(forms.ModelForm):
    role_name = forms.CharField(
        required=True,
        label="角色名称",
        min_length=1,
        max_length=20,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过20位"
        }
    )


    class Meta:
        model = Role_mas
        fields = ("role_name", )
        # fields='__all__'

    def clean(self):
        cleaned_data = super(Role_mas_role_name_form, self).clean()

        var_role_name = cleaned_data.get("role_name")
        cleaned_data

        return cleaned_data
    
    
class Role_mas_tmp_form(forms.ModelForm):
    role_name = forms.CharField(
                            required=True,
                            label="角色名称",
                            min_length=1,
                            max_length=20,
                            error_messages={
                                'required': '此字段为必输项',
                                'min_length': "此字段至少需输入至少1位",
                                'max_length': "此字段不可超过20位"
                            }
                          )
    role_desc = forms.CharField(
                            required=True,
                            label="角色描述",
                            min_length=1,
                            max_length=20,
                            error_messages={
                                'required': '此字段为必输项',
                                'min_length': "此字段至少需输入至少1位",
                                'max_length': "此字段不可超过20位"
                            }
                          )
    status = forms.ChoiceField(
                            required=True,
                            choices=STATUS,
                            label="角色状态",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )

    class Meta:
        model = Role_mas_tmp
        fields = ("id", "role_name", "role_desc", "email", "handphone", "status", "func")
        #fields = '__all__'

    def clean(self):
        cleaned_data = super(Role_mas_tmp_form, self).clean()

        logger.info("validation start")

        var_role_name = cleaned_data.get("role_name")
        var_func = cleaned_data.get("func")

        #####################
        # 检查重复记录
        #####################
        # if var_func == "role_mas_tmp_add":
        role_mas_lst = Role_mas_tmp.objects.filter(role_name=var_role_name)
        if role_mas_lst.count() >= 1:
            raise ValidationError("该角色已在临时档中存在，不可重复新建，请仔细检查。")

        logger.info("validation end")

        return cleaned_data


class Menu_mas_form(forms.ModelForm):
    menu_lvl = forms.ChoiceField(
                            required=True,
                            choices=MENU_LVL,
                            label="菜单级别",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    menu_name = forms.CharField(
        required=True,
        label="菜单名称",
        min_length=1,
        max_length=20,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过20位"
        }
    )
    menu_parent_id = forms.IntegerField(
        required=True,
        label="父菜单ID",
        error_messages={
            'required': '此字段为必输项',
            'invalid': "请输入数字 "
        }
    )
    menu_name = forms.CharField(
        required=True,
        label="菜单名称",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    menu_sht_desc = forms.CharField(
        required=True,
        label="菜单图标",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    menu_long_desc = forms.CharField(
        required=True,
        label="菜单URL",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="菜单状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )
    # ver_no = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    # func = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    # prod = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    # maker = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    # checker = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    # inp_date = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )

    class Meta:
        model = Menu_mas
        fields = ("menu_lvl", "menu_parent_id", "menu_name", "menu_sht_desc", "menu_long_desc", "status", "func")
        #fields = ("id", "role_name", "role_desc", "email", "handphone", "status", "func")
        #fields='__all__'

    def clean(self):
        cleaned_data = super(Menu_mas_form, self).clean()

        var_menu_name = cleaned_data.get("menu_name")
        var_func = cleaned_data.get("func")
        cleaned_data

        #####################
        # 检查重复记录
        #####################
        if var_func == "menu_mas_tmp_add":
            menu_mas_lst = Role_mas.objects.filter(menu_name=var_menu_name)
            if menu_mas_lst.count() >= 1:
                raise ValidationError("该菜单已在主表中存在，请仔细检查。")

        return cleaned_data

class Menu_mas_tmp_form(forms.ModelForm):
    # role_id = forms.IntegerField(
    #     required=True,
    #     label="角色ID",
    #     error_messages={
    #         'required': '此字段为必输项',
    #         'invalid': "请输入数字 "
    #     }
    # )s
    menu_lvl = forms.ChoiceField(
                            required=True,
                            choices=MENU_LVL,
                            label="菜单级别",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    menu_name = forms.CharField(
        required=True,
        label="菜单名称",
        min_length=1,
        max_length=20,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过20位"
        }
    )
    menu_parent_id = forms.IntegerField(
        required=True,
        label="父菜单ID",
        error_messages={
            'required': '此字段为必输项',
            'invalid': "请输入数字 "
        }
    )
    menu_name = forms.CharField(
        required=True,
        label="菜单名称",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    menu_sht_desc = forms.CharField(
        required=True,
        label="菜单图标",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    menu_long_desc = forms.CharField(
        required=True,
        label="菜单URL",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="菜单状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )

    class Meta:
        model = Menu_mas_tmp
        fields = ("menu_lvl", "menu_parent_id", "menu_name", "menu_sht_desc", "menu_long_desc", "status", "func")
        #fields = '__all__'
        #exclude = ('ver_no', 'prod', 'func', 'maker', 'inp_date', 'checker', 'app_date')

    def clean(self):
        cleaned_data = super(Menu_mas_tmp_form, self).clean()

        logger.info("validation start")

        var_role_id = cleaned_data.get("role_id")
        var_menu_name = cleaned_data.get("menu_name")
        var_func = cleaned_data.get("func")

        logger.info("validation end")

        return cleaned_data

class User_role_mas_form(forms.ModelForm):
    user_role_name = forms.CharField(
        required=True,
        label="用户与角色关系",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="菜单状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )

    class Meta:
        model = User_role_mas
        fields = ("user_role_name", "status", "func")
        #fields='__all__'

    def clean(self):
        cleaned_data = super(User_role_mas_form, self).clean()

        # var_menu_name = cleaned_data.get("menu_name")
        # var_func = cleaned_data.get("func")
        cleaned_data

        #####################
        # 检查重复记录
        #####################
        # if var_func == "menu_mas_tmp_add":
        #     menu_mas_lst = Role_mas.objects.filter(menu_name=var_menu_name)
        #     if menu_mas_lst.count() >= 1:
        #         raise ValidationError("该菜单已在主表中存在，请仔细检查。")

        return cleaned_data

class User_role_mas_tmp_form(forms.ModelForm):
    user_role_name = forms.CharField(
        required=True,
        label="用户与角色关系",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="菜单状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )
    class Meta:
        model = User_role_mas_tmp
        fields = ("user_role_name", "status", "func")
        #fields = '__all__'

    def clean(self):
        cleaned_data = super(User_role_mas_tmp_form, self).clean()

        logger.info("validation start")

        # var_user_role_name = cleaned_data.get("user_role_name")
        # var_status = cleaned_data.get("status")
        # logger.info("--------", var_user_role_name, "--------" )
        # logger.info(var_status)

        logger.info("validation end")

        return cleaned_data

class User_mas_form(forms.ModelForm):
    employee_id = forms.CharField(
        required=True,
        label="工号",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    name = forms.CharField(
        required=True,
        label="姓名",
        min_length=1,
        max_length=120,
        error_messages={
            'required': '此字段为必输项',
            'miength': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过120位"
        }
    )
    address = forms.CharField(
        required=False,
        label="地址",
        min_length=1,
        max_length=120,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过120位"
        }
    )
    address = forms.CharField(required=False,
                          label="地址",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项',
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                            }
    )
    age = forms.IntegerField(required=False,
                          label="年龄",
                          error_messages={
                              'required': '此字段为必输项',
                              'invalid': "请输入数字 "
                          }
    )
    phone = forms.CharField(
        required=True,
        label="直线电话",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    mobile_phone = forms.CharField(
        required=True,
        label="移动电话",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="菜单状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )

    class Meta:
        model = User_mas
        fields = ("on_board_date", "employee_id", "name", "address", "age", "phone", "mobile_phone", "status", "func")
        #fields='__all__'

    def clean(self):
        cleaned_data = super(User_mas_form, self).clean()

        # var_menu_name = cleaned_data.get("menu_name")
        # var_func = cleaned_data.get("func")
        cleaned_data

        #####################
        # 检查重复记录
        #####################
        # if var_func == "menu_mas_tmp_add":
        #     menu_mas_lst = Role_mas.objects.filter(menu_name=var_menu_name)
        #     if menu_mas_lst.count() >= 1:
        #         raise ValidationError("该菜单已在主表中存在，请仔细检查。")

        return cleaned_data

class User_mas_tmp_form(forms.ModelForm):
    employee_id = forms.CharField(
        required=True,
        label="工号",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    name = forms.CharField(
        required=True,
        label="姓名",
        min_length=1,
        max_length=120,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过120位"
        }
    )
    on_board_date = forms.DateField(widget=widgets.AdminDateWidget(), label="报到日期")
    address = forms.CharField(
        required=False,
        label="地址",
        min_length=1,
        max_length=120,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过120位"
        }
    )
    address = forms.CharField(required=False,
                          label="地址",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项',
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                            }
    )
    age = forms.IntegerField(required=False,
                          label="年龄",
                          error_messages={
                              'required': '此字段为必输项',
                              'invalid': "请输入数字 "
                          }
    )
    phone = forms.CharField(
        required=True,
        label="直线电话",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    mobile_phone = forms.CharField(
        required=True,
        label="移动电话",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )
    status = forms.ChoiceField(
        required=True,
        choices=STATUS,
        label="状态",
        error_messages={
            'required': '此字段为必输项'
        }
    )
    class Meta:
        model = User_mas_tmp
        fields = ("id", "on_board_date", "employee_id", "name", "address", "age", "phone", "mobile_phone", "status", "func")
        #fields = '__all__'

    def clean(self):
        cleaned_data = super(User_mas_tmp_form, self).clean()

        logger.info("validation start")

        # var_user_role_name = cleaned_data.get("user_role_name")
        # var_status = cleaned_data.get("status")
        # logger.info("--------", var_user_role_name, "--------" )
        # logger.info(var_status)

        logger.info("validation end")

        return cleaned_data

class UserForm(forms.ModelForm):

    username = forms.CharField(
        required=True,
        label="用户名",
        min_length=1,
        max_length=100,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过100位"
        }
    )

    password = forms.CharField(
        required=True,
        label="密码",
        min_length=1,
        max_length=8,
        error_messages={
            'required': '此字段为必输项',
            'min_length': "此字段至少需输入至少1位",
            'max_length': "此字段不可超过8位"
        },
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "password", )


