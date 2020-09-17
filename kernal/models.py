from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import json

# Create your models here.
class Parm_mas(models.Model):
    id = models.AutoField("参数序号", primary_key=True, )
    key_grp = models.CharField("参数键值组", max_length=20, default='system')
    key = models.CharField("参数键值", max_length=20, default='system')
    value = models.CharField("参数内容", max_length=100)
    key_desc = models.CharField("参数键值描述", max_length=100)
    value_desc = models.CharField("参数内描述", max_length=100)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Role_mas", max_length=20)
    func = models.CharField("功能名称", default="Role_mas_add", max_length=20)
    maker = models.CharField("经办员", default="Role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("key_grp", "key",)
        unique_together = (('id',),)
        index_together = (('key_grp', 'key',), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.role_name

class Menu_mas(models.Model):
    id = models.AutoField("菜单序号", primary_key=True)
    #role_id = models.ForeignKey(Role_mas, related_name='role_menu_mas_id', default=1, blank=True)  # 此项为参考外键的字段名称
    menu_lvl = models.CharField("菜单级别", default=1, max_length=20)
    menu_order = models.IntegerField("菜单显示顺序", default=0)
    menu_parent_id = models.IntegerField("父菜单id", default=0)
    menu_name = models.CharField("菜单名称", max_length=100)
    menu_sht_desc = models.CharField("菜单图标", max_length=100, blank=True)
    menu_long_desc = models.CharField("菜单URL", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Menu_mas", max_length=20)
    func = models.CharField("功能名称", default="Menu_mas_add", max_length=20)
    maker = models.CharField("经办员", default="Menu_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        #ordering = ("role_id", "menu_lvl", "menu_parent_id", "menu_name", )
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('menu_lvl', 'menu_parent_id', 'menu_name', ), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.menu_name

    def get_absolute_url_dsp(self):
        return reverse("kernal:menu_mas_dsp", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:menu_mas_tmp_amd2lvl", args=[self.id])


    def toJSON(self):

        def datetime_handler(x):
            if isinstance(x, datetime.datetime):
                return x.isoformat()
            raise TypeError("Unknown type")

        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)

        return json.dumps(d, default=datetime_handler)


class Menu_mas_tmp(models.Model):
    id = models.AutoField("菜单序号", primary_key=True)
    #role_id = models.ForeignKey(Role_mas, related_name='role_menu_mas_tmp_id', default=1, blank=True)  # 此项为参考外键的字段名称
    menu_lvl = models.CharField("菜单级别", default=1, max_length=20)
    menu_order = models.IntegerField("菜单显示顺序", default=0)
    menu_parent_id = models.IntegerField("父菜单ID", default=0)
    menu_name = models.CharField("菜单名称", max_length=100)
    menu_sht_desc = models.CharField("菜单图标", max_length=100, blank=True)
    menu_long_desc = models.CharField("菜单URL", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10, default="A") # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1, blank=True)
    prod = models.CharField("产品名称", default="Menu_mas", max_length=20, blank=True)
    func = models.CharField("功能名称", default="Menu_mas_add", max_length=20, blank=True)
    maker = models.CharField("经办员", default="Menu_mas", max_length=20, blank=True)
    inp_date = models.DateTimeField("创建日期", default=timezone.now, blank=True)
    checker = models.CharField("复核员", default="---", max_length=20, blank=True)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        #ordering = ("role_id", "menu_lvl", "menu_parent_id", "menu_name", )
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('menu_lvl', 'menu_parent_id', 'menu_name', ), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

    def get_absolute_url_dsp(self):
        return reverse("kernal:menu_mas_tmp_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:menu_mas_tmp_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:menu_mas_tmp_amd2lvl", args=[self.id])

class Menu_log(models.Model):
    tx_date = models.DateTimeField("交易日期", default=timezone.now)
    # role_id = models.ForeignKey(Role_mas, related_name='role_log_id')  # 此项为参考外键的字段名称
    menu_lvl = models.CharField("菜单级别", max_length=20)
    menu_order = models.IntegerField("菜单显示顺序", default=0)
    menu_parent_id = models.CharField("父菜单ID", default=0, max_length=20)
    menu_name = models.CharField("菜单名称", max_length=100)
    menu_sht_desc = models.CharField("菜单图标", max_length=100, blank=True)
    menu_long_desc = models.CharField("菜单URL", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Menu_mas", max_length=20)
    func = models.CharField("功能名称", default="Menu_mas_add", max_length=20)
    maker = models.CharField("经办员", default="Menu_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("-tx_date", "id",)
        unique_together = (("tx_date", "menu_name"),)
        index_together = (("tx_date", "menu_name"), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.menu_name

class Role_mas(models.Model):
    role_name = models.CharField("角色", max_length=20)
    role_desc = models.CharField("角色描述", max_length=100)
    menu = models.ForeignKey(Menu_mas, related_name='Role_mas_menu_id', default=1, blank=True)  # 此项为参考外键的字段名称
    email = models.EmailField("电子邮件", blank=True, error_messages={'invalid': '格式错了.'})
    handphone = models.CharField("联系手机", max_length=20, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Role_mas", max_length=20)
    func = models.CharField("功能名称", default="Role_mas_add", max_length=20)
    maker = models.CharField("经办员", default="Role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('role_name',), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

    def get_absolute_url_dsp(self):
        return reverse("kernal:role_mas_dsp", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:role_mas_tmp_amd2lvl", args=[self.id])

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

class Role_mas_tmp(models.Model):
    id = models.AutoField("角色序号", primary_key=True,)
    role_name = models.CharField("角色名称", max_length=20)
    role_desc = models.CharField("角色描述", max_length=100)
    menu = models.ForeignKey(Menu_mas, related_name='Role_mas_tmp_menu_id', default=1, blank=True)  # 此项为参考外键的字段名称
    email = models.EmailField("电子邮件", blank=True)
    handphone = models.CharField("联系手机", max_length=20, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号")
    prod = models.CharField("产品名称", default="Role_mas", max_length=20)
    func = models.CharField("功能名称", default="role_mas_tmp_add", max_length=20)
    maker = models.CharField("经办员", default="Role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('role_name',), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

    def get_absolute_url_dsp(self):
        return reverse("kernal:role_mas_tmp_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:role_mas_tmp_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:role_mas_tmp_amd2lvl", args=[self.id])

    # def get_absolute_url_add(self):

class Role_log(models.Model):
    tx_date = models.DateTimeField("交易日期", default=timezone.now)
    role_name = models.CharField("角色", max_length=20)
    role_desc = models.CharField("角色描述", max_length=100)
    menu = models.ForeignKey(Menu_mas, related_name='Role_log_menu_id', default=1, blank=True)  # 此项为参考外键的字段名称
    email = models.EmailField("电子邮件", blank=True, error_messages={'invalid': '格式错了.'})
    handphone = models.CharField("联系手机", max_length=20, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Role_mas", max_length=20)
    func = models.CharField("功能名称", default="Role_mas_add", max_length=20)
    maker = models.CharField("经办员", default="Role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("-tx_date", "id",)
        unique_together = (("tx_date", "role_name"),)
        index_together = (("tx_date", ), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.role_name

class User_role_mas(models.Model):
    id = models.AutoField("序号", primary_key=True)
    user = models.ForeignKey(User, related_name='user_role_mas_user_id', default=1, blank=True)  # 此项为参考外键的字段名称
    role = models.ForeignKey(Role_mas, related_name='user_role_mas_role_id', default=1, blank=True )  # 此项为参考外键的字段名称
    user_role_name = models.CharField("用户与角色关系", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_role_mas", max_length=20)
    func = models.CharField("功能名称", default="User_role_mas_add", max_length=30)
    maker = models.CharField("经办员", default="User_role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.user_role_name

    def get_absolute_url_dsp(self):
        return reverse("kernal:user_role_mas_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:user_role_mas_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:user_role_mas_amd2lvl", args=[self.id])

class User_role_mas_tmp(models.Model):
    id = models.AutoField("序号", primary_key=True)
    user = models.ForeignKey(User, related_name='user_role_tmp_user_id', default=1, blank=True)  # 此项为参考外键的字段名称
    role = models.ForeignKey(Role_mas, related_name='user_role_tmp_role_id', default=1, blank=True)  # 此项为参考外键的字段名称
    user_role_name = models.CharField("用户与角色关系", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_role_mas", max_length=20)
    func = models.CharField("功能名称", default="user_role_mas_tmp_add", max_length=30)
    maker = models.CharField("经办员", default="User_role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.user_role_name

    def get_absolute_url_dsp(self):
        return reverse("kernal:user_role_mas_tmp_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:user_role_mas_tmp_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:user_role_mas_tmp_amd2lvl", args=[self.id])

class User_role_log(models.Model):
    tx_date = models.DateTimeField("交易日期", default=timezone.now)
    id = models.AutoField("序号", primary_key=True)
    user = models.ForeignKey(User, related_name='user_role_log_user_id', default=1, )  # 此项为参考外键的字段名称
    role = models.ForeignKey(Role_mas, related_name='user_role_log_role_id', default=1, )  # 此项为参考外键的字段名称
    user_role_name = models.CharField("用户与角色关系长描述", max_length=100, blank=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_role_mas", max_length=20)
    func = models.CharField("功能名称", default="User_role_mas_add", max_length=30)
    maker = models.CharField("经办员", default="User_role_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (('id',),)
        index_together = (('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.user_role_name

class User_mas(models.Model):
    user = models.OneToOneField(User, unique=True)
    employee_id = models.CharField("工号", max_length=50, default=999999)
    name = models.CharField("姓名", max_length=120)
    on_board_date = models.DateField("报到日期", blank=True, null=True)
    address = models.CharField("地址", max_length=120, blank=True, null=True)
    age = models.IntegerField("年龄")
    phone = models.CharField("直线电话", max_length=100, blank=True, null=True)
    mobile_phone = models.CharField("移动电话", max_length=100, blank=True, null=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_mas", max_length=20)
    func = models.CharField("功能名称", default="User_mas_add", max_length=20)
    maker = models.CharField("经办员", default="User_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("user",)
        #unique_together = (('id',),)
        index_together = (('employee_id', 'name'), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

    def get_absolute_url_dsp(self):
        return reverse("kernal:user_mas_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:user_mas_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:user_mas_tmp_amd2lvl", args=[self.id])

class User_mas_tmp(models.Model):
    # user = models.OneToOneField(User, unique=True)
    employee_id = models.CharField("工号", max_length=50, default=999999)
    name = models.CharField("姓名", max_length=120)
    on_board_date = models.DateField("报到日期", blank=True, null=True)
    address = models.CharField("地址", max_length=120, blank=True, null=True)
    age = models.IntegerField("年龄")
    phone = models.CharField("直线电话", max_length=100, blank=True, null=True)
    mobile_phone = models.CharField("移动电话", max_length=100, blank=True, null=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_mas", max_length=20)
    func = models.CharField("功能名称", default="User_mas_add", max_length=20)
    maker = models.CharField("经办员", default="User_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("employee_id",)
        #unique_together = (('id',),)
        index_together = (('employee_id', 'name'), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

    def get_absolute_url_dsp(self):
        return reverse("kernal:user_mas_tmp_dsp", args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("kernal:user_mas_tmp_amd", args=[self.id])

    def get_absolute_url_amd2lvl(self):
        return reverse("kernal:user_mas_tmp_amd2lvl", args=[self.id])

class User_log(models.Model):
    tx_date = models.DateTimeField("交易日期", default=timezone.now)
    # user = models.OneToOneField(User, unique=True)
    user = models.ForeignKey(User, related_name='User_log_user_id')
    employee_id = models.CharField("工号", max_length=50, default=999999)
    name = models.CharField("姓名", max_length=120)
    on_board_date = models.DateField("报到日期", blank=True, null=True)
    address = models.CharField("地址", max_length=120, blank=True, null=True)
    age = models.IntegerField("年龄")
    phone = models.CharField("直线电话", max_length=100, blank=True, null=True)
    mobile_phone = models.CharField("移动电话", max_length=100, blank=True, null=True)
    status = models.CharField("状态", max_length=10)     # A-Active D-Deleted S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="User_mas", max_length=20)
    func = models.CharField("功能名称", default="User_mas_add", max_length=20)
    maker = models.CharField("经办员", default="User_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("user",)
        #unique_together = (('id',),)
        index_together = (('employee_id', 'name'), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'),)

    def __str__(self):
        return self.id

