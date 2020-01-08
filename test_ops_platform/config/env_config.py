#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/7
# @Author  : Edrain
import re
from pathlib import Path

home_path = re.findall(r".*?test_ops_platform", str(Path.cwd()))  # 正则匹配出文件夹的主路径

current_record_path = str(Path(home_path[0]) / "config")
