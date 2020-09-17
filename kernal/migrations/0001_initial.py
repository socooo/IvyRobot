# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-28 11:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='交易日期')),
                ('menu_lvl', models.CharField(max_length=20, verbose_name='菜单级别')),
                ('menu_order', models.IntegerField(default=0, verbose_name='菜单显示顺序')),
                ('menu_parent_id', models.CharField(default=0, max_length=20, verbose_name='父菜单ID')),
                ('menu_name', models.CharField(max_length=100, verbose_name='菜单名称')),
                ('menu_sht_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单短描述')),
                ('menu_long_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单长描述')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='Menu_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='Menu_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Menu_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('-tx_date', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Menu_mas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='菜单序号')),
                ('menu_lvl', models.CharField(default=1, max_length=20, verbose_name='菜单级别')),
                ('menu_order', models.IntegerField(default=0, verbose_name='菜单显示顺序')),
                ('menu_parent_id', models.IntegerField(default=0, verbose_name='父菜单id')),
                ('menu_name', models.CharField(max_length=100, verbose_name='菜单名称')),
                ('menu_sht_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单短描述')),
                ('menu_long_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单长描述')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='Menu_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='Menu_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Menu_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Menu_mas_tmp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='菜单序号')),
                ('menu_lvl', models.CharField(default=1, max_length=20, verbose_name='菜单级别')),
                ('menu_order', models.IntegerField(default=0, verbose_name='菜单显示顺序')),
                ('menu_parent_id', models.IntegerField(default=0, verbose_name='父菜单ID')),
                ('menu_name', models.CharField(max_length=100, verbose_name='菜单名称')),
                ('menu_sht_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单短描述')),
                ('menu_long_desc', models.CharField(blank=True, max_length=100, verbose_name='菜单长描述')),
                ('status', models.CharField(default='A', max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(blank=True, default=1, verbose_name='版本号')),
                ('prod', models.CharField(blank=True, default='Menu_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(blank=True, default='Menu_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(blank=True, default='Menu_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(blank=True, default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Parm_mas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='参数序号')),
                ('key_grp', models.CharField(default='system', max_length=20, verbose_name='参数键值组')),
                ('key', models.CharField(default='system', max_length=20, verbose_name='参数键值')),
                ('value', models.CharField(max_length=100, verbose_name='参数内容')),
                ('key_desc', models.CharField(max_length=100, verbose_name='参数键值描述')),
                ('value_desc', models.CharField(max_length=100, verbose_name='参数内描述')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='Role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='Role_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('key_grp', 'key'),
            },
        ),
        migrations.CreateModel(
            name='Role_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='交易日期')),
                ('role_name', models.CharField(max_length=20, verbose_name='角色')),
                ('role_desc', models.CharField(max_length=100, verbose_name='角色描述')),
                ('email', models.EmailField(blank=True, error_messages={'invalid': '格式错了.'}, max_length=254, verbose_name='电子邮件')),
                ('handphone', models.CharField(blank=True, max_length=20, verbose_name='联系手机')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='Role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='Role_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('-tx_date', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Role_mas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=20, verbose_name='角色')),
                ('role_desc', models.CharField(max_length=100, verbose_name='角色描述')),
                ('email', models.EmailField(blank=True, error_messages={'invalid': '格式错了.'}, max_length=254, verbose_name='电子邮件')),
                ('handphone', models.CharField(blank=True, max_length=20, verbose_name='联系手机')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='Role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='Role_mas_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Role_mas_tmp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='角色序号')),
                ('role_name', models.CharField(max_length=20, verbose_name='角色名称')),
                ('role_desc', models.CharField(max_length=100, verbose_name='角色描述')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='电子邮件')),
                ('handphone', models.CharField(blank=True, max_length=20, verbose_name='联系手机')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(verbose_name='版本号')),
                ('prod', models.CharField(default='Role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='role_mas_tmp_add', max_length=20, verbose_name='功能名称')),
                ('maker', models.CharField(default='Role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
                ('menu', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Role_mas_tmp_menu_id', to='kernal.Menu_mas')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='User_role_log',
            fields=[
                ('tx_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='交易日期')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('user_role_name', models.CharField(blank=True, max_length=100, verbose_name='用户与角色关系长描述')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='User_role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='User_role_mas_add', max_length=30, verbose_name='功能名称')),
                ('maker', models.CharField(default='User_role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_log_role_id', to='kernal.Role_mas')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_log_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='User_role_mas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('user_role_name', models.CharField(blank=True, max_length=100, verbose_name='用户与角色关系')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='User_role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='User_role_mas_add', max_length=30, verbose_name='功能名称')),
                ('maker', models.CharField(default='User_role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
                ('role', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_mas_role_id', to='kernal.Role_mas')),
                ('user', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_mas_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='User_role_mas_tmp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('user_role_name', models.CharField(blank=True, max_length=100, verbose_name='用户与角色关系')),
                ('status', models.CharField(max_length=10, verbose_name='状态')),
                ('ver_no', models.IntegerField(default=1, verbose_name='版本号')),
                ('prod', models.CharField(default='User_role_mas', max_length=20, verbose_name='产品名称')),
                ('func', models.CharField(default='user_role_mas_tmp_add', max_length=30, verbose_name='功能名称')),
                ('maker', models.CharField(default='User_role_mas', max_length=20, verbose_name='经办员')),
                ('inp_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('checker', models.CharField(default='---', max_length=20, verbose_name='复核员')),
                ('app_date', models.DateTimeField(blank=True, verbose_name='修改日期')),
                ('role', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_tmp_role_id', to='kernal.Role_mas')),
                ('user', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_role_tmp_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='role_mas',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='role_mas',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('role_name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='role_log',
            unique_together=set([('tx_date', 'role_name')]),
        ),
        migrations.AlterIndexTogether(
            name='role_log',
            index_together=set([('tx_date',), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='parm_mas',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='parm_mas',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('key_grp', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu_mas_tmp',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='menu_mas_tmp',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('menu_lvl', 'menu_parent_id', 'menu_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu_mas',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='menu_mas',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('menu_lvl', 'menu_parent_id', 'menu_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='menu_log',
            unique_together=set([('tx_date', 'menu_name')]),
        ),
        migrations.AlterIndexTogether(
            name='menu_log',
            index_together=set([('tx_date', 'menu_name'), ('status', 'func', 'maker', 'inp_date', 'checker', 'app_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='user_role_mas_tmp',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='user_role_mas_tmp',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='user_role_mas',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='user_role_mas',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='user_role_log',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='user_role_log',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='role_mas_tmp',
            unique_together=set([('id',)]),
        ),
        migrations.AlterIndexTogether(
            name='role_mas_tmp',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('role_name',)]),
        ),
    ]
