from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from users.models import CompanyInifo, UserProfile
from plans.models import AuditCompanyInfo, PlansInifo,AllNoticeInfo


# Create your models here.
# 创建审计计划库
class ScheduleInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name11', null=True, blank=True)
    audit_company = models.ForeignKey(AuditCompanyInfo, verbose_name='被审计单位名称', on_delete=models.CASCADE, null=True,
                                      blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True, blank=True)
    schedule_title = models.CharField(max_length=50, verbose_name='任务名称', null=True, blank=True)
    schedule_content = models.TextField(verbose_name='任务内容', null=True, blank=True)
    schedule_feedback = models.TextField(verbose_name='任务反馈', null=True, blank=True)
    start_time = models.DateField(default=datetime.now, verbose_name='任务开始时间')
    end_time = models.DateField(default=datetime.now, verbose_name='任务结束时间')
    status = models.BooleanField(default=True, verbose_name="逻辑删除")

    def __str__(self):
        return self.schedule_title

    def coding(self):
        from users.tests import coding
        coding=coding(self.id)
        return coding

    class Meta:
        verbose_name = '任务详情'
        verbose_name_plural = verbose_name


class ProblemInfo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name12', null=True, blank=True)
    audit_company = models.ForeignKey(AuditCompanyInfo, verbose_name='被审计单位名称', on_delete=models.CASCADE, null=True,
                                      blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    problem_title = models.CharField(max_length=50, verbose_name='问题名称', null=True, blank=True)
    problem_content = models.TextField(verbose_name='问题内容', null=True, blank=True)
    problem_feedback = models.TextField(verbose_name='问题反馈', null=True, blank=True)
    problem_type = models.CharField(max_length=10, verbose_name='问题类型', choices=(('sg', '建议'), ('re', '整改')),
                                    default='sg')
    problem_class = models.CharField(max_length=20, verbose_name='问题分类', null=True, blank=True)
    problem_status = models.CharField(max_length=10, verbose_name='问题状态',
                                      choices=(('do', '疑点'), ('el', '消除'), ('co', '确认')), default='do')

    def __str__(self):
        return self.problem_title

    def coding(self):
        from users.tests import coding
        coding=coding(self.id)
        return coding

    class Meta:
        verbose_name = '问题详情'
        verbose_name_plural = verbose_name


class ScheduleFileInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name13', null=True, blank=True)
    audit_company = models.ForeignKey(AuditCompanyInfo, verbose_name='被审计单位名称', on_delete=models.CASCADE, null=True,
                                      blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    schedule_file = models.FileField(upload_to='plans/schedule/%Y/%m', max_length=100, verbose_name="记录文件", null=True,
                                     blank=True)

    def __str__(self):
        return self.project_name.project_name

    class Meta:
        verbose_name = '项目附件'
        verbose_name_plural = verbose_name


class ProblemFileInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name14', null=True, blank=True)
    audit_company = models.ForeignKey(AuditCompanyInfo, verbose_name='被审计单位名称', on_delete=models.CASCADE, null=True,
                                      blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    problem_file = models.FileField(upload_to='plans/problem/%Y/%m', max_length=100, verbose_name="问题文件", null=True,
                                    blank=True)
    problem_id = models.ForeignKey(ProblemInfo, verbose_name='问题编号', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.project_name.project_name

    class Meta:
        verbose_name = '问题附件'
        verbose_name_plural = verbose_name


class ReportFileInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name15', null=True, blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    report_file = models.FileField(upload_to='plans/report/%Y/%m', max_length=100, verbose_name="问题文件", null=True,
                                   blank=True)
    report_type = models.CharField(max_length=10, verbose_name='报告类型',
                                   choices=(('fi', '报告终稿'), ('fifi', '终稿附件'), ('pr', '报告过程稿'), ('prfi', '过程稿附件')),
                                   default='pr')

    def __str__(self):
        return self.project_name.project_name

    def coding(self):
        from users.tests import coding
        coding=coding(self.id)
        return coding

    class Meta:
        verbose_name = '报告附件'
        verbose_name_plural = verbose_name


class FeedbackFileInifo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name16', null=True, blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True,
                                 blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True,
                                     blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    feedback_file = models.FileField(upload_to='plans/feedback/%Y/%m', max_length=100, verbose_name="征求意见附件", null=True,
                                     blank=True)
    feedback_type = models.CharField(max_length=10, verbose_name='过程类型', choices=(('se', '征求'), ('fe', '反馈')),
                                     default='se')

    def __str__(self):
        return self.project_name.project_name

    def coding(self):
        from users.tests import coding
        coding=coding(self.id)
        return coding

    class Meta:
        verbose_name = '征求意见'
        verbose_name_plural = verbose_name


class RectificationPrjectInfo(models.Model):
    project_name = models.ForeignKey(PlansInifo, verbose_name='审计项目名称', on_delete=models.CASCADE, null=True,
                                     blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    re_status= models.CharField(max_length=10, verbose_name='整改状态', choices=(('pr', '整改中'), ('co', '整改完成')),
                                     default='pr')
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name19', null=True, blank=True)
    re_year=models.CharField(max_length=5,verbose_name='年度',default=str(datetime.now().year))
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    report_NO=models.ForeignKey(AllNoticeInfo, verbose_name='报告编号', on_delete=models.CASCADE,
                                   related_name='report_No', null=True, blank=True)

    def __str__(self):
        return self.project_name.project_name

    class Meta:
        verbose_name = '整改项目'
        verbose_name_plural = verbose_name

class RectificationProblemInfo(models.Model):
    re_problem=models.ForeignKey(ProblemInfo, verbose_name='整改问题', on_delete=models.CASCADE,
                                   related_name='problem_info', null=True, blank=True)
    re_project=models.ForeignKey(RectificationPrjectInfo, verbose_name='整改项目', on_delete=models.CASCADE,
                                   related_name='re_project', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name17', null=True, blank=True)
    re_improve=models.TextField(verbose_name='改进措施', null=True, blank=True)
    re_department=models.CharField(max_length=20, verbose_name='整改责任部门', null=True, blank=True)
    re_person=models.CharField(max_length=20,verbose_name='整改责任人',null=True,blank=True)
    re_date=models.DateField(default=datetime.now, verbose_name='整改完成时间',null=True,blank=True)
    re_situation=models.CharField(max_length=10, verbose_name='整改完成情况', choices=(('pr', '整改中'), ('co', '整改完成'),('un','无法整改')),
                                     default='pr',null=True,blank=True)
    accountability_is=models.CharField(max_length=10, verbose_name='是否问责', choices=(('n', '否'), ('y', '是')),
                                     default='n',null=True,blank=True)
    accountability_content=models.TextField(verbose_name='问责情况', null=True, blank=True)
    announcement_is=models.CharField(max_length=10, verbose_name='是否公告', choices=(('n', '否'), ('y', '是')),
                                     default='n',null=True,blank=True)
    remarks=models.TextField(verbose_name='备注', null=True, blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return self.re_problem.project_name

    def warn(self):
        import datetime
        overdue=datetime.datetime.today().date()-self.re_date
        overdue=overdue.days
        return overdue

    def feedback_nm(self):
        from ex.models import RectificationFeedbackInfo
        num = RectificationFeedbackInfo.objects.filter(status=True,re_project_name_id=self.id).count()
        return num

    def coding(self):
        from users.tests import coding
        key=str(self.id)
        coding=coding(key)
        return coding

    class Meta:
        verbose_name = '整改问题'
        verbose_name_plural = verbose_name





class RectificationFeedbackInfo(models.Model):
    re_project_name=models.ForeignKey(RectificationProblemInfo,verbose_name='整改问题', on_delete=models.CASCADE,
                                   related_name='problem_info1', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name21', null=True, blank=True)
    re_improve=models.TextField(verbose_name='改进措施', null=True, blank=True)
    re_department=models.CharField(max_length=20, verbose_name='整改责任部门', null=True, blank=True)
    re_person=models.CharField(max_length=20,verbose_name='整改责任人',null=True,blank=True)
    re_date=models.DateField(default=datetime.now, verbose_name='整改完成时间')
    re_situation=models.CharField(max_length=10, verbose_name='整改完成情况', choices=(('pr', '整改中'), ('co', '整改完成'),('un','无法整改')),
                                     default='pr')
    accountability_is=models.CharField(max_length=10, verbose_name='是否问责', choices=(('n', '否'), ('y', '是')),
                                     default='n')
    accountability_content=models.TextField(verbose_name='问责情况', null=True, blank=True)
    announcement_is=models.CharField(max_length=10, verbose_name='是否公告', choices=(('n', '否'), ('y', '是')),
                                     default='n')
    remarks=models.TextField(verbose_name='备注', null=True, blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.re_project_name.re_problem.project_name

    def file_num(self):
        from ex.models import RectificationFeedbackFileInfo
        num=RectificationFeedbackFileInfo.objects.filter(status=True,re_feedback_id=self.id).count()
        return num

    class Meta:
        verbose_name = '整改回复'
        verbose_name_plural = verbose_name


class RectificationFeedbackFileInfo(models.Model):
    company_id = models.ForeignKey(CompanyInifo, verbose_name='审计单位', on_delete=models.CASCADE,
                                   related_name='company_name18', null=True, blank=True)
    username = models.ForeignKey(UserProfile, verbose_name='审计人员姓名', on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    re_feedback = models.ForeignKey(RectificationFeedbackInfo, verbose_name='整改回复', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="逻辑删除")
    re_file = models.FileField(upload_to='re/feedback/%Y/%m', max_length=100, verbose_name="问题文件", null=True,
                                   blank=True)


    def __str__(self):
        return self.re_feedback.re_project_name.re_project.project_name.project_name

    class Meta:
        verbose_name = '整改附件'
        verbose_name_plural = verbose_name






