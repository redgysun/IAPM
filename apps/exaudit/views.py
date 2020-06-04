from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.db.models import Count,Sum
from django.db.models.aggregates import Aggregate, Count, Sum
# Create your views here.
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from plans.forms import PlanAddInfoForm
from ex.models import ScheduleInifo, ProblemInfo, ScheduleFileInifo, ProblemFileInifo, FeedbackFileInifo, ReportFileInifo
from ex.models import RectificationPrjectInfo,RectificationProblemInfo,RectificationFeedbackInfo,RectificationFeedbackFileInfo
from plans.models import PlansInifo, AuditMemberInfo, AuditCompanyInfo, AllNoticeInfo,StartFieldInfo,StartInfo,AllNoticeFileInfo
from users.models import UserProfile
from django.db.models import Q
import os
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
import datetime
from django.core.files import File
from users.tests import coding,uncoding


def exaudit_return(request):
    return render(request,'exaudit/exaudit_return.html',{})

def exaudit_feedback(request):
    if request.method=='POST':
        re_problem_id=uncoding(request.POST.get('re_problem_id'))
        if re_problem_id == '0':
            return render(request, 'exaudit/exaudit_return.html', {
                're_problem_msg':'编码错误'
            })
        else:
            re_problem = RectificationProblemInfo.objects.filter(status=True, id=int(re_problem_id)).first()
            re_project = RectificationPrjectInfo.objects.filter(status=True,id=re_problem.re_project_id,re_status='pr').first()
            if re_project:
                re_feedback_list = RectificationFeedbackInfo.objects.filter(status=True,re_project_name_id=re_problem_id).order_by('-add_time')
                re_feedback_nm = list(set(re_feedback.id for re_feedback in re_feedback_list))
                today = datetime.datetime.now().today()
                re_feedback_file_list = RectificationFeedbackFileInfo.objects.filter(status=True, re_feedback_id__in=re_feedback_nm)
                return render(request,'exaudit/exaudit_feedback.html',{
                    're_project':re_project,
                    # 're_project_id':re_project_id,
                    're_problem':re_problem,
                    're_feedback_list':re_feedback_list,
                    'today':today,
                    're_feedback_file_list':re_feedback_file_list,
                    're_problem_id':coding(re_problem_id)
                })
            else:
                return render(request, 'exaudit/exaudit_return.html', {
                    're_problem_msg':'项目已整改结束'
                })

def add_feedback(request):
    if request.method == "POST":
        re_department=request.POST.get('re_department')
        re_person=request.POST.get('re_person')
        re_improve=request.POST.get('re_improve')
        re_date=request.POST.get('re_date')
        re_situation=request.POST.get('re_situation')
        accountability_is=request.POST.get('accountability_is')
        accountability_content=request.POST.get('accountability_content')
        announcement_is=request.POST.get('announcement_is')
        remarks=request.POST.get('remarks')
        re_problem_id=int(uncoding(request.POST.get('re_problem_id')))
        re_problem = RectificationProblemInfo.objects.filter(status=True, id=re_problem_id).first()
        re_project = RectificationPrjectInfo.objects.filter(status=True, id=re_problem.re_project_id,
                                                            re_status='pr').first()
        try:
            a=RectificationFeedbackInfo()
            a.re_project_name_id=re_problem_id
            a.company_id_id=re_project.company_id_id
            a.re_improve=re_improve
            a.re_department=re_department
            a.re_person=re_person
            a.re_date=datetime.datetime.strptime(re_date,'%Y-%m-%d')
            a.re_situation=re_situation
            a.accountability_is=accountability_is
            a.accountability_content=accountability_content
            a.announcement_is=announcement_is
            a.remarks=remarks
            a.save()
            re_problem=RectificationProblemInfo.objects.filter(status=True,id=int(re_problem_id))
            b=re_problem[0]
            b.re_improve=re_improve
            b.re_department = re_department
            b.re_person = re_person
            b.re_date = datetime.datetime.strptime(re_date, '%Y-%m-%d')
            b.re_situation = re_situation
            b.accountability_is = accountability_is
            b.accountability_content = accountability_content
            b.announcement_is = announcement_is
            b.remarks = remarks
            b.username_id=None
            b.save()
            return JsonResponse({'status': 'ok', 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '添加失败'})

