from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect
import UsersManage.models as models
from UsersManage.utils.forms import LoginForm
from UsersManage.utils.generateCode import check_code


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'Login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 校验验证码
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验账号密码是否正确
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:  # 账号密码错误
            form.add_error("password", "账号或密码错误")
            return render(request, 'login.html', {'form': form})

        # 账号密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存七天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/user_info/')
    return render(request, 'login.html', {"form": form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')
