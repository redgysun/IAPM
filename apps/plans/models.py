from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from users.models import CompanyInifo, UserProfile


# Create your models here.
# 创建审计计划库
class PlansInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name2', null=True,blank=True)
    audit_company = models.CharField(max_length=50, verbose_name='被审计单位名称',null=True,blank=True)
    audit_person = models.CharField(max_length=20, verbose_name='被审计人姓名', null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.CharField(max_length=50, verbose_name='审计项目名称', null=True,blank=True)
    project_year = models.CharField(max_length=5, verbose_name='项目年度', null=True,blank=True)
    plan_type = models.CharField(max_length=20, verbose_name='计划类型', null=True,blank=True)
    project_type = models.CharField(max_length=20, verbose_name='项目类别')
    project_basis = models.TextField(verbose_name='项目依据', null=True,blank=True)
    project_status = models.CharField(max_length=10, choices=(
        ('pl', '准备'), ('st', '启动'), ('ex', '执行'), ('cp', '完成'), ('re', '整改'), ('cl', '关闭')), default='pl',
                                      verbose_name='项目阶段')
    project_exaudit=models.BooleanField(default=False, verbose_name="是否外审")
    project_exauditname=models.CharField(max_length=50, verbose_name='外审组织名称',null=True,blank=True)
    status=models.BooleanField(default=True,verbose_name="逻辑删除")

    def __str__(self):
        return self.project_name

    def coding(self):
        from users.tests import coding
        key=str(self.id)
        coding=coding(key)
        return coding


    class Meta:
        verbose_name = '项目计划'
        verbose_name_plural = verbose_name


class StartFieldInfo(models.Model):
    project_name = models.ForeignKey(PlansInifo, verbose_name='项目名称', on_delete=models.CASCADE,
                                     related_name='project_name5')
    start_file = models.FileField(upload_to='plans/file/%Y/%m', max_length=100, verbose_name="计划文件", null=True,
                                  blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status=models.BooleanField(default=True, verbose_name="逻辑删除")

    def __str__(self):
        return self.project_name.project_name

    class Meta:
        verbose_name = '项目启动附件'
        verbose_name_plural = verbose_name


class AuditCompanyInfo(models.Model):
    audit_company = models.CharField(max_length=50, verbose_name='被审计单位名称')
    audit_person = models.CharField(max_length=20, verbose_name='被审计人姓名',null=True,blank=True)
    project_name = models.ForeignKey(PlansInifo, verbose_name='项目名称', on_delete=models.CASCADE,
                                     related_name='project_name1')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status=models.BooleanField(default=True, verbose_name="逻辑删除")

    def __str__(self):
        return self.audit_company

    class Meta:
        verbose_name = '被审计单位列表'
        verbose_name_plural = verbose_name


class AuditMemberInfo(models.Model):
    project_name = models.ForeignKey(PlansInifo, verbose_name='项目名称', on_delete=models.CASCADE,
                                     related_name='project_name3')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    username = models.ForeignKey(UserProfile, verbose_name='审计成员', on_delete=models.CASCADE, related_name='username1')
    audit_role = models.CharField(max_length=10, choices=(('lvl1', '主审'), ('lvl2', '组员'), ('lvl3', '其他')),
                                  default='lvl2', verbose_name='审计角色')
    status=models.BooleanField(default=True, verbose_name="逻辑删除")

    def __str__(self):
        return self.project_name.project_name

    class Meta:
        verbose_name = '审计成员信息'
        verbose_name_plural = verbose_name


class AllNoticeInfo(models.Model):
    notice_name =models.CharField(max_length=60,verbose_name='通知书名称')
    notice_type=models.CharField(max_length=10,verbose_name='通知类型',choices=(('audit','审计通知'),('nomal','日常通知'),('report','报告编号')),default='audit')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    company_id=models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name3', null=True,blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    project_name=models.ForeignKey(PlansInifo, verbose_name='项目名称', on_delete=models.CASCADE,
                                     related_name='project_name6',null=True,blank=True)
    notice_NO=models.CharField(max_length=20,verbose_name='通知书编号',null=True,blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计成员', on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.notice_name

    def year(self):
        from plans.models import  AllNoticeInfo
        date=AllNoticeInfo.objects.filter(status=True,id=self.id).first()
        year=date.add_time.year
        return year

    def file_num(self):
        from plans.models import AllNoticeFileInfo
        file_num=AllNoticeFileInfo.objects.filter(status=True,notice_name_id=self.id)
        return file_num



    class Meta:
        verbose_name='通知书'
        verbose_name_plural=verbose_name


class AllNoticeFileInfo(models.Model):
    notice_name=models.ForeignKey(AllNoticeInfo,verbose_name='通知书名称', on_delete=models.CASCADE,related_name='notice_name1', null=True,blank=True)
    company_id=models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name4', null=True,blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    notice_file = models.FileField(upload_to='plans/notice/%Y/%m', max_length=100, verbose_name="通知附件", null=True,
                                   blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status = models.BooleanField(default=True, verbose_name="逻辑删除")


    def __str__(self):
        return self.notice_name.nOtice_name

    def year(self):
        from plans.models import  AllNoticeFileInfo
        date=AllNoticeFileInfo.objects.filter(status=True,id=self.id).first()
        year=date.add_time.year
        return year

    class Meta:
        verbose_name='通知书附件'
        verbose_name_plural=verbose_name


class StartInfo(models.Model):
    project_name=models.ForeignKey(PlansInifo, verbose_name='项目名称', on_delete=models.CASCADE,
                                     related_name='project_name7')
    company_id=models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name5', null=True,blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    start_name=models.CharField(max_length=50,verbose_name='方案名称',null=True,blank=True)
    start_username=models.ForeignKey(UserProfile,verbose_name='编制人',on_delete=models.CASCADE,related_name='username_2')
    start_target=models.TextField(verbose_name='审计目标', null=True,blank=True)
    start_range = models.TextField(verbose_name='审计范围', null=True, blank=True)
    start_basis = models.TextField(verbose_name='审计依据', null=True, blank=True)
    start_content = models.TextField(verbose_name='审计内容', null=True, blank=True)
    start_progress = models.TextField(verbose_name='审计程序', null=True, blank=True)
    start_date=models.DateField(verbose_name='预计开始时间', null=True, blank=True)


    def __str__(self):
        return self.start_name

    class Meta:
        verbose_name='审计方案'
        verbose_name_plural=verbose_name



