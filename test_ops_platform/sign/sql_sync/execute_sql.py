#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/02/16
# @Author  : Edrain
import configparser
import os
import re
from pathlib import Path

import paramiko
import pymysql

home_path = re.findall(r".*?test_ops_platform", str(Path.cwd()))  # 正则匹配出文件夹的主路径
cmd = str(Path(home_path[0]) / "sign" / "sql-sync")


def exe_sql(choose_env, execute_sql):
    """执行SQL"""
    right_result = []
    env = []
    error_message = []
    use_env = []
    if execute_sql != "":
        sql = execute_sql
        get_config_file(cmd)
        # 在本地路径下，保存sql执行记录
        execution_record_path = f'{cmd}\\sql执行记录.log'
        execution_record = open(execution_record_path, 'a', encoding='utf8')
        execution_record.write("\n" + "--" * 80 + "\n")
        execution_record.writelines(sql)
        execution_record.close()
        # 读取本地路径下，各个环境服务器的配置信息
        config = configparser.ConfigParser()
        config.read(f'{cmd}\\iniconfig.ini')
        all_env_list = config.sections()  # <class 'list'>: ['10', '11', '12']
        if choose_env == "ALL":
            use_env = all_env_list
        else:
            use_env.append(choose_env)
        for env_name in use_env:
            host = config.get(env_name, "host")
            user = config.get(env_name, "user")
            passwd = config.get(env_name, "password")
            port_str = config.get(env_name, "port")
            port = int(port_str)
            print(f'execute {env_name} start')
            # start_execute_sql_message = f'execute {env_name} start'
            try:
                miss = connect_db_server(host, user, passwd, port, sql)
                right_result.append(miss)
                env.append(env_name)
            except Exception as e:
                print(e)
                env.append(env_name)
                right_result.append(e)
        print("当前SQL执行环境为：", env)
        print("right result: ", right_result)
        print(error_message)
        if right_result:
            if len(right_result) == 1:
                execute_sql_result_message = f'执行完成，测试环境 {env[0]} 执行结果: {right_result[0]}'
                return execute_sql_result_message
            else:
                execute_all_sql_result_message = ""
                for i in range(len(env)):
                    result_i = f'执行完成，测试环境 {env[i]} 执行结果{[i + 1]}: {right_result[i]}\n'
                    execute_all_sql_result_message = f'{execute_all_sql_result_message}{result_i}'
                return execute_all_sql_result_message
        else:
            return "执行失败,执行失败的哇"
    else:
        return "请输入要执行的SQL！"


def get_config_file(cmd):
    """从系统上获取数据库的配置文件"""
    config = configparser.ConfigParser()
    try:
        config.read(f'{cmd}/server_info')  # 读取本地路径文件，名称为 server_info的文件，改文件需要和程序放在相同目录下
        sections = config.sections()
        print("这是获取本地的配置文件：", sections)
        host = config.get("info", "host")
        username = config.get("info", "user")
        password = config.get("info", "password")
        try:
            t = paramiko.Transport(host, 22)  # 用于做远程控制
            t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(t)
            src = '/home/config/iniconfig.ini'  # 远程路径和文件名
            des = os.path.join(cmd, 'iniconfig.ini')  # 拼接保存本地路径和文件名
            sftp.get(src, des)  # 下载文件
            t.close()
        except Exception as e:
            print(e)
            print(f'失败原因：{e}')
    except configparser.NoSectionError:
        print("无法找到配置文件")
        print(f'无法找到初始化服务器配置文件server_info')


def connect_db_server(host, username, password, port, sql):
    """连接数据库服务器"""
    conn = pymysql.connect(host=host, user=username, passwd=password, port=port, charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute("%s" % sql)
    message = f'there has {count} rows record'
    cursor.close()
    conn.commit()
    conn.close()
    return message
