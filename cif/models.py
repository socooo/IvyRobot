from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
# 命名规则
# 不采用驼峰规则（避免因大小写引起血案）
# 类名首字母大写，实例采用小写
# 采用英文表达，不可使用中文缩写
# 采用动词，名词法，可使用下划线 "_" 分割
# 业务模型一般包括三张表： 
#  1. 主档表： xxx_mas
#  2. 临时表： xxx_tmp 未复核时的临时寄存
#  3. 日志表: xxx_log

class Cif_mas(models.Model):
    id_type = models.CharField("证件类型", max_length=20)
    id_country = models.CharField("证件国别", max_length=20)
    id_no = models.CharField("证件号", max_length=120)
    customer_id = models.CharField("客户号", max_length=20)
    first_name = models.CharField("客户（名）",max_length=120)
    last_name = models.CharField("客户（姓）",max_length=120)
    address = models.CharField("客户地址",max_length=120)
    age = models.IntegerField("客户年龄")
    balance = models.DecimalField("余额",max_digits=18, decimal_places=2)
    birthday = models.DateField("生日")
    # email=models.EmailField("客户电子邮件",blank=True)
    email = models.EmailField("客户电子邮件", blank=True,error_messages={'invalid': '格式错了.'})
    handphone=models.CharField("客户手机", max_length=20,blank=True)
#     created = models.DateTimeField("创建日期",default=timezone.now)
#     updated = models.DateTimeField("修改日期",default=timezone.now)
#     created = models.DateTimeField("录入",default=timezone.now)
#     updated = models.DateTimeField("复核",default=timezone.now)
    status=models.CharField("状态", max_length=10) 
    #A-Active
    #D-Deleted
    #S-Suspense
    ver_no = models.IntegerField("版本号",default=1)
    prod = models.CharField("产品名称",default="Cif_mas", max_length=20)
    func = models.CharField("功能名称",default="cifmas_add", max_length=20)
    maker = models.CharField("经办员",default="Cif_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期",default=timezone.now)
    checker = models.CharField("复核员",default="---", max_length=20)
    app_date = models.DateTimeField("修改日期",blank=True)
    
    class Meta:
        ordering = ("-inp_date",)
        index_together = (('id_type', 'id_country', 'id_no','customer_id'),)
#         unique_together = ('id_type', 'id_country','id_no',)
        
    def __str__(self):
        return self.customer_id
        
    def get_absolute_url_dsp(self):
        return reverse("cif:cifmas_dsp",args=[self.id])
    
    def get_absolute_url_amd(self):
        return reverse("cif:cifmas_amd",args=[self.customer_id])
    
    def get_absolute_url_amd2lvl(self):
        return reverse("cif:cifmas_tmp_amd2lvl",args=[self.customer_id])
    
    def get_absolute_url_add(self):
        return reverse("cif:cifmas_add")

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
    
class Cif_mas_tmp(models.Model):
    id_type = models.CharField("证件类型", max_length=20)
    id_country = models.CharField("证件国别", max_length=20)
    id_no = models.CharField("证件号", max_length=120)
    customer_id = models.CharField("客户号", max_length=20)
    first_name = models.CharField("客户（名）",max_length=120)
    last_name = models.CharField("客户（姓）",max_length=120)
    address = models.CharField("客户地址",max_length=120)
    age = models.IntegerField("客户年龄")
    balance = models.DecimalField("余额",max_digits=18, decimal_places=2)
    birthday = models.DateField("生日")
    email=models.EmailField("客户电子邮件",blank=True)
    handphone=models.CharField("客户手机", max_length=20,blank=True)
#     created = models.DateTimeField("创建日期",default=timezone.now)
#     updated = models.DateTimeField("修改日期",default=timezone.now)
    status=models.CharField("状态", max_length=10,default="A",blank=True)
    #A-Active
    #D-Deleted
    #S-Suspense
    ver_no = models.IntegerField("版本号",default=1)
    prod = models.CharField("产品名称",default="Cif_mas", max_length=20)
    func = models.CharField("功能名称",default="cifmas_tmp_add", max_length=20)
    maker = models.CharField("经办员",default="Cif_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期",default=timezone.now)
    checker = models.CharField("复核员",default="---", max_length=20)
    app_date = models.DateTimeField("修改日期",blank=True)

    class Meta:
        ordering = ("-inp_date",)
        index_together = (('id_type', 'id_country', 'id_no','customer_id'),)
