import os
from uuid import uuid4

import django.utils.timezone
from django.db import models


# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'media/Products'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Book(models.Model):
    title = models.CharField('نام کتاب', max_length=60)

    description = models.TextField('توضیحات', help_text="product description", null=True, blank=True)

    product_image = models.ImageField('تصویر', upload_to=path_and_rename, blank=True, null=True)

    price = models.DecimalField(default=10000, decimal_places=2, max_digits=13, verbose_name='قیمت')

    # comment = models.CharField(max_length=300, null=True)
    SORT_CHOICE = ((1, 'مذهبی'), (2, 'رمان'), (3, 'درسی'), (4, 'علمی'))
    genre = models.IntegerField('دسته بندی', choices=SORT_CHOICE, null=False, blank=True, default=None)

    condition = models.BooleanField('وضعیت', choices=((0, 'موجود'), (1, 'نا موجود')))
    author = models.CharField(max_length=120, verbose_name="ناشر", default='')
    author_id = models.DecimalField(default=None, decimal_places=0, max_digits=20)
    publish_date = models.DateField('تاریخ انتشار', default=django.utils.timezone.now)

    def __str__(self):
        return self.title
