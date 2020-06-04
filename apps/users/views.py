from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.db.models import Count,Sum
from django.db.models.aggregates import Aggregate,Count,Sum
# Create your views here.
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import UserLoginForm,UserRegisterForm,UserChangePasswordForm,UserChangeInfoForm
from .models import UserProfile
from plans.models import PlansInifo,AuditMemberInfo
from ex.models import RectificationPrjectInfo,AllNoticeInfo
from django.db.models import Q
import os
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
import datetime
from .tests import coding,uncoding

#首页
@login_required(login_url='users/user_login/')
def index(request):
    now_year=datetime.datetime.today().year
    now_date=datetime.datetime.today()
    project_total_num=PlansInifo.objects.filter(status=True,company_id_id=request.user.company_name_id,add_time__year=now_year)
    project_ex_num=PlansInifo.objects.filter(status=True,company_id_id=request.user.company_name_id,project_status='ex')
    project_un_num = PlansInifo.objects.filter(status=True, company_id_id=request.user.company_name_id,
                                               project_status='pl')
    re_project_num=RectificationPrjectInfo.objects.filter(status=True,company_id_id=request.user.company_name_id,re_status='pr')
    normal_notice_num=AllNoticeInfo.objects.filter(status=True,company_id_id=request.user.company_name_id,notice_type='nomal',add_time__year=now_year)
    user_list=UserProfile.objects.filter(is_active=True,company_name_id=request.user.company_name_id)
    return render(request,'index.html',{
        'now_date':now_date,
        'project_total_num':project_total_num,
        'project_ex_num':project_ex_num,
        'project_un_num':project_un_num,
        're_project_num':re_project_num,
        'normal_notice_num':normal_notice_num,
        'user_list':user_list,

    })

#登陆界面


