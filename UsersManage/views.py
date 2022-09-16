from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
import UsersManage.models as models


# from UsersManage.models import UsersInfo, Department

# Create your views here.


def user_info(request):
    # generate_department()
    user_list = models.UsersInfo.objects.all()
    return render(request, 'UsersInfo.html', {"user_list": user_list})


# -------------------------- ModelForm --------------------------\
class UserModelForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UsersInfo
        fields = ['name', 'password', 'age', 'account', 'gender', 'create_time', 'depart']  # '__all__'
        widgets = {
            # "name": forms.TextInput(attrs={"class": "form-control"}),
            # "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
            # "age": forms.TextInput(attrs={"class": "form-control"),
            "create_time": forms.DateInput(attrs={"type": "date", "class": "form-control"}, format='%Y-%m-%d')  # 日期控件
            # "create_time": forms.DateInput(attrs={"type": "time", "class": "form-control"}, format='%Y-%m-%d')  # 时间控件
        }  # 为组件添加样式

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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


def depart_info(request):
    depart_list = models.Department.objects.all()
    return render(request, 'DepartInfo.html', {"depart_list": depart_list})


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


def pretty_num_info(request):
    pretty_num_list = models.PrettyNum.objects.all().order_by("-level")  # -id:按id desc排序

    return render(request, "PrettyNumInfo.html", {"pretty_num_list": pretty_num_list})


class PrettyNumModelForm(forms.ModelForm):

    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}', "手机号格式错误"),  # 必须以1开头,3-9位第二位的11位数字
                    # RegexValidator(r'^1[3-9]\d{9}', "手机号格式错误")  # 可添加多个正则表达式
                    ]
    )
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']  # '__all__'
        # fields = '__all__'
        # exclude = ['mobile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def add_pretty_num(request):
    if request.method == "GET":
        form = PrettyNumModelForm()
        return render(request, "AddPrettyNum.html", {"form": form})

    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty_num_info/')

    return render(request, 'AddPrettyNum.html', {"form": form})


def test(request):
    return render(request, 'Navigation.html')

