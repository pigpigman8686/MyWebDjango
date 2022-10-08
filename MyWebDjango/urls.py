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
from UsersManage.views import views, user, department, prettyNumber, admin, login, task, order, upload

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 用户管理
    path('user_info/', user.user_info),
    path('add_user/', user.add_user),
    path('edit_user/<int:nid>/', user.edit_user),
    path('delete_user/', user.delete_user),
    # 部门管理
    path('depart_info/', department.depart_info),
    path('add_depart/', department.add_depart),
    path('edit_depart/<int:nid>/', department.edit_depart),
    path('delete_depart/', department.delete_depart),
    # 靓号管理
    path('pretty_num_info/', prettyNumber.pretty_num_info),
    path('add_pretty_num/', prettyNumber.add_pretty_num),
    path('delete_pretty_num/', prettyNumber.delete_pretty_num),
    # 管理员管理
    path('admin_info/', admin.admin_info),
    path('add_admin/', admin.add_admin),
    path('edit_admin/<int:nid>', admin.edit_admin),
    path('delete_admin/', admin.delete_admin),
    path('reset_admin/<int:nid>/', admin.reset_admin),
    # 登陆界面
    path('login/', login.login),
    path('image/code/', login.image_code),
    path('logout/', login.logout),
    # 任务管理
    path('task_list/', task.task_info),
    path('task_ajax/', task.task_ajax),  # 学习Ajax
    path('task_add/', task.add_task),
    # 订单管理
    path('order_list/', order.order_list),
    path('order_add/', order.add_order),
    path('order_delete/', order.order_delete),
    path('order_detail/', order.order_detail),
    path('order_edit/', order.order_edit),
    # 上传文件
    path('upload_list/', upload.upload_list),
    path('upload_form/', upload.upload_form),
    path('upload_modal_form/', upload.upload_modal_form),
    # 测试接口
    path('test/', views.test)
]
