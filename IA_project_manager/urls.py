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
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from IA_project_manager import settings
# import xadmin
from users import views


urlpatterns = [
    # path('xadmin/', xadmin.site.urls),
    path('admin/',admin.site.urls),
    # path('captcha/',include('captcha.urls')),
    path('' , views.index , name='index'),
    ##media配置——配合settings中的MEDIA_ROOT的配置，就可以在浏览器的地址栏访问media文件夹及里面的文件了
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('users/', include(('users.urls', "users"), namespace="users")),
    path('plans/', include(('plans.urls', "plans"), namespace="plans")),
    path('ex/', include(('ex.urls', "ex"), namespace="ex")),
    path('exaudit/', include(('exaudit.urls', "exaudit"), namespace="exaudit")),
]


handler404 = views.handler_404
handler500 = views.handler_500