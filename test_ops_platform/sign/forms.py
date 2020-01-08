# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/27
# @Author  : Edrain
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms


class UserForm(forms.Form):
    """用户-表单-信息"""
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='电子邮箱', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))  # 验证码输入框大小


class CommonWebsitesForm(forms.Form):
    site_name = forms.CharField()
    site_url = forms.URLField()
    site_description = forms.Textarea()
