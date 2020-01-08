#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/24
# @Author  : Edrain
from django.urls import path

from sign import views_sql_sync, views_project_deploy_online
from . import views, views_websites

app_name = 'sign'  # 设置命名空间
urlpatterns = [
    # path('', views.sign, name='sign'),
    # path('login_action/', views.login_action, name='login_action'),  # name的值可以在html中关联{% url 'xxx' %} template tag
    path('', views.home, name='home'),  # 跳转到主页
    path('sign_up/', views.sign_up, name='sign_up'),  # 注册
    path('sign_in/', views.sign_in, name='sign_in'),  # 登录
    path('logout/', views.logout, name='logout'),  # 退出
    path('base_home/', views.base_home, name='base_home'),  # 退出
    path('common_websites/', views_websites.common_websites, name='common_websites'),  # 常用网站
    path('common_websites/add_common_websites/', views_websites.add_common_websites, name='add_common_websites'),
    path('company_websites_online/', views_websites.company_websites_online, name='company_websites_online'),  # 常用网站
    path('company_websites_online/add_company_websites_online/', views_websites.add_company_websites_online,
         name='add_company_websites_online'),
    path('sql_sync/', views_sql_sync.sql_sync, name='sql_sync'),
    path('sql_sync/execute_sql_sync/', views_sql_sync.execute_sql_sync, name='execute_sql_sync'),

    path('test_env_deploy/', views_project_deploy_online.test_env_deploy, name='test_env_deploy'),
    path('test_env_deploy/test_env_deploy_check_out_version',
         views_project_deploy_online.test_env_deploy_check_out_version, name='test_env_deploy_check_out_version'),
    path('test_env_deploy/test_env_deploy_execute/', views_project_deploy_online.test_env_deploy_execute,
         name='test_env_deploy_execute'),

    path('produce_env_online/', views_project_deploy_online.produce_env_online, name='produce_env_online'),
    path('echo_once/', views_project_deploy_online.echo_once, name="echo_once")


]
