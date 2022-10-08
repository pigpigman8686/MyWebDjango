import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

import UsersManage.models as models
from UsersManage.utils.forms import UserModelForm, TaskModelForm
from UsersManage.utils.pagination import Pagination


def task_info(request):
    queryset_task = models.Task.objects.all().order_by('id')
    pagination = Pagination(request, queryset_task)

    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": pagination.page_queryset,
        "page_string": pagination.html()
    }
    return render(request, 'TaskInfo.html', context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)

    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def add_task(request):
    # {'level': ['1'], 'title': ['sdfsdfsdfsd'], 'detail': ['111'], 'user': ['8']}
    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
