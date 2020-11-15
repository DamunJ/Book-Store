import os
from sys import path
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


def path_and_rename(instance, filename):
    upload_to = 'images/Profiles'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)

    return wrapper


class Profile(models.Model):
    """
    Manages the users' profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='حساب کاربری')

    mobile = models.CharField('تلفن همراه', max_length=11, null=True, blank=True)

    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)

    GENDER_CHOICES = ((1, 'مرد'), (2, 'زن'))
    gender = models.IntegerField('جنسیت', choices=GENDER_CHOICES, null=True, blank=True)

    profile_image = models.ImageField('تصویر', upload_to=path_and_rename, blank=True, null=True)

    balance = models.IntegerField('اعتبار', default=0)

    def __str__(self):
        return self.user.username

    def get_balance_display(self):
        return '{} تومان'.format(self.balance)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True
