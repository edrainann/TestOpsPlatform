#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/2
# @Author  : Edrain
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from dwebsocket import accept_websocket

from project_deploy import SSHConnection
from test_ops_platform.sign.models import EnvironmentName, ProjectName, DeployExecuteAction


@accept_websocket
def echo_once(request):
    if not request.is_websocket():
        try:
            message1 = request.GET['mess1']
            print("===", message1)
            return HttpResponse(message1)
        except:
            return render(request, 'home/index_1.html', locals())
    else:  # 判断是不是websocket连接
        for message in request.websocket:
            # message = message.decode('utf-8')  # 接收前端发来的数据
            print("-----", message)
            seg = str(message).split("###")
            env_name = seg[0]
            project_name = seg[1]
            com = f'cd /home/shell/dev-sh;sh {project_name} version'
            print(com)
            command = 'cd /home/shell/dev-sh'  # 这里是要执行的命令或者脚本
            SSHConnection("Env_10").echo_once_link(request, command)
            print('end===')


def test_env_deploy(request):
    """测试环境打包部署"""
    env_name_list = EnvironmentName.objects.all()
    project_name_list = ProjectName.objects.all()
    deploy_execute_action_list = DeployExecuteAction.objects.all()
    return render(request, 'home/test_env_deploy.html', locals())


@accept_websocket
def test_env_deploy_check_out_version(request):
    """测试环境打包部署--查看当前版本"""
    if not request.is_websocket():
        try:
            env_name = request.GET['env_name']
            project_name = request.GET['project_name']
            return render(request, 'home/test_env_deploy.html', locals())
        except:
            return render(request, 'home/test_env_deploy.html', locals())
    else:
        for message in request.websocket:
            try:
                message = message.decode('utf-8')  # 接收前端发来的数据
                seg = str(message).split("###")
                env_name = seg[0]
                project_name = seg[1]
                command = f'cd /home/shell/dev-sh;sh {project_name}.sh version'  # 这里是要执行的命令或者脚本
                SSHConnection(env_name).echo_once_link(request, command)
            except:
                return HttpResponseRedirect(reverse('sign:test_env_deploy'))


@accept_websocket
def test_env_deploy_execute(request):
    """测试环境打包部署--update/new执行"""
    if not request.is_websocket():
        try:
            env_name = request.GET['env_name']
            project_name = request.GET['project_name']
            return HttpResponse(env_name, project_name)
        except:
            return render(request, 'home/test_env_deploy.html', locals())
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            seg = str(message).split("###")
            env_name = seg[0]
            project_name = seg[1]
            version_number = seg[2]
            deploy_execute_action = seg[3]
            command = f'cd /home/shell/dev-sh;sh {project_name}.sh {deploy_execute_action} {version_number}'  # 这里是要执行的命令或者脚本
            SSHConnection(env_name).echo_once_link(request, command)


def produce_env_online(request):
    """生产环境部署上线"""
    return render(request, 'home/produce_env_online.html')