def del_feedback(request):
    feedback_id = request.GET.get('feedback_id')
    feedback_list1 = RectificationFeedbackInfo.objects.filter(status=True, id=int(feedback_id))
    feedback_info = feedback_list1[0]
    try:
        problem_info_id=feedback_info.re_project_name_id
        a = feedback_info
        a.status = False
        a.save()
        feedback_info2=RectificationFeedbackInfo.objects.filter(status=True,re_project_name_id=problem_info_id).order_by('-add_time').first()
        problem_info=RectificationProblemInfo.objects.filter(status=True,id=problem_info_id).first()
        if feedback_info2:
            b=problem_info
            b.re_improve=feedback_info2.re_improve
            b.re_department=feedback_info2.re_department
            b.re_person=feedback_info2.re_person
            b.re_date=feedback_info2.re_date
            b.re_situation=feedback_info2.re_situation
            b.accountability_is=feedback_info2.accountability_is
            b.accountability_content=feedback_info2.accountability_content
            b.announcement_is=feedback_info2.announcement_is
            b.remarks=feedback_info2.remarks
            b.username_id=feedback_info2.username_id
            b.save()
        else:
            b=problem_info
            b.re_improve=None
            b.re_department=None
            b.re_person=None
            b.re_date=datetime.datetime.today()
            b.re_situation='pr'
            b.accountability_is='n'
            b.accountability_content=None
            b.announcement_is='n'
            b.remarks=None
            b.username_id=None
            b.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})


def re_feedback_file(request):
    re_problem_id = int(uncoding(request.POST.get('re_problem_id')))
    re_problem = RectificationProblemInfo.objects.filter(status=True, id=re_problem_id).first()
    re_feedback_id = request.POST.get('re_feedback_id')
    re_feedback_file = request.FILES.get('re_feedback_file')
    try:
        a=RectificationFeedbackFileInfo()
        a.company_id_id=re_problem.company_id_id
        a.re_feedback_id=int(re_feedback_id)
        a.re_file=re_feedback_file
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '新增成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '新增失败'})

def re_feedback_file_del(request):
    re_feedback_file_id = request.GET.get('re_feedback_file_id')
    re_feedback_file_list1 = RectificationFeedbackFileInfo.objects.filter(status=True, id=int(re_feedback_file_id))
    re_feedback_file = re_feedback_file_list1[0]
    try:
        a = re_feedback_file
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})



def start_detail(request):
    if request.method == "POST":
        switch = 'open'
    # switch_stauts = PlansInifo.objects.filter(status=True, id=int(project_id), project_status='cp').first()
    # if switch_stauts:
    #     switch = 'close'
        project_id=uncoding(request.POST.get('project_id'))
        project = PlansInifo.objects.filter(status=True, id=int(project_id),project_exaudit=True,project_status='ex').first()
        if project_id == '0':
            return render(request, 'exaudit/exaudit_return.html', {
                'project_msg':'编码错误'
            })
        elif not project :
            return render(request, 'exaudit/exaudit_return.html', {
                'project_msg':'非外审项目'
            })
        else:

            notice_info = AllNoticeInfo.objects.filter(status=True, company_id_id=project.company_id_id,
                                                       project_name_id=int(project_id), notice_type='audit').first()
            if notice_info:
                notice_id_1 = notice_info.id
                notice_file = AllNoticeFileInfo.objects.filter(status=True, notice_name_id=int(notice_id_1))
            else:
                notice_file = ''

            start_detail = StartInfo.objects.filter(status=True, company_id=project.company_id_id,
                                                    project_name=int(project_id)).first()
            start_file = StartFieldInfo.objects.filter(status=True, project_name=int(project_id))

            audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=int(project_id))
            project_member = AuditMemberInfo.objects.filter(status=True, project_name_id=int(project_id))
            member_list_id = list(set(member.username.id for member in project_member))

            user_list = UserProfile.objects.filter(is_active='1', company_name=project.company_id_id)
            except_member_list = list(set(member.id for member in user_list))
            except_member = user_list.exclude(id__in=member_list_id)

            # member_list = project_member.filter(username_id=request.user.id)
            # if member_list:
            #     member = member_list[0]
            # else:
            #     member = ''

            project_name = PlansInifo.objects.filter(id=int(project_id), status=True).first()
            project_id=coding(int(project_id))
            return render(request, 'exaudit/start_detail.html', {
                'project_id': project_id,
                'switch': switch,
                'notice_info': notice_info,
                'notice_file': notice_file,
                'start_detail': start_detail,
                'start_file': start_file,
                'audit_company': audit_company,
                'project_member': project_member,
                # 'member': member,
                'except_members': except_member,
                'project_name': project_name,
                'projcet':project
            })
            #     return HttpResponse(json.dumps(
            #         {'id': notice_info.id}
            #     ))

