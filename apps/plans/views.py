from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.db.models import Count,Sum
from django.db.models.aggregates import Aggregate, Count, Sum
# Create your views here.
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import PlanAddInfoForm
from .models import PlansInifo, AllNoticeInfo, AllNoticeFileInfo, StartInfo, StartFieldInfo, AuditCompanyInfo, \
    AuditMemberInfo
from users.models import UserProfile
from django.db.models import Q
import os
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
import datetime
from django.core.files import File


@login_required(login_url='users/user_login/')
def plans_list(request):
    switch = request.GET.get('switch', '')
    all_plans = PlansInifo.objects.filter(project_status='pl', company_id=request.user.company_name)
    all_years = list(set(years.project_year for years in all_plans))
    plans_list = PlansInifo.objects.filter(status=True, project_status='pl', company_id=request.user.company_name.id)
    company_id = request.user.company_name_id
    this_year = datetime.date.today().year
    if switch:
        # 全局搜索功能的过滤
        keyword = request.GET.get('keyword', '')
        if keyword:
            plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name,
                                                   project_name__icontains=keyword)

        # 按年查询
        year = request.GET.get('year', '')
        if year:
            plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name, project_year=year)

        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(plans_list, 15)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        # return HttpResponse(json.dumps(test))

        return render(request, 'plans/plans_list.html', {
            'plans_list': plans_list,
            'pages': pages,
            'switch': switch,
            'all_years': all_years,
            'keyword': keyword,
            'year': year,
            'this_year': this_year,
            'company_id': company_id
        })



    else:

        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(plans_list, 15)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'plans/plans_list.html', {
            'plans_list': plans_list,
            'pages': pages,
            'switch': switch,
            'all_years': all_years,
            'this_year': this_year,
            'company_id': company_id
        })


