import xadmin
from .models import CompanyInifo
from xadmin import views
#配置xadmin主题,注册的时候要用到专用的view去注册
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

class CommXadminSetting(object):
    site_title = '内审项目管理系统'
    site_footer = 'IAPM@redgysun'
    menu_style = 'accordion'
    model_icon = 'fa fa-check-square'

class CompanyInifoxadmin(object):
    list_display = ['company_name','company_code','add_time']
    search_fields = ['company_name']
    list_filter = ['company_name']




xadmin.site.register(CompanyInifo,CompanyInifoxadmin)
#注册主题类
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
#注册全局样式的类
xadmin.site.register(views.CommAdminView,CommXadminSetting)