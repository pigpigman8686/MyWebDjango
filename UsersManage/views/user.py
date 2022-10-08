from django.shortcuts import render, redirect
import UsersManage.models as models
from UsersManage.utils.forms import UserModelForm
from UsersManage.utils.pagination import Pagination


def user_info(request):
    # generate_department()
    user_list = models.UsersInfo.objects.all().order_by('id')
    pagination = Pagination(request, user_list)
    context = {
        "user_list": pagination.page_queryset,
        "page_string": pagination.html()
    }
    return render(request, 'UsersInfo.html', context)


def add_user(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "AddUser.html", {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user_info/')

    return render(request, 'AddUser.html', {"form": form})


def edit_user(request, nid):
    row_data = models.UsersInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_data)  # 将已有的实例数据放入modelform中

        return render(request, 'EditUser.html', {"form": form})

    form_new = UserModelForm(data=request.POST, instance=row_data)  # 【注意】：带了instance才是修改，否则就会新添加一个
    if form_new.is_valid():
        # 默认保存用户输入的值，想额外保存一些值：
        # form_new.instance.字段名 = 值
        form_new.save()  # 保存修改
        return redirect('/user_info/')
    return render(request, 'AddUser.html', {"form": form_new})


def delete_user(request):
    nid = request.GET.get('id')
    models.UsersInfo.objects.filter(id=nid).delete()
    return redirect('/user_info/')