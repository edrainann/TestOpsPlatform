#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30
# @Author  : Edrain

from django.http import HttpResponse
from django.shortcuts import render

from sign.sql_sync.execute_sql import exe_sql
from sign.models import SqlSync


def sql_sync(request):
    """SQL同步"""
    sql_sync_env_list = SqlSync.objects.all()
    return render(request, 'home/sql_sync.html', locals())


def execute_sql_sync(request):
    """执行SQL同步"""
    if request.method == "POST":
        choose_env = request.POST.get("choose_env", "")
        execute_sql = request.POST.get("execute_sql", "")
        print(choose_env, execute_sql)
        execute_sql_result_message = exe_sql(choose_env, execute_sql)
        return HttpResponse(execute_sql_result_message)
