from django.shortcuts import render, redirect
import UsersManage.models as models
from UsersManage.utils.forms import PrettyNumModelForm
from UsersManage.utils.pagination import Pagination


def pretty_num_info(request):

    data_dict = {}
    search_data = request.GET.get('search', '')
    if search_data:
        data_dict["mobile__contains"] = search_data  # xxx__contains某个字段包含

    pretty_num_list = models.PrettyNum.objects.filter(**data_dict).order_by("-level")  # -id:按id desc排序
    # for i in range(0, 200):
    #     number = models.PrettyNum(mobile='13333333333', price=100, level=2, status=1)
    #     number.save()

    pagination = Pagination(request, pretty_num_list)

    context = {
        "search_data": search_data,
        "pretty_num_list": pagination.page_queryset,
        "page_string": pagination.html()  # 分页html
    }

    return render(request, "PrettyNumInfo.html", context)


def add_pretty_num(request):
    if request.method == "GET":
        form = PrettyNumModelForm()
        return render(request, "AddPrettyNum.html", {"form": form})

    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty_num_info/')

    return render(request, 'AddPrettyNum.html', {"form": form})


def delete_pretty_num(request):
    nid = request.GET.get('id')
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty_num_info/')
