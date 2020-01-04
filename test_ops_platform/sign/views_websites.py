# -*- coding: utf-8 -*-
# @Time    : 2019/12/29 
# @Author  : Edrain

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from sign.models import CommonWebsites, CompanyWebsitesOnline


def common_websites(request):
    """常用网站"""
    websites_list = CommonWebsites.objects.all()
    add_website = "add_common_websites/"
    return render(request, 'home/common_websites.html', locals())


def add_common_websites(request):
    """常用网站"""
    if request.method == "POST":
        site_name = request.POST.get("site_name", "")
        site_url = request.POST.get("site_url", "")
        site_description = request.POST.get("site_description", "")
        # 添加到数据库
        sites = CommonWebsites.objects.create()
        sites.site_name = site_name
        sites.site_url = site_url
        sites.site_description = site_description
        sites.save()
    return HttpResponseRedirect(reverse('sign:common_websites'))


def company_websites_online(request):
    """公司网站_上线类"""
    websites_list = CompanyWebsitesOnline.objects.all()
    add_website = "add_company_websites_online/"
    return render(request, 'home/company_websites.html', locals())


def add_company_websites_online(request):
    """公司网站_上线类"""
    if request.method == "POST":
        site_name = request.POST.get("site_name", "")
        site_url = request.POST.get("site_url", "")
        site_description = request.POST.get("site_description", "")
        # 添加到数据库
        sites = CompanyWebsitesOnline.objects.create()
        sites.site_name = site_name
        sites.site_url = site_url
        sites.site_description = site_description
        sites.save()
    return HttpResponseRedirect(reverse('sign:company_websites_online'))
