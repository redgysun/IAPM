"""IA_project_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,re_path
from .views import plans_list,plans_add,plan_detail,plan_fix,plan_del,plan_start,start_detail,ex_list
from .views import notice_info,notice_file,notice_del,start_info,start_file,start_file_del,audit_company_info,audit_company_del,normal_notice_file_del
from .views import auto_company,audit_member,audit_member_del,all_notice_list,normal_notice,all_notice_file,fix_normal_notice,normal_notice_file

urlpatterns = [
    path('plans_list/', plans_list, name='plans_list'),
    path('plans_add/', plans_add, name='plans_add'),
    re_path('plan_detail/(\d+)', plan_detail, name='plan_detail'),
    path('plan_fix/',plan_fix,name='plan_fix'),
    # re_path('user_changeitems/(\d+)', user_changeitems, name='user_changeitems'),
    path('plan_del/',plan_del,name='plan_del'),
    path('plan_start/',plan_start,name='plan_start'),
    re_path('start_detail/(\d+)',start_detail,name='start_detail'),
    path('ex_list/',ex_list,name='ex_list'),
    path('notice_info',notice_info,name='notice_info'),
    path('notice_file',notice_file,name='notice_file'),
    path('notice_del',notice_del,name='notice_del'),
    path('start_info',start_info,name='start_info'),
    path('start_file',start_file,name='start_file'),
    path('start_file_del',start_file_del,name='start_file_del'),
    path('audit_company_info',audit_company_info,name='audit_company_info'),
    path('audit_company_del',audit_company_del,name='audit_company_del'),
    path('auto_company',auto_company,name='auto_company'),
    path('audit_member', audit_member, name='audit_member'),
    path('audit_member_del', audit_member_del, name='audit_member_del'),
    path('all_notice_list', all_notice_list, name='all_notice_list'),
    path('normal_notice', normal_notice, name='normal_notice'),
    re_path('all_notice_file/(\d+)',all_notice_file,name='all_notice_file'),
    path('fix_normal_notice', fix_normal_notice, name='fix_normal_notice'),
    path('normal_notice_file', normal_notice_file, name='normal_notice_file'),
    path('normal_notice_file_del', normal_notice_file_del, name='normal_notice_file_del'),



]

# handler404 = 'users.views.handler_404'
# handler500 = 'users.views.handler_500'
