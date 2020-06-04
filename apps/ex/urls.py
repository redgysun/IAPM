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
from .views import schedule_list, add_schedule, schedule_del, schedule_file, schedule_file_del, schedule_detail, \
    fix_schedule, problem_list, problem_detail, problem_add, auto_problem_class, add_problem
from .views import fix_problem, add_problem_file, del_problem_file, report_detail, add_feedback_file, del_feedback_file,re_finish_project
from .views import notice_info, add_report_file,del_report_file,clean_doubts,re_project,off_project,re_problem,re_feedback,add_feedback,del_feedback,re_feedback_file,re_feedback_file_del
from .views import re_problem_exportxl
urlpatterns = [
    re_path('schedule_list/(\d+)', schedule_list, name='schedule_list'),
    path('add_schedule', add_schedule, name='add_schedule'),
    path('schedule_del', schedule_del, name='schedule_del'),
    path('schedule_file', schedule_file, name='schedule_file'),
    path('schedule_file_del', schedule_file_del, name='schedule_file_del'),
    re_path('schedule_detail/(\d+)', schedule_detail, name='schedule_detail'),
    path('fix_schedule', fix_schedule, name='fix_schedule'),
    re_path('problem_list/(\d+)', problem_list, name='problem_list'),
    re_path('problem_detail/(\d+)', problem_detail, name='problem_detail'),
    re_path('problem_add/(\d+)', problem_add, name='problem_add'),
    path('auto_problem_class', auto_problem_class, name='auto_problem_class'),
    path('add_problem', add_problem, name='add_problem'),
    path('fix_problem', fix_problem, name='fix_problem'),
    # re_path('user_changeitems/(\d+)', user_changeitems, name='user_changeitems'),
    path('add_problem_file', add_problem_file, name='add_problem_file'),
    path('del_problem_file', del_problem_file, name='del_problem_file'),
    re_path('report_detail/(\d+)', report_detail, name='report_detail'),
    path('add_feedback_file', add_feedback_file, name='add_feedback_file'),
    path('del_feedback_file', del_feedback_file, name='del_feedback_file'),
    path('noitce_info', notice_info, name='notice_info'),
    path('add_report_file', add_report_file, name='add_report_file'),
    path('del_report_file', del_report_file, name='del_report_file'),
    path('clean_doubts', clean_doubts, name='clean_doubts'),
    path('off_project', off_project, name='off_project'),
    path('re_project', re_project, name='re_project'),
    re_path('re_problem/(\d+)', re_problem, name='re_problem'),
    re_path('re_feedback/(\d+)', re_feedback, name='re_feedback'),
    path('add_feedback', add_feedback, name='add_feedback'),
    path('del_feedback', del_feedback, name='del_feedback'),
    path('re_feedback_file', re_feedback_file, name='re_feedback_file'),
    path('re_feedback_file_del', re_feedback_file_del, name='re_feedback_file_del'),
    path('re_finish_project', re_finish_project, name='re_finish_project'),
    re_path('re_problem_exportxl/(\d+)', re_problem_exportxl, name='re_problem_exportxl'),
]

# handler404 = 'users.views.handler_404'
# handler500 = 'users.views.handler_500'
