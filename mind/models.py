
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, number, age, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, number=number, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, number, age, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, number, age, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    CATEGORIES = [
        ("ADMIN", "administrator"),
        ("USER", "user")
    ]
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    number = PhoneNumberField(region='BR')
    age = models.CharField(max_length=2)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number', 'age', 'category']

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return self.title

class reminder(models.Model):
    reminder_name = models.CharField(max_length=30, blank=True)
    reminder_date = models.DateTimeField(auto_now_add=True)
    reminder_content = models.CharField(max_length=500, blank=True, null=True)
    reminder_hour = models.TimeField(blank=False, null=False)



