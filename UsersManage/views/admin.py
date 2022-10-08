from django.shortcuts import render, redirect
import UsersManage.models as models
from UsersManage.utils.forms import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from UsersManage.utils.pagination import Pagination


def admin_info(request):
    admin_list = models.Admin.objects.all()

    pagination = Pagination(request, admin_list)

    context = {
        "admin_list": pagination.page_queryset,
        "page_string": pagination.html()
    }
    return render(request, 'AdminInfo.html', context)


def add_admin(request):
    title = "新建管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'AddAdmin.html', {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin_info/')
    return render(request, 'AddAdmin.html', {"form": form, "title": title})


def edit_admin(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin_info/')

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'AddAdmin.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin_info/')
    return render(request, 'AddAdmin.html', {"form": form, "title": title})


def delete_admin(request):
    nid = request.GET.get('id')
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin_info/')


def reset_admin(request, nid):
    row_data = models.Admin.objects.filter(id=nid).first()
    if row_data:
        redirect('/admin_info/')

    title = "重置密码 - {}".format(row_data.username)
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'AddAdmin.html', {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_data)
    if form.is_valid():
        form.save()
        return redirect('/admin_info/')
    return render(request, 'AddAdmin.html', {"form": form, "title": title})

    pass