@login_required(login_url='users/user_login/')
def plans_add(request):
    if request.method == "POST":
        this_year = datetime.date.today().year
        company_id = request.POST.get("company_id")
        project_name = request.POST.get("project_name")
        project_year = request.POST.get("project_year")
        plan_type = request.POST.get("plan_type")
        project_type = request.POST.get("project_type")
        project_basis = request.POST.get("project_basis")
        project_status = request.POST.get("project_status")
        project_exaudit=request.POST.get("project_exaudit")
        project_exauditname=request.POST.get("project_exauditname")
        test = {
            'company_id': company_id,
            'project_name': project_name,
            'project_year': project_year,
            'plan_type': plan_type,
            'project_type': project_type,
            'project_basis': project_basis,
            'project_status': project_status,
        }
        # return HttpResponse(json.dumps(test))
        # plan_add_form = PlanAddInfoForm(request.POST, instance=request.user)
        #     # if plan_add_form.is_valid():
        #     #     plan_add_form.save()
        #     #     return HttpResponse(json.dumps(test))
        #     #     # return render(request, 'plans/plans_list.html',{
        #     #     #     'this_year': this_year,
        #     #     # })
        #     #     # return HttpResponse(json.dumps(test))
        #     # else:
        #     #     # return render(request, 'plans/plans_list.html',{
        #     #     #     'this_year': this_year,
        #     #     # })
        #     #     test = {'status': 'false'}
        #     #     return HttpResponse(json.dumps(test))
        try:
            a = PlansInifo()
            a.company_id = request.user.company_name
            a.project_name = project_name
            a.project_year = project_year
            a.project_type = project_type
            a.plan_type = plan_type
            a.project_basis = project_basis
            a.project_status = project_status
            if project_exaudit == "True":
                a.project_exaudit=True
                a.project_exauditname=project_exauditname
            a.save()
            switch = request.GET.get('switch', '')
            all_plans = PlansInifo.objects.filter(project_status='pl', company_id=request.user.company_name)
            all_years = list(set(years.project_year for years in all_plans))
            plans_list = PlansInifo.objects.filter(status=True, project_status='pl',
                                                   company_id=request.user.company_name.id)
            company_id = request.user.company_name_id
            this_year = datetime.date.today().year
            if switch:
                # 全局搜索功能的过滤
                keyword = request.GET.get('keyword', '')
                if keyword:
                    plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name,
                                                           project_name__icontains=keyword)

                # 按年查询
                year = request.GET.get('year', '')
                if year:
                    plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name,
                                                           project_year=year)

                pagenum = request.GET.get('pagenum', '')
                pa = Paginator(plans_list, 15)
                try:
                    pages = pa.page(pagenum)
                except PageNotAnInteger:
                    pages = pa.page(1)
                except EmptyPage:
                    pages = pa.page(pa.num_pages)

                # return HttpResponse(json.dumps(test))

                return render(request, 'plans/plans_list.html', {
                    'plans_list': plans_list,
                    'pages': pages,
                    'switch': switch,
                    'all_years': all_years,
                    'keyword': keyword,
                    'year': year,
                    'this_year': this_year,
                    'company_id': company_id
                })



            else:

                pagenum = request.GET.get('pagenum', '')
                pa = Paginator(plans_list, 15)
                try:
                    pages = pa.page(pagenum)
                except PageNotAnInteger:
                    pages = pa.page(1)
                except EmptyPage:
                    pages = pa.page(pa.num_pages)

                return render(request, 'plans/plans_list.html', {
                    'plans_list': plans_list,
                    'pages': pages,
                    'switch': switch,
                    'all_years': all_years,
                    'this_year': this_year,
                    'company_id': company_id
                })

        except Exception as e:
            switch = request.GET.get('switch', '')
            all_plans = PlansInifo.objects.filter(project_status='pl', company_id=request.user.company_name)
            all_years = list(set(years.project_year for years in all_plans))
            plans_list = PlansInifo.objects.filter(status=True, project_status='pl',
                                                   company_id=request.user.company_name.id)
            company_id = request.user.company_name_id
            this_year = datetime.date.today().year
            if switch:
                # 全局搜索功能的过滤
                keyword = request.GET.get('keyword', '')
                if keyword:
                    plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name,
                                                           project_name__icontains=keyword)

                # 按年查询
                year = request.GET.get('year', '')
                if year:
                    plans_list = PlansInifo.objects.filter(status=True, company_id=request.user.company_name,
                                                           project_year=year)

                pagenum = request.GET.get('pagenum', '')
                pa = Paginator(plans_list, 15)
                try:
                    pages = pa.page(pagenum)
                except PageNotAnInteger:
                    pages = pa.page(1)
                except EmptyPage:
                    pages = pa.page(pa.num_pages)

                # return HttpResponse(json.dumps(test))

                return render(request, 'plans/plans_list.html', {
                    'plans_list': plans_list,
                    'pages': pages,
                    'switch': switch,
                    'all_years': all_years,
                    'keyword': keyword,
                    'year': year,
                    'this_year': this_year,
                    'company_id': company_id
                })



            else:

                pagenum = request.GET.get('pagenum', '')
                pa = Paginator(plans_list, 15)
                try:
                    pages = pa.page(pagenum)
                except PageNotAnInteger:
                    pages = pa.page(1)
                except EmptyPage:
                    pages = pa.page(pa.num_pages)

                return render(request, 'plans/plans_list.html', {
                    'plans_list': plans_list,
                    'pages': pages,
                    'switch': switch,
                    'all_years': all_years,
                    'this_year': this_year,
                    'company_id': company_id
                })



@login_required(login_url='users/user_login/')
def plan_detail(request, project_id):
    plan = PlansInifo.objects.filter(id=int(project_id)).first()
    # return HttpResponse(json.dumps(
    #     {'id': plan.id }
    # ))
    return render(request, 'plans/plan_detail.html', {'plan': plan
                                                      })


@login_required(login_url='users/user_login/')
def plan_fix(request):
    if request.method == "POST":
        this_year = datetime.date.today().year
        plan_id = request.POST.get("plan_id")
        project_name = request.POST.get("project_name")
        project_year = request.POST.get("project_year")
        plan_type = request.POST.get("plan_type")
        project_type = request.POST.get("project_type")
        project_basis = request.POST.get("project_basis")
        project_exaudit=request.POST.get("project_exaudit")
        project_exauditname=request.POST.get("project_exauditname")

        test = {
            'plan_id': plan_id,
            'project_name': project_name,
            'project_year': project_year,
            'plan_type': plan_type,
            'project_type': project_type,
            'project_basis': project_basis,
        }
        try:
            plan = PlansInifo.objects.filter(id=int(plan_id))
            a = plan[0]
            a.project_name = project_name
            a.project_year = project_year
            a.project_type = project_type
            a.plan_type = plan_type
            a.project_basis = project_basis
            if project_exaudit == "True":
                a.project_exaudit=True
                a.project_exauditname = project_exauditname
            else:
                a.project_exaudit=False
                a.project_exauditname=None
            a.save()
            plan = PlansInifo.objects.filter(id=int(plan_id)).first()
            # # PlansInifo.objects.create(company_id=company_id,project_year=project_year,project_type=project_type,plan_type=plan_type,project_basis=project_basis,project_status=project_status)
            return render(request, 'plans/plan_detail.html', {
                'plan': plan
            })
            # return HttpResponse(json.dumps(
            #     {'id':a.id }
            # ))

        except Exception as e:
            return render(request, 'plans/plans_list.html', {
                'this_year': this_year,
            })
            # return HttpResponse(json.dumps(
            #     {'id':'false' }
            # ))


