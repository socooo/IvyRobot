from django import forms
from .models import Cif_mas,Cif_mas_tmp
from django.forms import ValidationError
from django.contrib.admin import widgets

ID_COUNTRY = (
    ('CN', '中国'),
    ('US', '美国'),
    ('CA', '加拿大'),
)

ID_TYPES = (
    ('001', '身份证'),
    ('002', '护照 '),
    ('003', '军官证'),
)

STATUS = (
    ('A', '正常'),
    ('D', '关闭'),
    ('S', '挂起'),
)
  
class Cif_mas_Form(forms.ModelForm):
    id_type = forms.ChoiceField(
                            required=True,
                            choices=ID_TYPES,
                            label="证件类型",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    id_country = forms.ChoiceField(
                            required=True,
                            choices=ID_COUNTRY,
                            label="证件国家",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    id_no = forms.CharField(required=True,
                          label="证件号",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                                        }
                          )
    customer_id = forms.CharField(required=True,
                          label="客户号",
                          min_length=2,
                          max_length=20,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    first_name = forms.CharField(required=True,
                          label="客户（名）",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    last_name = forms.CharField(required=True,
                          label="客户（姓）",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    address=forms.CharField(required=True,
                          label="客户地址",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                                        }
                          )
    age=forms.IntegerField(required=True,
                          label="客户年龄",
                          error_messages={
                              'required': '此字段为必输项', 
                              'invalid': "请输入数字 "
                                        }
                          )
    balance=forms.DecimalField(required=True,
                          label="客户余额",
                          error_messages={
                              'required': '此字段为必输项', 
                              'invalid': "请输入数字 "
                                        }
                          )
    birthday = forms.DateField(widget=widgets.AdminDateWidget(),label="生日")
#     created = forms.DateTimeField("创建日期",default=timezone.now)
#     updated = forms.DateTimeField("修改日期",default=timezone.now)
    status = forms.ChoiceField(
                            required=True,
                            choices=STATUS,
                            label="客户状态",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    
    class Meta:
        model=Cif_mas
#         fields=("id_type","id_country","id_no","customer_id","first_name","last_name","address","age","balance","birthday","created","updated",)
        fields=("id_type","id_country","id_no","customer_id","first_name","last_name","address","age","balance","birthday","email","handphone","status","func") #,"inp_date","app_date")
        #fields='__all__'
        
    def clean(self):
        cleaned_data=super(Cif_mas_Form,self).clean()

        var_id_type=cleaned_data.get("id_type")
        var_id_country=cleaned_data.get("id_country")
        var_id_no=cleaned_data.get("id_no")

        var_address=cleaned_data.get("address")
        var_age=cleaned_data.get("age")
        var_email=cleaned_data.get("email")

        var_func=cleaned_data.get("func")

        if var_address.find("中南海") >=0 or var_address.find("钓鱼台") >=0 :
             raise ValidationError(var_address+ "，这个地址不允许登记")
        
        if var_age>=1 and var_age<=150:
            pass
        else:
            raise ValidationError("年龄应大于等于 1岁，小于 150岁")

        if (var_func=="cifmas_add"):
            cifmas_lst = Cif_mas.objects.filter(id_type=var_id_type, id_country=var_id_country, id_no=var_id_no)
            if (cifmas_lst.count()>=1):
                raise ValidationError("该客户的证件国家、证件类型、证件号已在主表中存在，请仔细检查。")\

        return cleaned_data
    
    
class Cif_mas_tmp_Form(forms.ModelForm):
    id_type = forms.ChoiceField(
                            required=True,
                            choices=ID_TYPES,
                            label="证件类型",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    id_country = forms.ChoiceField(
                            required=True,
                            choices=ID_COUNTRY,
                            label="证件国家",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    id_no = forms.CharField(required=True,
                          label="证件号",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                                        }
                          )
    customer_id = forms.CharField(required=True,
                          label="客户号",
                          min_length=2,
                          max_length=20,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    first_name = forms.CharField(required=True,
                          label="客户（名）",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    last_name = forms.CharField(required=True,
                          label="客户（姓）",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过20位"
                                        }
                          )
    address=forms.CharField(required=True,
                          label="客户地址",
                          min_length=2,
                          max_length=120,
                          error_messages={
                              'required': '此字段为必输项', 
                              'min_length': "此字段至少需输入至少2位",
                              'max_length': "此字段不可超过120位"
                                        }
                          )
    age=forms.IntegerField(required=True,
                          label="客户年龄",
                          error_messages={
                              'required': '此字段为必输项', 
                              'invalid': "请输入数字 "
                                        }
                          )
    balance=forms.DecimalField(required=True,
                          label="客户余额",
                          error_messages={
                              'required': '此字段为必输项', 
                              'invalid': "请输入数字 "
                                        }
                          )
    birthday = forms.DateField(widget=widgets.AdminDateWidget(),label="生日")
    status = forms.ChoiceField(
                            required=True,
                            choices=STATUS,
                            label="客户状态",
                            error_messages={
                              'required': '此字段为必输项'
                                        }
                          )
    
    class Meta:
        model = Cif_mas_tmp
        fields = ("id_type", "id_country", "id_no", "customer_id", "first_name", "last_name", "address", "age", "balance","birthday", "email", "handphone", "status", "func")
        #fields='__all__'

    def clean(self):
        cleaned_data=super(Cif_mas_tmp_Form,self).clean()

        import logging
        logger = logging.getLogger('sourceDns.webdns.views')

        var_id_type=cleaned_data.get("id_type")
        var_id_country=cleaned_data.get("id_country")
        var_id_no=cleaned_data.get("id_no")

        var_address= cleaned_data.get("address")
        var_age = cleaned_data.get("age")
        var_email = cleaned_data.get("email")

        var_maker = cleaned_data.get("maker")
        var_status = cleaned_data.get("status")

        var_func = cleaned_data.get("func")

        if var_address.find("中南海") >=0 or var_address.find("钓鱼台") >=0 :
             raise ValidationError(var_address+ "，这个地址不允许登记")
        
        if var_age>=1 and var_age<=150:
            pass
        else:
            raise ValidationError("年龄应大于等于 1岁，小于 150岁")

        if (var_func == "cifmas_tmp_add"):
            cifmas_lst = Cif_mas.objects.filter(id_type=var_id_type,id_country=var_id_country,id_no=var_id_no)
            if (cifmas_lst.count()>=1):
                raise ValidationError("该客户的证件国家、证件类型、证件号已在主表中存在，请仔细检查。")

        return cleaned_data