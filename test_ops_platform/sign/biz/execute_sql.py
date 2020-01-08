#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/02/16
# @Author  : Edrain
import configparser

import pymysql

from env_config import current_record_path


def exe_sql(choose_env, execute_sql):
    """执行SQL"""
    right_result = []
    env = []
    error_message = []
    use_env = []
    if execute_sql != "":
        sql = execute_sql
        # 读取本地路径下，各个环境服务器的配置信息
        config = configparser.ConfigParser()
        config.read(f'{current_record_path}\\connect_db_info.ini')
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
            try:
                miss = connect_db_server(host, user, passwd, port, sql)
                right_result.append(miss)
                env.append(env_name)
            except Exception as e:
                print(e)
                env.append(env_name)
                right_result.append(e)
        print("当前SQL执行环境为：", env)
        print("正确结果：", right_result)
        print("错误结果：", error_message)
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