def start_detail1(request,project_id):
    switch = 'open'
# switch_stauts = PlansInifo.objects.filter(status=True, id=int(project_id), project_status='cp').first()
# if switch_stauts:
#     switch = 'close'

    project_id = uncoding(project_id)
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not project:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:

        notice_info = AllNoticeInfo.objects.filter(status=True, company_id_id=project.company_id_id,
                                                   project_name_id=int(project_id), notice_type='audit').first()
        if notice_info:
            notice_id_1 = notice_info.id
            notice_file = AllNoticeFileInfo.objects.filter(status=True, notice_name_id=int(notice_id_1))
        else:
            notice_file = ''

        start_detail = StartInfo.objects.filter(status=True, company_id=project.company_id_id,
                                                project_name=int(project_id)).first()
        start_file = StartFieldInfo.objects.filter(status=True, project_name=int(project_id))

        audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=int(project_id))
        project_member = AuditMemberInfo.objects.filter(status=True, project_name_id=int(project_id))
        member_list_id = list(set(member.username.id for member in project_member))

        user_list = UserProfile.objects.filter(is_active='1', company_name=project.company_id_id)
        except_member_list = list(set(member.id for member in user_list))
        except_member = user_list.exclude(id__in=member_list_id)

        # member_list = project_member.filter(username_id=request.user.id)
        # if member_list:
        #     member = member_list[0]
        # else:
        #     member = ''

        project_name = PlansInifo.objects.filter(id=int(project_id), status=True).first()
        project_id = coding(int(project_id))
        return render(request, 'exaudit/start_detail.html', {
            'project_id': project_id,
            'switch': switch,
            'notice_info': notice_info,
            'notice_file': notice_file,
            'start_detail': start_detail,
            'start_file': start_file,
            'audit_company': audit_company,
            'project_member': project_member,
            # 'member': member,
            'except_members': except_member,
            'project_name': project_name,
            'project':project
        })
        #     return HttpResponse(json.dumps(
        #         {'id': notice_info.id}
        #     ))

