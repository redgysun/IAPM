from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
#创建审计单位库
class CompanyInifo(models.Model):
    company_name = models.CharField(max_length=50,verbose_name='审计单位名称')
    company_code = models.CharField(max_length=20,verbose_name='组织机构代码证号')
    company_department= models.CharField(max_length=20,verbose_name='审计单位部门名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '审计单位名称'
        verbose_name_plural =verbose_name


# 创建审计用户库
class UserProfile(AbstractUser):
    company_name = models.ForeignKey(CompanyInifo,verbose_name='审计单位', on_delete=models.CASCADE,related_name='company_name1',default='1')
    user_image = models.ImageField(upload_to='users/image/%Y/%m',max_length=100,verbose_name="用户头像",null=True,blank=True,default='users/image/u6.jpg')
    user_PQ = models.CharField(max_length=100, verbose_name='职业资格',null=True, blank=True )
    user_phone=models.CharField(max_length=11, verbose_name='手机', null=True, blank=True)
    user_gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='male', verbose_name='性别')
    user_birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    leftbar_title=models.CharField(max_length=30,verbose_name="标题布局",default="HeaderL_Fix")
    leftbar_option=models.CharField(max_length=30,verbose_name="边栏布局",default="sidebar-static-minified")
    leftbar_titlecolor=models.CharField(max_length=30,verbose_name="标题背景",default="HeaderB_Light")
    leftbar_navcolor=models.CharField(max_length=30,verbose_name="导航背景",default="Sidebar2_Dark")
    leftbar_navposition=models.CharField(max_length=30,verbose_name="导航位置",default="Siderbar2_Left")


    def __str__(self):
        return self.username

    def project_num(self):
        from plans.models import AuditMemberInfo
        now_year=datetime.today().year
        project_num=AuditMemberInfo.objects.filter(status=True,add_time__year=now_year,username_id=self.id)
        return  project_num

    def lvl1_num(self):
        from plans.models import AuditMemberInfo
        now_year=datetime.today().year
        lvl1_num=AuditMemberInfo.objects.filter(status=True,add_time__year=now_year,username_id=self.id,audit_role='lvl1')
        return  lvl1_num

    def going_num(self):
        from plans.models import AuditMemberInfo,PlansInifo
        now_year=datetime.today().year
        ex_project_list=PlansInifo.objects.filter(status=True,company_id_id=self.company_name_id,project_status='ex')
        ex=list(set(ex_project.id for ex_project in ex_project_list))
        going_num=AuditMemberInfo.objects.filter(status=True,add_time__year=now_year,username_id=self.id,project_name_id__in=ex)
        return  going_num


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