@login_required(login_url='users/user_login/')
def plan_del(request):
    status = request.POST.get('status', '')
    plan_id = request.POST.get('plan_id')
    plan = PlansInifo.objects.filter(id=int(plan_id)).first()
    try:
        a = plan
        a.status = status
        a.save()
        # return HttpResponse(json.dumps(
        #     {'id':a.id }
        # ))
        return JsonResponse({'status': 'ok', 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'status': 'false', 'msg': '删除失败'})
    # return render(request, 'plans/plans_list.html', {
    # })
    #     return HttpResponse(json.dumps(
    #         {'id': 'false'}
    #     ))


@login_required(login_url='users/user_login/')
def ex_list(request):
    finish_plans = PlansInifo.objects.filter(project_status='cp', status=True, company_id=request.user.company_name)
    ex_plans = PlansInifo.objects.filter(project_status='ex', status=True, company_id=request.user.company_name)

    all_years = list(set(years.project_year for years in finish_plans))
    year = request.GET.get('year', '')
    if year:
        finish_plans = PlansInifo.objects.filter(status=True, company_id=request.user.company_name, project_year=year,
                                                 project_status='cp')

    keyword = request.GET.get('keyword', '')
    if keyword:
        finish_plans = PlansInifo.objects.filter(status=True, project_status='cp', company_id=request.user.company_name,
                                                 project_name__icontains=keyword)
        ex_plans = PlansInifo.objects.filter(status=True, project_status='ex', company_id=request.user.company_name,
                                             project_name__icontains=keyword)

    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(finish_plans, 15)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)
    return render(request, 'plans/ex_list.html', {
        'finish_plans': finish_plans,
        'ex_plans': ex_plans,
        'all_years': all_years,
        'pages': pages,
        'year': year,
        'keyword': keyword,

    })
    # return HttpResponse(json.dumps(
    #     {'finish_plans':finish_plans.first(),
    #     'ex_plans':ex_plans.first(),
    #     'all_years':all_years,
    #     # 'pages': pages,
    #     'year':year,
    #     'keyword': keyword, }
    # ))


def plan_start(request):
    if request.method == "POST":
        plan_id = request.POST.get('plan_id')
        try:
            a = AuditMemberInfo()
            a.project_name_id = int(plan_id)
            a.username_id = request.user.id
            a.audit_role = 'lvl1'
            a.save()
            b = PlansInifo.objects.filter(status=True, id=int(plan_id)).first()
            b.project_status = 'ex'
            b.save()
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '修改失败'})


@login_required(login_url='users/user_login/')
def start_detail(request, project_id):
    switch = 'open'
    switch_stauts = PlansInifo.objects.filter(status=True, id=int(project_id), project_status='cp').first()
    if switch_stauts:
        switch = 'close'

    notice_info = AllNoticeInfo.objects.filter(status=True, company_id_id=int(request.user.company_name_id),
                                               project_name_id=int(project_id), notice_type='audit').first()
    if notice_info:
        notice_id_1 = notice_info.id
        notice_file = AllNoticeFileInfo.objects.filter(status=True, notice_name_id=int(notice_id_1))
    else:
        notice_file = ''

    start_detail = StartInfo.objects.filter(status=True, company_id=int(request.user.company_name_id),
                                            project_name=int(project_id)).first()
    start_file = StartFieldInfo.objects.filter(status=True, project_name=int(project_id))

    audit_company = AuditCompanyInfo.objects.filter(status=True, project_name_id=int(project_id))
    project_member = AuditMemberInfo.objects.filter(status=True, project_name_id=int(project_id))
    member_list_id = list(set(member.username.id for member in project_member))

    user_list = UserProfile.objects.filter(is_active='1', company_name=int(request.user.company_name_id))
    except_member_list = list(set(member.id for member in user_list))
    except_member = user_list.exclude(id__in=member_list_id)

    member_list = project_member.filter(username_id=request.user.id)
    if member_list:
        member = member_list[0]
    else:
        member = ''

    project_name = PlansInifo.objects.filter(id=int(project_id), status=True).first()
    return render(request, 'plans/start_detail.html', {
        'project_id': project_id,
        'switch': switch,
        'notice_info': notice_info,
        'notice_file': notice_file,
        'start_detail': start_detail,
        'start_file': start_file,
        'audit_company': audit_company,
        'project_member': project_member,
        'member': member,
        'except_members': except_member,
        'project_name': project_name
    })
    #     return HttpResponse(json.dumps(
    #         {'id': notice_info.id}
    #     ))


