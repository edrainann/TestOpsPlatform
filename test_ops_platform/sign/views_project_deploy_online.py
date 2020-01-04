#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/2
# @Author  : Edrain
from django.http import HttpResponse
from django.shortcuts import render

from sign.models import EnvironmentName, ProjectName, DeployExecuteAction


def test_env_deploy(request):
    """测试环境打包部署"""
    env_name_list = EnvironmentName.objects.all()
    project_name_list = ProjectName.objects.all()
    deploy_execute_action_list = DeployExecuteAction.objects.all()
    return render(request, 'home/test_env_deploy.html', locals())


def test_env_deploy_check_out_version(request):
    """测试环境打包部署--查看当前版本"""
    if request.method == "POST":
        env_name = request.POST.get("env_name", "")
        project_name = request.POST.get("project_name", "")
        version_number = request.POST.get("version_number", "")


def test_env_deploy_execute(request):
    """测试环境打包部署--执行"""
    if request.method == "POST":
        env_name = request.POST.get("env_name", "")
        project_name = request.POST.get("project_name", "")
        version_number = request.POST.get("version_number", "")
        deploy_execute_action = request.POST.get("deploy_execute_action", "")
        print(env_name, project_name, version_number, deploy_execute_action)
        test_env_deploy_execute_message = "...."
    return HttpResponse(test_env_deploy_execute_message)


def produce_env_online(request):
    """生产环境部署上线"""
    return render(request, 'home/produce_env_online.html')
