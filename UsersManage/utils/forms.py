from django import forms
import UsersManage.models as models
from django.core.validators import RegexValidator, ValidationError
from UsersManage.utils.encrypt import md5
from UsersManage.utils.Bootstrap import BootstrapForm, BootstrapModelForm


# -------------------------- ModelForm --------------------------\
class UserModelForm(BootstrapModelForm):
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


class PrettyNumModelForm(BootstrapModelForm):
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


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):  # 钩子方法，form.is_valid()前执行
        pwd = self.cleaned_data.get('password')
        # 返回什么，数据库就保存什么
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')  # 自动调用钩子对应的函数
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError("密码不一致")
        return confirm_pwd


class AdminEditModelForm(BootstrapModelForm):

    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()  # pk:prime key
        if exists:
            raise ValidationError("密码不能与过去的相同")

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))

        if pwd != confirm_pwd:
            raise ValidationError("密码不一致")

        return confirm_pwd


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput
        }


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = [""]
        exclude = ["oid", 'admin']


class UpForm(BootstrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


class UpModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"