def notice_info(request):
    if request.method == "POST":
        project_id = request.POST.get('project_id')
        notice_name = request.POST.get('notice_name')
        notice_NO = request.POST.get('notice_NO')
        notice_info = AllNoticeInfo.objects.filter(status=True, company_id=int(request.user.company_name_id),
                                                   project_name=int(project_id), notice_type='audit')
        if notice_info:
            notice_info1 = notice_info[0]
            try:
                a = notice_info1
                a.notice_name = notice_name
                a.notice_NO = notice_NO
                a.project_name_id = int(project_id)
                a.notice_type = 'audit'
                a.company_id_id = int(request.user.company_name_id)
                a.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功1'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '修改失败1'})

        else:
            notice_info = AllNoticeInfo()
            try:
                a = notice_info
                a.notice_name = notice_name
                a.notice_NO = notice_NO
                a.project_name_id = int(project_id)
                a.notice_type = 'audit'
                a.company_id_id = int(request.user.company_name_id)
                a.save()
                return JsonResponse({'status': 'ok', 'msg': '修改成功2'})
            except Exception as e:
                return JsonResponse({'status': 'false', 'msg': '修改失败2'})


def notice_file(request):
    if request.method == "POST":

        notice_file1 = request.FILES.get("notice_file1")
        notice_id = request.POST.get("notice_id")
        company_id = request.user.company_name_id
        veri = AllNoticeInfo.objects.filter(id=int(notice_id))
        try:
            a = AllNoticeFileInfo()
            a.company_id_id = int(company_id)
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
        start_name = request.POST.get('start_name')
        start_target = request.POST.get('start_target')
        start_range = request.POST.get('start_range')
        start_basis = request.POST.get('start_basis')
        start_content = request.POST.get('start_content')
        start_progress = request.POST.get('start_progress')
        start_date = request.POST.get('start_date')
        project_id = request.POST.get('project_id')
        start_info = StartInfo.objects.filter(project_name_id=int(project_id), status=True)
        if start_info:
            start_info1 = start_info[0]
            try:
                a = start_info1
                a.company_id_id = request.user.company_name_id
                a.project_name_id = int(project_id)
                a.start_username_id = request.user.id
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
                a.company_id_id = request.user.company_name_id
                a.project_name_id = int(project_id)
                a.start_username_id = request.user.id
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
    project_id = request.POST.get("project_id")
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
    project_id = request.GET.get('project_id')
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

        audit_company = request.POST.get("audit_company")
        project_id = request.POST.get("project_id")
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
    project_id = request.GET.get('project_id')
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


def auto_company(request):
    auto_company = request.GET.get('auto_company')
    if auto_company:
        result_list = AuditCompanyInfo.objects.filter(audit_company__icontains=auto_company, status=True)
        result = list(set(result1.audit_company for result1 in result_list))
        if len(result) == 1:
            result = result[0]
            return JsonResponse({'status': 'ok', 'msg': result})
        elif result_list:
            result = '1' + str(result)
            return JsonResponse({'status': 'false', 'msg': result})
        else:
            pass


def audit_member(request):
    if request.method == "POST":
        audit_member = request.POST.get("audit_member")
        audit_role = request.POST.get("audit_role")
        project_id = request.POST.get("project_id")
        try:
            a = AuditMemberInfo()
            a.project_name_id = int(project_id)
            a.username_id = int(audit_member)
            a.audit_role = audit_role
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '审计人员更新成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '审计人员更新失败'})


