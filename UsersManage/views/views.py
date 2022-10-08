from django import forms
from django.shortcuts import render, redirect
from django.core.validators import RegexValidator
import UsersManage.models as models


# from UsersManage.models import UsersInfo, Department

# Create your views here.


def test(request):
    return render(request, 'Navigation.html')