def notice_info(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
        if project_id == '0' or not project:
            return JsonResponse({'status': 'false', 'msg': '无法更新通知信息'})
        else:
            notice_name = request.POST.get('notice_name')

            notice_info = AllNoticeInfo.objects.filter(status=True, company_id=project.company_id_id,
                                                       project_name=int(project_id), notice_type='audit')
            if notice_info:
                notice_info1 = notice_info[0]
                try:
                    a = notice_info1
                    a.notice_name = notice_name
                    a.project_name_id = int(project_id)
                    a.notice_type = 'audit'
                    a.company_id_id = int(project.company_id_id)
                    a.save()
                    return JsonResponse({'status': 'ok', 'msg': '修改成功1'})
                except Exception as e:
                    return JsonResponse({'status': 'false', 'msg': '修改失败1'})

            else:
                notice_info = AllNoticeInfo()
                try:
                    a = notice_info
                    a.notice_name = notice_name
                    a.notice_NO = '请补充审计通知编号'
                    a.project_name_id = int(project_id)
                    a.notice_type = 'audit'
                    a.company_id_id = int(project.company_id_id)
                    a.save()
                    return JsonResponse({'status': 'ok', 'msg': '修改成功2'})
                except Exception as e:
                    return JsonResponse({'status': 'false', 'msg': '修改失败2'})

def notice_file(request):
    if request.method == "POST":
        notice_file1 = request.FILES.get("notice_file1")
        notice_id = request.POST.get("notice_id")

        notice_info = AllNoticeInfo.objects.filter(id=int(notice_id)).first()
        company_id=notice_info.company_id_id
        veri = AllNoticeInfo.objects.filter(id=int(notice_id))
        try:
            a = AllNoticeFileInfo()
            a.company_id_id = company_id
            a.notice_name_id = int(notice_id)
            a.notice_file = notice_file1
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '通知附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '通知附件上传失败'})


def notice_del(request):
    notice_id = request.GET.get('notice_id')
    notice_file = request.GET.get('notice_file')
    notice_company = request.GET.get('notice_company')
    notice_name = request.GET.get('notice_name')
    try:
        file = AllNoticeFileInfo.objects.filter(id=int(notice_id))
        a = file[0]
        a.notice_file = notice_file
        a.company_id_id = int(notice_company)
        a.notice_name_id = int(notice_name)
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '附件删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '附件删除失败'})


def start_info(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
        if project_id == '0':
            return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
        elif not project:
            return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
        else:
            start_name = request.POST.get('start_name')
            start_target = request.POST.get('start_target')
            start_range = request.POST.get('start_range')
            start_basis = request.POST.get('start_basis')
            start_content = request.POST.get('start_content')
            start_progress = request.POST.get('start_progress')
            start_date = request.POST.get('start_date')
            company_id=project.company_id_id
            start_info = StartInfo.objects.filter(project_name_id=int(project_id), status=True)
            if start_info:
                start_info1 = start_info[0]
                try:
                    a = start_info1
                    a.company_id_id = company_id
                    a.project_name_id = int(project_id)
                    a.start_username_id = 1
                    a.start_name = start_name
                    a.start_target = start_target
                    a.start_range = start_range
                    a.start_basis = start_basis
                    a.start_content = start_content
                    a.start_progress = start_progress
                    a.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    a.save()
                    return JsonResponse({'status': 'ok', 'msg': '更新成功1'})
                except Exception as e:
                    return JsonResponse({'status': 'false', 'msg': '更新失败1'})
            else:
                start_info = StartInfo()
                try:
                    a = start_info
                    a.company_id_id = company_id
                    a.project_name_id = int(project_id)
                    a.start_username_id = 1
                    a.start_name = start_name
                    a.start_target = start_target
                    a.start_range = start_range
                    a.start_basis = start_basis
                    a.start_content = start_content
                    a.start_progress = start_progress
                    a.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    a.save()
                    return JsonResponse({'status': 'ok', 'msg': '更新成功2'})
                except Exception as e:
                    return JsonResponse({'status': 'false', 'msg': '更新失败2'})

def start_file(request):
    start_file = request.FILES.get("start_file")
    project_id = uncoding(request.POST.get("project_id"))
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
    elif not project:
        return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
    else:
        try:
            a = StartFieldInfo()
            a.project_name_id = int(project_id)
            a.start_file = start_file
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '方案附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '方案附件上传失败'})


def start_file_del(request):
    project_id = uncoding(request.GET.get('project_id'))
    start_file = request.GET.get('start_file')
    try:
        start_file1 = StartFieldInfo.objects.filter(project_name_id=int(project_id),status=True,id=int(start_file))
        a = start_file1[0]
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '附件删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '附件删除失败'})


def audit_company_info(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get("project_id"))
        project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
        if project_id == '0':
            return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
        elif not project:
            return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
        else:
            audit_company = request.POST.get("audit_company")
            audit_company_person = request.POST.get("audit_company_person")

            try:
                a = AuditCompanyInfo()
                a.project_name_id = int(project_id)
                a.audit_company = audit_company
                a.audit_person = audit_company_person
                a.save()
                # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
                return JsonResponse({'status': 'ok', 'msg': '被审计人更新成功'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '被审计人更新失败'})


def audit_company_del(request):
    project_id = uncoding(request.GET.get('project_id'))
    audit_company_id=request.GET.get('audit_company_id')
    # audit_company_person=request.GET.get('audit_company_person')
    try:
        audit_company1 = AuditCompanyInfo.objects.filter(project_name_id=int(project_id),id=int(audit_company_id),status=True)
        a = audit_company1[0]
        # a.audit_company=audit_company
        # a.audit_person=audit_company_person
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '被审计人删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '被审计人删除失败'})


def schedule_list(request, project_id):
    project_id = uncoding(project_id)
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not project:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:
        keyword = request.GET.get('keyword', '')
        sc_list = ScheduleInifo.objects.filter(project_name_id=int(project_id), status=True)
        user_list = sc_list.filter(username_id=None).order_by('-add_time')
        if keyword:
            user_list = sc_list.filter(username_id=None).order_by('-add_time').filter(
                Q(schedule_title__icontains=keyword) | Q(schedule_content__icontains=keyword) | Q(
                    schedule_feedback__icontains=keyword) | Q(audit_company__audit_company__icontains=keyword) | Q(
                    audit_company__audit_person__icontains=keyword))
        title = PlansInifo.objects.filter(id=int(project_id), status=True).first()
        this_date = datetime.date.today()
        member_name_list = AuditMemberInfo.objects.filter(project_name_id=int(project_id))
        # member_user = member_name_list.filter(username_id=request.user.id).first()
        sc_file_list = ScheduleFileInifo.objects.filter(status=True, project_name_id=int(project_id))
        audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=int(project_id))

        project_id=coding(project_id)
        return render(request, 'exaudit/schedule_list.html', {
            'project_id': project_id,
            'sc_list': sc_list,
            'user_list': user_list,
            'title': title,
            'this_date': this_date,
            'member_name': member_name_list,
            'sc_file_list': sc_file_list,
            'audit_company': audit_company,

            # 'member_user': member_user

        })


def add_schedule(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get("project_id"))
        project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
        if project_id == '0':
            return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
        elif not project:
            return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
        else:
            audit_company = request.POST.get('audit_company')
            schedule_title = request.POST.get('schedule_title', '')
            schedule_content = request.POST.get('schedule_content', '')
            schedule_feedback = request.POST.get('schedule_feedback', '')
            start_time = request.POST.get('start_time', '')
            end_time = request.POST.get('end_time', '')
            # return HttpResponse('开发中')
            try:
                a = ScheduleInifo()
                a.company_id_id = project.company_id_id
                a.project_name_id = int(project_id)
                a.username_id = None
                if int(audit_company) > 0:
                    a.audit_company_id = int(audit_company)
                a.schedule_title = schedule_title
                a.schedule_content = schedule_content
                a.schedule_feedback = schedule_feedback
                a.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
                a.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
                a.save()
                return JsonResponse({'status': 'ok', 'msg': '提交成功'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '提交失败'})


def schedule_del(request):
    schedule_id = request.GET.get('schedule_id')
    project_id = uncoding(request.GET.get('project_id'))
    schedule_list = ScheduleInifo.objects.filter(status=True, id=int(schedule_id), project_name_id=int(project_id))
    schedule = schedule_list[0]
    try:
        a = schedule
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})


