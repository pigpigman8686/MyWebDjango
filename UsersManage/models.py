from django.db import models

# Create your models here.


class Department(models.Model):
    """部门表"""

    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class UsersInfo(models.Model):
    """用户表"""

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


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)

    status_choices = (
        (1, "已占用"),
        (0, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)
