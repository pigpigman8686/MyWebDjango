from django.shortcuts import render, redirect
import UsersManage.models as models
from UsersManage.utils.pagination import Pagination


def depart_info(request):
    depart_list = models.Department.objects.all().order_by('id')

    pagination = Pagination(request, depart_list)

    context = {
        "depart_list": pagination.page_queryset,
        "page_string": pagination.html()
    }
    return render(request, 'DepartInfo.html', context)


def add_depart(request):
    if request.method == "GET":
        return render(request, 'AddDepart.html')

    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart_info/')


def edit_depart(request, nid):
    if request.method == "GET":
        row_data = models.Department.objects.filter(id=nid).first()
        return render(request, 'EditDepart.html', {"row_data": row_data})

    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart_info/')


def delete_depart(request):
    nid = request.GET.get('id')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart_info/')