def schedule_file(request):
    project_id = uncoding(request.POST.get("project_id"))
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
    elif not project:
        return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
    else:
        schedule_file1 = request.FILES.get('schedule_file')
        audit_company = request.POST.get('audit_company')
        try:
            a = ScheduleFileInifo()
            a.project_name_id = int(project_id)
            a.company_id_id = project.company_id_id
            if int(audit_company) > 0:
                a.audit_company_id = int(audit_company)
            a.username_id = None
            a.schedule_file = schedule_file1
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '附件上传失败'})


def schedule_file_del(request):
    project_id = uncoding(request.GET.get("project_id"))
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return JsonResponse({'status': 'false', 'msg': '项目编码损坏请重新进入'})
    elif not project:
        return JsonResponse({'status': 'false', 'msg': '项目已经结束'})
    else:
        schedule_file_id = request.GET.get('schedule_file_id')
        schedule_file_list1 = ScheduleFileInifo.objects.filter(status=True, id=int(schedule_file_id))
        schedule_file1 = schedule_file_list1[0]
        try:
            a = schedule_file1
            a.status = False
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '删除成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '删除失败'})


def schedule_detail(request, schedule_id):
    schedule_id = uncoding(schedule_id)
    schedule_info = ScheduleInifo.objects.filter(id=int(schedule_id),project_name__project_status='ex',project_name__project_exaudit=True)
    if schedule_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not schedule_info:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:
        user = schedule_info.first()
        project_id = user.project_name.id
        audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=project_id)
        sc_file_list = ScheduleFileInifo.objects.filter(status=True, project_name=project_id)
        member_name_list = AuditMemberInfo.objects.filter(project_name_id=int(project_id))
        # member_user = member_name_list.filter(username_id=request.user.id).first()
        title = PlansInifo.objects.filter(id=int(project_id), status=True).first()
        switch = 'close'
        if title.project_status == 'ex' :
            switch = 'open'
        project_id=coding(project_id)
        schedule_id=coding(schedule_id)
        return render(request, 'exaudit/schedule_detail.html', {
            'schedule_id': schedule_id,
            'user': user,
            'project_id': project_id,
            'audit_company': audit_company,
            'sc_file_list': sc_file_list,
            'member_name':member_name_list,
            # 'member_user':member_user,
            'title':title,
            'switch':switch
        })

