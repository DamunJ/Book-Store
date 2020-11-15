import os
from sys import path
from uuid import uuid4

from django.db import models
from django.utils import timezone


def path_and_rename(instance, filename, folder):
    """
    Function for rename the uploaded files
    """
    upload_to = 'images/{}'.format(folder)
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)

    # return the whole path to the file
    return os.path.join(upload_to, filename)

    def wrapper(instance, filename, folder):
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


class Author(models.Model):
    """
    Represents an Author
    """

    def upload(self, instance, filename):
        return path_and_rename(instance, filename, 'Author')

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField(choices=GENDER_CHOICES)

    birthday = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to=upload, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Publisher(models.Model):
    """
    Represents a Publisher
    """
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Represents a Genre of books
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a Book
    """

    def upload(instance, filename):
        return path_and_rename(instance, filename, 'Books')

    title = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=20, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    translator = models.ForeignKey(Author, related_name="translator", on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)

    # Language
    English = 1
    Persian = 2
    LANGUAGE_CHOICES = ((English, 'انگلیسی'), (Persian, 'فارسی'))
    language = models.IntegerField(choices=LANGUAGE_CHOICES, default=Persian)

    # Genre
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    # Cover
    cover = models.ImageField(upload_to=upload, blank=True, null=True)

    # Condition
    SALE_OPEN = 1
    SALE_CLOSE = 2
    SALE_NOT_STARTED = 3
    SALE_CHOICES = ((SALE_OPEN, 'درحال فروش'), (SALE_CLOSE, 'فروش بسته شده'), (SALE_NOT_STARTED, 'فروش به زودی'))
    condition = models.IntegerField(choices=SALE_CHOICES)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    """
    Represents an Item of Order
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)


class Order(models.Model):
    """
    Represents an Order
    """
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    status_choices = (
        (STATUS_SHOPPING, 'در حال خرید'),
        (STATUS_SUBMITTED, 'ثبت شده'),
        (STATUS_CANCELED, 'لغو شده')
    )

    customer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    order_time = models.DateTimeField(null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=status_choices)

    @staticmethod
    def initiate(customer):
        for order in Order.objects.filter(customer=customer):
            if order.status == Order.STATUS_SHOPPING:
                raise PermissionError('شما یک سفارش فعال دارید!')
        order = Order()
        order.customer = customer
        order.status = Order.STATUS_SHOPPING
        order.save()

    def add_book(self, book):
        order_item = OrderItem()
        order_item.order = self
        order_item.book = book
        order_item.save()
        self.total_price += book.price
        self.save()
        return True

    def remove_book(self, book):
        OrderItem.objects.get(order=Order.objects.get(pk=self.pk), book=book).delete()
        self.total_price -= book.price
        self.save()
        return True

    def submit(self):
        # Check Permissions and Values
        if self.status != self.STATUS_SHOPPING:
            raise PermissionError('شما نمی‌توانید این سفارش را ثبت کنید')
        if len(OrderItem.objects.filter(order=self)) > 1:
            raise PermissionError('شما نمی‌توانید یک سفارش خالی را ثبت کنید')
        if self.total_price > self.customer.balance:
            raise ValueError('موجودی کافی نیست!')

        # Update Total Price
        total = 0
        for book in OrderItem.objects.filter(order=self):
            total += book.price
        self.total_price = total

        # spend customer's balance
        self.customer.spend(self.total_price)

        # submit Order
        self.order_time = timezone.now()
        self.status = self.STATUS_SUBMITTED
        self.save()

    def cancel(self):
        if self.status != self.STATUS_SUBMITTED:
            raise PermissionError('شما اجازه لغو سفارش را ندارید!')

        # Cancel order
        self.status = self.STATUS_CANCELED
        self.save()
