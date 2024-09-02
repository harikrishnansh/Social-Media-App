from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=300, blank=False, null=False)
    dob = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True,default=False)

    USERNAME_FIELD = 'email'
    class Meta:
        managed = True
        db_table = 'users'