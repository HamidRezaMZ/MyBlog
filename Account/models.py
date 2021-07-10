from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name="ایمیل")
    is_author = models.BooleanField(default=False, verbose_name="وضغیت نویسندگی")
    special_user = models.DateTimeField(default=datetime.now(), verbose_name="کاربر ویژه تا")

    def is_special_user(self):
        if self.special_user > datetime.now():

            return True
        else:
            return False

    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کاربر ویژه"