#         unique_together = ('id_type', 'id_country','id_no',)

    def __str__(self):
        return self.customer_id

    def get_absolute_url_dsp(self):
        return reverse("cif:cifmas_tmp_dsp",args=[self.id])

    def get_absolute_url_amd(self):
        return reverse("cif:cifmas_tmp_amd",args=[self.customer_id])

    def get_absolute_url_add(self):
        return reverse("cif:cifmas_tmp_add")
    
class Cif_log(models.Model):
    tx_date = models.DateTimeField("交易日期",default=timezone.now)
    id_type = models.CharField("证件类型", max_length=20)
    id_country = models.CharField("证件国别", max_length=20)
    id_no = models.CharField("证件号", max_length=120)
    customer_id = models.CharField("客户号", max_length=20)
    first_name = models.CharField("客户（名）",max_length=120)
    last_name = models.CharField("客户（姓）",max_length=120)
    address = models.CharField("客户地址",max_length=120)
    age = models.IntegerField("客户年龄")
    balance = models.DecimalField("余额",max_digits=18, decimal_places=2)
    birthday = models.DateField("生日")
    email=models.EmailField("客户电子邮件",blank=True)
    handphone=models.CharField("客户手机", max_length=20,blank=True)
#     created = models.DateTimeField("创建日期",default=timezone.now)
#     updated = models.DateTimeField("修改日期",default=timezone.now)
#     created = models.DateTimeField("录入",default=timezone.now)
#     updated = models.DateTimeField("复核",default=timezone.now)
    status=models.CharField("状态", max_length=10) 
    #A-Active
    #D-Deleted
    #S-Suspense
    ver_no = models.IntegerField("版本号")
    prod = models.CharField("产品名称",default="Cif_mas", max_length=20)
    func = models.CharField("功能名称",default="cifmas_add", max_length=20)
    maker = models.CharField("经办员",default="Cif_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期",default=timezone.now)
    checker = models.CharField("复核员",default="---", max_length=20)
    app_date = models.DateTimeField("修改日期",blank=True)
    
    class Meta:
        ordering = ("-tx_date",)
        index_together = ('tx_date','customer_id','ver_no',)
#         unique_together = ('id_type', 'id_country','id_no',)
        
    def __str__(self):
        return self.customer_id
        
    def get_absolute_url_dsp(self):
        return reverse("cif:cifmas_dsp",args=[self.id])

class Cif_tst(models.Model):
    id = models.AutoField(primary_key=True)
    id_type = models.CharField("证件类型", max_length=20)
    id_country = models.CharField("证件国别", max_length=20)
    id_no = models.CharField("证件号", max_length=120)
    customer_id = models.CharField("客户号", max_length=20)
    first_name = models.CharField("客户（名）", max_length=120)
    last_name = models.CharField("客户（姓）", max_length=120)
    address = models.CharField("客户地址", max_length=120)
    age = models.IntegerField("客户年龄")
    balance = models.DecimalField("余额", max_digits=18, decimal_places=2)
    birthday = models.DateField("生日")
    # email=models.EmailField("客户电子邮件",blank=True)
    email = models.EmailField("客户电子邮件", blank=True, error_messages={'invalid': '格式错了.'})
    handphone = models.CharField("客户手机", max_length=20, blank=True)
    status = models.CharField("状态", max_length=10)
    # A-Active
    # D-Deleted
    # S-Suspense
    ver_no = models.IntegerField("版本号", default=1)
    prod = models.CharField("产品名称", default="Cif_mas", max_length=20)
    func = models.CharField("产品名称", default="Cif_mas", max_length=20)
    maker = models.CharField("经办员", default="Cif_mas", max_length=20)
    inp_date = models.DateTimeField("创建日期", default=timezone.now)
    checker = models.CharField("复核员", default="---", max_length=20)
    app_date = models.DateTimeField("修改日期", blank=True)

    class Meta:
        ordering = ("-inp_date",)
        unique_together = (('id_type', 'id_country', 'id_no'), ('customer_id',),) #多重index
        index_together = (('first_name', 'last_name'), ('age',), ('status',), ('func', 'maker', 'inp_date', 'checker', 'app_date', ),)

    def __str__(self):
        return self.customer_id

# class Cif_tst1(models.Model):
#     cust_id = models.ForeignKey(Cif_tst, related_name='cif_id1') # 此项为参考外键的字段名称
#     # cust_auto_id = models.ForeignKey(Cif_tst) # 此项为参考外键的字段名称
#
#     column = models.CharField(max_length=200)
#     created = models.DateField(auto_now_add=True)
#     class Meta:
#         ordering = ("cust_id",)
#         index_together = (('cust_id', 'column'), )

