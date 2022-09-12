from django.db import models

# Create your models here.


class Department(models.Model):

    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class UsersInfo(models.Model):

    name = models.CharField(verbose_name='姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    gender_choices = (
        (1, '男'),
        (2, '女'),
        (3, '未知')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=3)
    create_time = models.DateTimeField(verbose_name='入职时间')
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)