def fix_schedule(request):
    if request.method == "POST":
        audit_company = request.POST.get('audit_company')
        schedule_title = request.POST.get('schedule_title', '')
        schedule_content = request.POST.get('schedule_content', '')
        schedule_feedback = request.POST.get('schedule_feedback', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        project_id = uncoding(request.POST.get('project_id'))
        schedule_id = uncoding(request.POST.get('schedule_id'))
        # return HttpResponse('开发中')
        try:
            a1 = ScheduleInifo.objects.filter(id=int(schedule_id))
            a = a1[0]
            if int(audit_company) > 0:
                a.audit_company_id = int(audit_company)
            a.schedule_title = schedule_title
            a.schedule_content = schedule_content
            a.schedule_feedback = schedule_feedback
            a.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            a.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '提交成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '提交失败'})

def problem_list(request, project_id):
    project_id = uncoding(project_id)
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not project:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:
        do_problem_list = ProblemInfo.objects.filter(status=True, project_name_id=int(project_id), problem_status='do',username_id=None).order_by('-add_time')
        co_sg_problem_list = ProblemInfo.objects.filter(status=True, project_name_id=int(project_id), problem_status='co',username_id=None,
                                                        problem_type='sg').order_by('-add_time')
        co_re_problem_list = ProblemInfo.objects.filter(status=True, project_name_id=int(project_id), problem_status='co',username_id=None,
                                                        problem_type='re').order_by('-add_time')
        el_problem_list = ProblemInfo.objects.filter(status=True, project_name_id=int(project_id), problem_status='el',username_id=None).order_by('-add_time')
        problem_file_list = ProblemFileInifo.objects.filter(status=True, project_name_id=int(project_id))
        switch = 'open'
        project_id=coding(project_id)
        return render(request, 'exaudit/problem_list.html', {
            'project_id': project_id,
            'do_problem_list': do_problem_list,
            'co_sg_problem_list': co_sg_problem_list,
            'co_re_problem_list': co_re_problem_list,
            'el_problem_list': el_problem_list,
            'problem_file_list': problem_file_list,
            'switch':switch,
            'project':project
        })

def problem_add(request, project_id):
    project_id = uncoding(project_id)
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not project:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:
        audit_company = AuditCompanyInfo.objects.filter(project_name_id=int(project_id), status=True)
        project_id=coding(project_id)
        return render(request, 'exaudit/problem_add.html', {
            'project_id': project_id,
            'audit_company': audit_company
        })




def auto_problem_class(request):
    problem_class = request.GET.get('problem_class')
    project_id = uncoding(request.GET.get('project_id'))
    if problem_class:
        project_info_list = PlansInifo.objects.filter(status=True, id=int(project_id))
        project_info = project_info_list[0]
        result_list = ProblemInfo.objects.filter(company_id_id=project_info.company_id_id,
                                                 problem_class__icontains=problem_class, status=True)
        result=list(set(result1.problem_class for result1 in result_list))
        if len(result) == 1:
            result = result[0]
            return JsonResponse({'status': 'ok', 'msg': result})
        elif result_list:
            result = '1' + str(result)
            return JsonResponse({'status': 'false', 'msg': result})
        else:
            pass


def add_problem(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get("project_id"))
        project_info = PlansInifo.objects.filter(status=True, id=int(project_id)).first()
        audit_company = request.POST.get('audit_company')
        problem_title = request.POST.get('problem_title', '')
        problem_content = request.POST.get('problem_content', '')
        problem_feedback = request.POST.get('problem_feedback', '')
        problem_class = request.POST.get('problem_class', '')
        problem_type = request.POST.get('problem_type', '')
        problem_status = request.POST.get('problem_status', '')
        try:
            a = ProblemInfo()
            a.company_id_id = project_info.company_id_id
            a.username_id = None
            if int(audit_company) > 0:
                a.audit_company_id = int(audit_company)
            a.project_name_id = int(project_id)
            a.problem_title = problem_title
            a.problem_content = problem_content
            a.problem_feedback = problem_feedback
            a.problem_class = problem_class
            a.problem_type = problem_type
            a.problem_status = problem_status
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '新增成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '更新失败'})



def problem_detail(request, problem_id):
    problem_id=uncoding(problem_id)
    problem_info = ProblemInfo.objects.filter(status=True, id=int(problem_id)).first()
    if problem_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif problem_info.project_name.project_status != 'ex' and problem_info.project_name.project_exaudit != True:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:

        project_id = problem_info.project_name_id
        # user = AuditMemberInfo.objects.filter(status=True, project_name_id=project_id, username_id=request.user.id).first()
        switch = 'open'
        project_is = PlansInifo.objects.filter(status=True, id=int(project_id), project_status='ex').first()


        audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=int(project_id))
        problem_file_list = ProblemFileInifo.objects.filter(status=True, problem_id=int(problem_id))
        project_id=coding(project_id)
        return render(request, 'exaudit/problem_detail.html', {
            'project_id': project_id,
            'problem_info': problem_info,
            # 'user': user,
            'switch': switch,
            'audit_company': audit_company,
            'problem_file_list': problem_file_list

        })



