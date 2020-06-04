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
from django.urls import path, re_path
from .views import exaudit_feedback,exaudit_return,add_feedback,del_feedback,re_feedback_file,re_feedback_file_del,start_detail,start_detail1,notice_info,notice_file,notice_del,start_info,start_file,start_file_del,audit_company_info,audit_company_del
from .views import schedule_list,add_schedule,schedule_detail,schedule_del,schedule_file,schedule_file_del,fix_schedule,problem_list,problem_add,auto_problem_class,add_problem,problem_detail,fix_problem,add_problem_file,del_problem_file
from .views import report_detail,add_feedback_file,del_feedback_file,notice_info1,add_report_file,del_report_file,clean_doubts
urlpatterns = [

    path('exaudit_feedback', exaudit_feedback, name='exaudit_feedback'),
    path('exaudit_return', exaudit_return, name='exaudit_return'),
    path('add_feedback', add_feedback, name='add_feedback'),
    path('del_feedback', del_feedback, name='del_feedback'),
    path('re_feedback_file', re_feedback_file, name='re_feedback_file'),
    path('re_feedback_file_del', re_feedback_file_del, name='re_feedback_file_del'),
    path('start_detail', start_detail, name='start_detail'),
    re_path('start_detail1/(\w+)', start_detail1, name='start_detail1'),
    path('notice_info', notice_info, name='notice_info'),
    path('notice_file', notice_file, name='notice_file'),
    path('notice_del', notice_del, name='notice_del'),
    path('start_info', start_info, name='start_info'),
    path('start_file', start_file, name='start_file'),
    path('start_file_del', start_file_del, name='start_file_del'),
    path('audit_company_info', audit_company_info, name='audit_company_info'),
    path('audit_company_del', audit_company_del, name='audit_company_del'),
    re_path('schedule_list/(\d+)', schedule_list, name='schedule_list'),
    path('add_schedule', add_schedule, name='add_schedule'),
    re_path('schedule_detail/(\d+)', schedule_detail, name='schedule_detail'),
    path('schedule_del', schedule_del, name='schedule_del'),
    path('schedule_file', schedule_file, name='schedule_file'),
    path('schedule_file_del', schedule_file_del, name='schedule_file_del'),
    path('fix_schedule', fix_schedule, name='fix_schedule'),
    re_path('problem_list/(\d+)', problem_list, name='problem_list'),
    re_path('problem_add/(\d+)', problem_add, name='problem_add'),
    path('auto_problem_class', auto_problem_class, name='auto_problem_class'),
    path('add_problem', add_problem, name='add_problem'),
    re_path('problem_detail/(\d+)', problem_detail, name='problem_detail'),
    path('fix_problem', fix_problem, name='fix_problem'),
    path('add_problem_file', add_problem_file, name='add_problem_file'),
    path('del_problem_file', del_problem_file, name='del_problem_file'),
    re_path('report_detail/(\d+)', report_detail, name='report_detail'),
    path('add_feedback_file', add_feedback_file, name='add_feedback_file'),
    path('del_feedback_file', del_feedback_file, name='del_feedback_file'),
    path('notice_info1', notice_info1, name='notice_info1'),
    path('add_report_file', add_report_file, name='add_report_file'),
    path('del_report_file', del_report_file, name='del_report_file'),
    path('clean_doubts', clean_doubts, name='clean_doubts'),
    # re_path('user_changeitems/(\d+)', user_changeitems, name='user_changeitems'),

]

# handler404 = 'users.views.handler_404'
# handler500 = 'users.views.handler_500'
