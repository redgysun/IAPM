from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #使用django自己的UserAdmin来注册
from django.utils.translation import gettext, gettext_lazy as _
from .models import UserProfile,CompanyInifo

class UserAdmin(UserAdmin):
    #重写fieldsets在admin后台加入自己新增的字段
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
        #
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}), 'is_staff',
        (_('Company name'), {'fields': ('company_name',)}),
    )
    list_editable = ['email', 'first_name']

admin.site.register(UserProfile, UserAdmin)
admin.site.site_header = '内审项目管理系统'
admin.site.site_title = '后台设置'
# Register your models here.


 # Blog模型的管理器
@admin.register(CompanyInifo)
class Companydmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id','company_name', 'company_code', 'company_department', 'add_time')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-add_time',)

    # list_editable 设置默认可编辑字段
    list_editable = ['company_name', 'company_department']

    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    # list_display_links = ('id', 'company_name')
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)