def fix_problem(request):
    if request.method == "POST":
        problem_id = uncoding(request.POST.get('problem_id'))
        project_id = uncoding(request.POST.get("project_id"))
        audit_company = request.POST.get('audit_company')
        problem_title = request.POST.get('problem_title', '')
        problem_content = request.POST.get('problem_content', '')
        problem_feedback = request.POST.get('problem_feedback', '')
        problem_class = request.POST.get('problem_class', '')
        problem_type = request.POST.get('problem_type', '')
        problem_status = request.POST.get('problem_status', '')
        try:
            a1 = ProblemInfo.objects.filter(status=True, id=int(problem_id))
            a = a1[0]
            if int(audit_company) > 0:
                a.audit_company_id = int(audit_company)
            a.project_name_id = int(project_id)
            a.problem_title = problem_title
            a.problem_content = problem_content
            a.problem_feedback = problem_feedback
            a.problem_class = problem_class
            a.problem_type = problem_type
            a.problem_status = problem_status
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '修改失败'})

def add_problem_file(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        problem_file = request.FILES.get('problem_file')
        problem_id = uncoding(request.POST.get('problem_id'))
        audit_company = request.POST.get('audit_company')
        try:
            a = ProblemFileInifo()
            a.project_name_id = int(project_id)
            project_info=PlansInifo.objects.filter(status=True,id=int(project_id)).first()
            a.company_id_id = project_info.company_id_id
            if int(audit_company) > 0:
                a.audit_company_id = int(audit_company)
            a.username_id = None
            a.problem_file = problem_file
            a.problem_id_id = int(problem_id)
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '附件上传失败'})

def del_problem_file(request):
    problem_file_id = request.GET.get('problem_file')
    problem_id = uncoding(request.GET.get('problem_id'))
    problem_file_list1 = ProblemFileInifo.objects.filter(status=True, id=int(problem_file_id))
    problem_file1 = problem_file_list1[0]
    try:
        a = problem_file1
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})