def user_login(request):
    if request.method == 'GET':
        return render(request,'users/login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                # user_list=UserProfile.objects.filter(username=username)
                # user=user_list[0]
                if user.is_active:
                    login(request, user)
                    if request.user.company_name_id > 1:
                        return redirect('/')
                    else:
                        logout(request)
                    # request.session.set_expiry(0)
                        return render(request, 'users/login.html', {
                            'msg': '请让管理员分配所属公司'
                        })

                else:
                    return render(request, 'users/login.html', {
                        'msg': '账户未激活'
                    })
            else:
                return render(request, 'users/login.html', {
                    'msg': '请检查账号密码'
                })
        else:
            return render(request, 'users/login.html', {
                'msg': '请检查账号密码',
                'user_login_form': user_login_form
            })

def user_logout(request):
    logout(request)
    return redirect(reverse('index'))

# return render(request,'index.html')

def user_register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    else:
        user_register_form = UserRegisterForm(request.POST)
        check = request.POST.get("check")
        pwd1 = request.POST.get("password1")
        pwd = request.POST.get("password")
        if user_register_form.is_valid() and check == 'ok' and pwd1 == pwd:
            username = user_register_form.cleaned_data['username']
            password = user_register_form.cleaned_data['password']
            user_list = UserProfile.objects.filter(Q(username=username)|Q(email=username))
            if user_list:
                return render(request,'users/register.html',{
                    'msg':'用户已经存在'
                })
            else:
                a = UserProfile()
                a.username = username
                a.set_password(password)
                a.email = username
                a.first_name = request.POST.get("first_name")
                a.save()
                return redirect(reverse('index'))
        else:
            return render(request, 'users/register.html', {
                'msg':'请检查注册信息'
            })




@login_required(login_url='users/user_login/')
def user_setting(request):
    start_day=request.user.add_time
    start_day1=start_day
    usedays=datetime.datetime.now()-start_day1
    # datetime.date.today datetime.now()
    project_num=AuditMemberInfo.objects.filter(status=True,username_id=request.user.id)
    return render(request, 'users/setting.html',{
        'usedays':usedays.days,
        'project_num':project_num
    })

@login_required(login_url='users/user_login/')
def user_changepassword(request):
    if request.method == 'GET':
        return render(request, 'users/changepassword.html')
    else:
        user_reset_form = UserChangePasswordForm(request.POST)
        username=request.POST.get("username")
        if user_reset_form.is_valid():
            password = user_reset_form.cleaned_data['password']
            password1 = user_reset_form.cleaned_data['password1']
            if password == password1:
                user_list=UserProfile.objects.filter(username=username)
                user=user_list[0]
                user.set_password(password1)
                user.save()
                logout(request)
                return redirect(reverse('users:user_login'))
            else:
                pass
        else:
            return render(request, 'users/changepassword.html', {
            'msg': '两次密码不一致',
            'user_reset_form': user_reset_form
            })

@login_required(login_url='users/user_login/')
def user_changeitems(request,item_id):
    username=request.user.username
    leftbar_items=request.POST.get('leftbar_titlecolr')
    user_list = UserProfile.objects.filter(username=username)
    user=user_list[0]
    if int(item_id) == 1:
        user.leftbar_titlecolor='HeaderB_Light'
        user.save()
        return redirect('/')
    elif int(item_id) == 2:
        user.leftbar_titlecolor = 'HeaderB_Dark'
        user.save()
        return redirect('/')
    elif int(item_id) == 3:
        user.leftbar_navcolor='Sidebar2_Light'
        user.save()
        return redirect('/')
    elif int(item_id) == 4:
        user.leftbar_navcolor='Sidebar2_Dark'
        user.save()
        return redirect('/')
    elif int(item_id) == 5:
        user.leftbar_navposition='Siderbar2_Left'
        user.save()
        return redirect('/')
    else:
        user.leftbar_navposition='Siderbar2_Right'
        user.save()
        return redirect('/')

@login_required(login_url='users/user_login/')
def users_list(request):
    company_id=request.user.company_name_id
    users_list=UserProfile.objects.filter(company_name_id=int(company_id))
    start_day=request.user.add_time
    start_day1=start_day
    usedays=datetime.datetime.now()-start_day1

    # 分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(users_list, 10)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)
    return render(request, 'users/users_list.html', {
        'pages': pages,
        'users_list': users_list,
        'usedays': usedays.days
    })


def user_changeimage(request):
    """用户上传头像操作"""
    if request.method == "POST":
        user_id = request.user.id  # 只是当前登录用户
        ret = {'state': True, 'error': None, 'data': None}
        avatar = request.FILES.get("image", None)


        try:
            user_obj = UserProfile.objects.filter(id=user_id).first()
            user_obj.user_image = avatar
            user_obj.save()
            ret["data"] = "头像更新成功"
            start_day = request.user.add_time
            start_day1 = start_day
            usedays = datetime.datetime.now() - start_day1
        except Exception as e:
            ret["state"] = False
            ret["data"] = "头像更新失败，请确认图片格式"
            print(e)
        # return HttpResponse(json.dumps(ret))
        return render(request, 'users/setting.html',{
            'usedays': usedays.days
        })

# def user_fixinfo(request):
#     if request.method == "POST":
#         user_id = request.user.id  # 只是当前登录用户
#         ret = {'state': True, 'error': None, 'data': None}
#         first_name = request.POST.get("first_name")
#         user_gender = request.POST.get("user_gender")
#         user_phone = request.POST.get("user_phone")
#         user_birthday = request.POST.get("user_birthday")
#         user_PQ = request.POST.get("user_PQ")
#
#         # test = {'first_name': str(first_name), 'user_gender': user_gender, 'user_phone': user_phone,
#         #         'user_birthday': user_birthday, 'user_PQ': user_PQ}
#         # return HttpResponse(json.dumps(test))
#         try:
#             user_obj = UserProfile.objects.filter(id=user_id).first()
#             user_obj.first_name = first_name
#             user_obj.user_gender = user_gender
#             user_obj.user_phone = user_phone
#             user_obj.user_birthday = datetime.datetime.strptime(user_birthday,'%Y-%m-%d')
#             user_obj.user_PQ = user_PQ
#             user_obj.save()
#             ret["state"] = "ok"
#             test = {'first_name': first_name, 'user_gender': user_gender, 'user_phone': user_phone,
#                     'user_birthday': user_birthday, 'user_PQ': user_PQ}
#             return HttpResponse(json.dumps(test))
#         except Exception as e:
#             ret["state"] = "false"
#             print(e)
#             return HttpResponse(json.dumps(ret))
            # return render(request, 'users/setting.html')

def user_fixinfo(request):
    user_changeinfo_form = UserChangeInfoForm(request.POST, instance=request.user)
    test = {'ststus':'false'}
    start_day = request.user.add_time
    start_day1 = start_day
    usedays = datetime.datetime.now() - start_day1
    if user_changeinfo_form.is_valid():
        user_changeinfo_form.save(commit=True)
        test={'status': 'ok'}
        return render(request, 'users/setting.html',{
            'usedays': usedays.days
        })
        # return HttpResponse(json.dumps(test))
    else:
        return render(request, 'users/setting.html',{
            'usedays': usedays.days
        })
        # return HttpResponse(json.dumps(test))

def handler_404(request,exception, template_name='404.html'):
    return render(request,template_name)

def handler_500(request,template_name='500.html'):
    return render(request,template_name)