def audit_member_del(request):
    audit_member = request.GET.get('audit_member')
    project_id=request.GET.get('project_id')
    audit_member_role_lvl1_num=AuditMemberInfo.objects.filter(status=True,project_name_id=int(project_id),audit_role='lvl1').count()
    if audit_member_role_lvl1_num < 2:
        return JsonResponse({'status': 'false', 'msg': '请保证项目至少有一名主审'})
    else:
        try:
            audit_member1 = AuditMemberInfo.objects.filter(id=int(audit_member))
            a = audit_member1[0]
            # a.audit_company=audit_company
            # a.audit_person=audit_company_person
            a.status = False
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '审计人员删除成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '审计人员删除失败'})


def all_notice_list(request):
    audit_notice_list=AllNoticeInfo.objects.filter(status=True,company_id_id=request.user.company_name_id,notice_type='audit').order_by('-add_time')
    report_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                     notice_type='report').order_by('-add_time')
    normal_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                     notice_type='nomal').order_by('-add_time')
    now_year=datetime.datetime.today().year
    return render(request,'plans/all_notice_list.html',{
        'audit_notice_list':audit_notice_list,
        'report_notice_list':report_notice_list,
        'normal_notice_list':normal_notice_list,
        'now_year':now_year
    })

def normal_notice(request):
    if request.method == "POST":
        notice_name = request.POST.get('notice_name')
        notice_NO = request.POST.get('notice_NO')
        notice_info1 = AllNoticeInfo()
        try:
            a = notice_info1
            a.notice_name = notice_name
            a.notice_NO = notice_NO
            a.notice_type = 'nomal'
            a.company_id_id = int(request.user.company_name_id)
            a.username_id= request.user.id
            a.project_name_id=199
            a.save()
            notice_info=AllNoticeInfo.objects.filter(status=True,company_id_id=request.user.company_name_id).order_by('-add_time').first()
            audit_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                             notice_type='audit').order_by('-add_time')
            report_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                              notice_type='report').order_by('-add_time')
            normal_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                              notice_type='nomal').order_by('-add_time')
            now_year = datetime.datetime.today().year
            return JsonResponse({'status': 'ok', 'msg': '新增成功','id':notice_info.id})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '新增失败'})
        #     pass
        # return render(request, 'plans/all_notice_file.html', {
        #     'audit_notice_list': audit_notice_list,
        #     'report_notice_list': report_notice_list,
        #     'normal_notice_list': normal_notice_list,
        #     'now_year': now_year,
        #     'notice_info': notice_info
        # })

def all_notice_file(request,notice_id):
    audit_notice_list=AllNoticeInfo.objects.filter(status=True,company_id_id=request.user.company_name_id,notice_type='audit').order_by('-add_time')
    report_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                     notice_type='report').order_by('-add_time')
    normal_notice_list = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                                     notice_type='nomal').order_by('-add_time')
    now_year=datetime.datetime.today().year
    notice_info = AllNoticeInfo.objects.filter(status=True, company_id_id=request.user.company_name_id,id=int(notice_id)).order_by(
        '-add_time').first()
    notice_file_list=AllNoticeFileInfo.objects.filter(status=True,notice_name_id=int(notice_id))
    return render(request,'plans/all_notice_file.html',{
                      'audit_notice_list': audit_notice_list,
                      'report_notice_list': report_notice_list,
                      'normal_notice_list': normal_notice_list,
                      'now_year': now_year,
                      'notice_info':notice_info,
                      'notice_file_list':notice_file_list
    })

def fix_normal_notice(request):
    if request.method == "POST":
        notice_name = request.POST.get('notice_name')
        notice_NO = request.POST.get('notice_NO')
        notice_id = request.POST.get('notice_id')
        notice_info1 = AllNoticeInfo.objects.filter(status=True,id=int(notice_id),company_id_id=request.user.company_name_id)
        notice_info=notice_info1[0]
        try:
            a = notice_info
            a.notice_name = notice_name
            a.notice_NO = notice_NO
            a.save()
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '修改失败'})

def normal_notice_file(request):
    if request.method == "POST":

        notice_file1 = request.FILES.get("notice_file1")
        notice_id = request.POST.get("notice_id")
        company_id = request.user.company_name_id
        veri = AllNoticeInfo.objects.filter(id=int(notice_id))
        try:
            a = AllNoticeFileInfo()
            a.company_id_id = int(company_id)
            a.notice_name_id = int(notice_id)
            a.notice_file = notice_file1
            a.save()
            # AllNoticeFileInfo.objects.create(company_id=int(company_id),notice_name=int(notice_id),notice_file=notice_file1)
            return JsonResponse({'status': 'ok', 'msg': '通知附件上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'msg': '通知附件上传失败'})


def normal_notice_file_del(request):
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