def report_detail(request, project_id):

    project_id = uncoding(project_id)
    project = PlansInifo.objects.filter(status=True, id=int(project_id), project_exaudit=True,project_status='ex').first()
    if project_id == '0':
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '编码错误'
        })
    elif not project:
        return render(request, 'exaudit/exaudit_return.html', {
            'project_msg': '非外审项目'
        })
    else:

        feedback_file_list = FeedbackFileInifo.objects.filter(status=True, project_name_id=int(project_id)).order_by(
            'add_time')
        switch = 'close'
        project_info = PlansInifo.objects.filter(status=True, id=int(project_id),project_status='ex').first()
        if project_info:
            switch = 'open'
        # member = AuditMemberInfo.objects.filter(status=True, username_id=request.user.id,project_name_id=int(project_id)).first()
        notice_info = AllNoticeInfo.objects.filter(status=True, company_id_id=project.company_id_id,
                                                   project_name_id=int(project_id), notice_type='report').first()
        report_type1=['fi','fifi']
        report_fi_file=ReportFileInifo.objects.filter(status=True,project_name_id=int(project_id),report_type__in=report_type1).order_by('add_time')
        report_type2=['pr','prfi']
        report_pr_file=ReportFileInifo.objects.filter(status=True,project_name_id=int(project_id),report_type__in=report_type2).order_by('add_time')
        project_id=coding(project_id)
        return render(request, 'exaudit/report_detail.html', {
            'project_id': project_id,
            'feedback_file_list': feedback_file_list,
            'switch': switch,
            # 'member': member,
            'notice_info': notice_info,
            'report_fi_file':report_fi_file,
            'report_pr_file':report_pr_file
        })


def add_feedback_file(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        feedback_file = request.FILES.get('feedback_file')
        feedback_type = request.POST.get('feedback_type')
        project_info=PlansInifo.objects.filter(status=True,id=int(project_id)).first()
        try:
            a = FeedbackFileInifo()
            a.project_name_id = int(project_id)
            a.company_id_id = project_info.company_id_id
            a.username_id = None
            a.feedback_file = feedback_file
            a.feedback_type = feedback_type
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '附件上传失败'})

def del_feedback_file(request):
    feedback_file_id = uncoding(request.GET.get('feedback_file'))
    feedback_file_list1 = FeedbackFileInifo.objects.filter(status=True, id=int(feedback_file_id))
    feedback_file1 = feedback_file_list1[0]
    try:
        a = feedback_file1
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})


def notice_info1(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        project_info = PlansInifo.objects.filter(status=True,id=int(project_id)).first()
        notice_name = request.POST.get('notice_name')
        notice_NO = request.POST.get('notice_NO')
        notice_info = AllNoticeInfo.objects.filter(status=True, company_id=project_info.company_id_id,
                                                   project_name=int(project_id), notice_type='report')
        if notice_info:
            notice_info1 = notice_info[0]
            try:
                a = notice_info1
                a.notice_name = notice_name
                if not notice_info1.notice_NO:
                    a.notice_NO = '请补充审计报告编号'
                a.notice_type = 'report'
                a.project_name_id = int(project_id)
                a.company_id_id = project_info.company_id_id
                a.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功1'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '修改失败1'})

        else:
            notice_info = AllNoticeInfo()
            try:
                a = notice_info
                a.notice_name = notice_name
                a.notice_NO = '请补充审计报告编号'
                a.notice_type = 'report'
                a.project_name_id = int(project_id)
                a.company_id_id = project_info.company_id_id
                a.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功2'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '修改失败2'})


def add_report_file(request):
    if request.method == "POST":
        project_id = uncoding(request.POST.get('project_id'))
        report_file = request.FILES.get('report_file')
        report_type = request.POST.get('report_type')
        project_info=PlansInifo.objects.filter(status=True,id=int(project_id)).first()
        try:
            a = ReportFileInifo()
            a.project_name_id = int(project_id)
            a.company_id_id = project_info.company_id_id
            a.username_id = None
            a.report_file = report_file
            a.report_type = report_type
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '附件上传失败'})

def del_report_file(request):
    report_file_id = uncoding(request.GET.get('report_file'))
    report_file_list1 = ReportFileInifo.objects.filter(status=True, id=int(report_file_id))
    report_file1 = report_file_list1[0]
    try:
        a = report_file1
        a.status = False
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})


def clean_doubts(request):
    project_id=uncoding(request.POST.get('project_id'))
    problem_list=ProblemInfo.objects.filter(status=True,project_name_id=int(project_id),problem_status='do')
    if problem_list:
        try:
            for problem in  problem_list:
                a=problem
                a.problem_status='co'
                a.save()
            return JsonResponse({'status': 'ok', 'msg': '更新成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '更新失败'})
    else:
        return JsonResponse({'status': 'false', 'msg': '没有疑点需要确认'})