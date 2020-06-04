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
from django.urls import path,re_path
from .views import user_login, user_logout, user_register, user_setting,user_changepassword,user_changeitems,users_list
from .views import user_fixinfo,user_changeimage

urlpatterns = [
    path('user_login/', user_login, name='user_login'),
    path('user_logout', user_logout, name='user_logout'),
    path('user_register', user_register, name='user_register'),
    path('user_setting/', user_setting, name='user_setting'),
    path('user_changepassword', user_changepassword, name='user_changepassword'),
    path('users_list/', users_list, name='users_list'),
    re_path('user_changeitems/(\d+)', user_changeitems, name='user_changeitems'),
    path('user_changeimage/', user_changeimage, name='user_changeimage'),
    path('user_fixinfo/', user_fixinfo, name='user_fixinfo'),
]

# handler404 = 'users.views.handler_404'
# handler500 = 'users.views.handler_500'
