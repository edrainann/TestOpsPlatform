#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/3
# @Author  : Edrain
import configparser
import select

import paramiko

from env_config import current_record_path


class SSHConnection(object):

    def __init__(self, deploy_env_name):
        # 读取本地路径下，各个环境服务器的配置信息
        config = configparser.ConfigParser()
        config.read(f'{current_record_path}\\connect_server_info.ini')
        self.server_host = config.get(deploy_env_name, "server_host")
        self.server_username = config.get(deploy_env_name, "server_username")
        self.server_password = config.get(deploy_env_name, "server_password")
        self.server_port = config.get(deploy_env_name, "server_port")

    def connect_server(self):
        """连接服务器，准备执行命令"""
        # 创建一个ssh对象
        ssh = paramiko.SSHClient()
        # 如果之前没有，连接过的ip，会出现选择yes或者no的操作，自动选择yes
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=self.server_host, username=self.server_username, password=self.server_password,
                    port=self.server_port, timeout=5)
        return ssh

    def run_command(self, command):
        """执行命令行"""
        ssh_in, ssh_out, ssh_error = self.connect_server().exec_command(command)
        result = ssh_out.read() or ssh_error.read()
        print(result.decode().strip())
        return result.decode().strip()

    def link_server_client(self, command):
        # 开启channel 管道
        transport = self.connect_server().get_transport()
        channel = transport.open_session()
        channel.get_pty()
        # 将命令传入管道中
        channel.exec_command(command)
        while True:
            # 判断退出的准备状态
            if channel.exit_status_ready():
                break
            try:
                # 通过socket进行读取日志，个人理解，linux相当于客户端，我本地相当于服务端请求获取数据（此处若有理解错误，望请指出。。谢谢）
                rl, wl, el = select.select([channel], [], [])
                if len(rl) > 0:
                    recv = channel.recv(1024)
                    # 此处将获取的数据解码成gbk的存入本地日志
                    print(recv.decode('utf8', 'ignore'))
            # 键盘终端异常
            except KeyboardInterrupt:
                print("Caught control-C")
                channel.send("\x03")  # 发送 ctrl+c
                channel.close()
        self.connect_server().close()

    def link_server_client_01(self, command):
        # 开启channel 管道
        transport = self.connect_server().get_transport()
        channel = transport.open_session()
        channel.get_pty()
        # 将命令传入管道中
        channel.exec_command(command)
        result = ""
        while True:
            # 判断退出的准备状态
            if channel.exit_status_ready():
                break
            else:
                # 通过socket进行读取日志，个人理解，linux相当于客户端，我本地相当于服务端请求获取数据（此处若有理解错误，望请指出。。谢谢）
                rl, wl, el = select.select([channel], [], [])
                if len(rl) > 0:
                    recv = channel.recv(1024)
                    global client_result
                    client_result = recv.decode('utf8', 'ignore')  # 此处将获取的数据解码成gbk的存入本地日志
                    # print(client_result)
            result = f'{result}{client_result}'
        self.connect_server().close()
        return result

    def echo_once_link(self, request, command):
        """
        在界面上实时滚动，实现类似在xshell中tail的功能
        :param request: 请求
        :param command: 命令
        :return:
        """
        ssh = self.connect_server()
        # 务必要加上get_pty=True,否则执行命令会没有权限
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        # result = stdout.read()
        # 循环发送消息给前端页面
        while True:
            nextline = stdout.readline().strip()  # 读取脚本输出内容
            # print(nextline.strip())
            request.websocket.send(nextline)  # 发送消息到客户端
            # 判断消息为空时,退出循环
            if not nextline:
                break
        ssh.close()  # 关闭ssh连接
        print("already close")



