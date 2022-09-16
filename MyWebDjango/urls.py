"""MyWebDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from UsersManage import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 用户管理
    path('user_info/', views.user_info),
    path('add_user/', views.add_user),
    path('edit_user/<int:nid>/', views.edit_user),
    path('delete_user/', views.delete_user),
    # 部门管理
    path('depart_info/', views.depart_info),
    path('add_depart/', views.add_depart),
    path('edit_depart/<int:nid>/', views.edit_depart),
    path('delete_depart/', views.delete_depart),
    # 靓号管理
    path('pretty_num_info/', views.pretty_num_info),
    path('add_pretty_num/', views.add_pretty_num),
    # 测试接口
    path('test/', views.test)
]
