from django.db import models
from extensions.utils import jalali_converter
from django.utils.html import format_html
from Account.models import User
from django.urls import reverse
from datetime import datetime

# --------------- comment -------------------
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# managers
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="Children", verbose_name="زیر دسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته‌بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی‌پی")

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "آدرس آی پی"
        verbose_name_plural = "آدرس های آی پی"


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
        ('i', 'در حال بررسی'),  # investigation
        ('b', 'برگشت داده شده'),  # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="articles",
                               verbose_name="نویسنده")
    title = models.CharField(max_length=250, verbose_name='عنوان')
    slug = models.SlugField(max_length=500, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, verbose_name="دسته بندی", related_name="article")
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to="", verbose_name='تصویر')
    publish = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, blank=True, related_name="hits",
                                  verbose_name="بازدیدها")


    def get_absolute_url(self):
        return reverse("account:home")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'
        ordering = ['-publish']

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = "زمان انتشار"

    def category_published(self):
        return self.category.filter(status=True)

    def image_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.image.url))

    image_tag.short_description = "تصویر"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category_published()])

    category_to_str.short_description = "دسته بندی"

    objects = ArticleManager()

