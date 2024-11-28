
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
import random
import uuid
from django.db.utils import IntegrityError
from django.templatetags.static import static

import random
import os
from itertools import chain
from django.conf import settings

from .managers import UserManager


class Country(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=5)



class User(AbstractBaseUser, PermissionsMixin):
    
    UserTypeChoices = (
        ('staff', 'staff'),
        ('manager', 'manager'),
        ('customer', 'customer'),
    )

    def get_path(instance, filename):
        ext = filename.split('.')[-1]  # Get file extension
        file = f"dp-{uuid.uuid4()}.{ext}"  # Generate a random filename
        return f"users/profile/{instance.pk}/{file}"

    def generate_unique_account_id(self):
        """
        Generates a unique 8-digit integer ID with 'SBD' prefix.
        """
        while True:
            unique_id = random.randint(10000, 99999)
            if not User.objects.filter(account_id=f"SBD{unique_id}").exists():
                return "SBD" + str(unique_id)

    username = None

    account_id = models.CharField(max_length=20, unique=True, blank=True, db_index=True)
    user_type = models.CharField(max_length=30, choices=UserTypeChoices, default='customer',blank = True,null = True)
    email = models.EmailField('Email Address', unique=True)
    full_name = models.CharField('Full Name', max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    display_picture = models.FileField(blank=True, null=True, verbose_name='dp', upload_to=get_path)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=30, choices=(
        ("male", "male"),
        ("female", "female"),
        ("prefer not to say", "prefer_not_to_say")
    ), default="prefer_not_to_say")
    country = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=30)
    about = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    phone_number_verified = models.BooleanField(default=False, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    access_permission_level = models.PositiveIntegerField(default=5) #ranges from 1 through 5

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['full_name']

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # Specify fields to monitor
        self.__fields_to_watch_for_changes = ['email', "phone_number"]
        # Set the old values
        for field in self.__fields_to_watch_for_changes:
            setattr(self, '__initial_{}'.format(field), getattr(self, field))

    def has_changed(self, field):
        original = "__initial_{}".format(field)
        return getattr(self, original) != getattr(self, field)

    def save(self, *args, **kwargs):
        try:
            # Check if email was updated so it can be marked unverified
            if self.has_changed("email"):
                self.email_verified = False

            if self.has_changed("phone_number"):
                self.phone_number_verified = False

            if not self.pk or not self.account_id:
                self.account_id = self.generate_unique_account_id()

            super(User, self).save(*args, **kwargs)

        except IntegrityError:
            # Handle the error in case of unique account_id collision
            self.account_id = self.generate_unique_account_id()
            super(User, self).save(*args, **kwargs)

    def __str__(self):
        return (self.full_name or "") + " - " + self.email
    
    @property
    def is_company_staff(self) :
        from myadmin.models import Staff
        try : 
            self.staff
            return self.staff.is_active
        except Staff.DoesNotExist : return False

    def get_permission_level(self) :
        """" 
        permision level used to control what a user can see
        ranges from 1 which is the highest to 5
        1 - can see all(business owner) 
        2  - can see all except sensitive data
        3 - can see some
        """ 
        if self.is_superuser :
            return 1
        if self.is_company_staff : 
            return 3
        return 5
       

        

    @property
    def dp(self):
        default = static("core/img/dp/default-dp.png")
        try:
            return self.display_picture.url or default
        except:
            return default
        
    

    def send_user_email(self):
        pass


class Security(models.Model):

    user = models.OneToOneField(
        get_user_model(), related_name='security', on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Security, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.__str__()


class Language(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=5)


class Setting(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="setting",
        on_delete=models.CASCADE,
    )
    language = models.OneToOneField(
        Language, on_delete=models.PROTECT, null=True)


class NotificationCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Notification(models.Model):
    def get_image_upload_path(instance, file):
        return "notification/{}.{}".format(instance.pk, file.split('.')[1])

    user = models.ForeignKey(
        get_user_model(),
        related_name="notification",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        NotificationCategory, related_name='notifications', on_delete=models.PROTECT)
    title = models.CharField(max_length=30)
    message = models.TextField()
    content_url = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    image = models.FileField(upload_to=get_image_upload_path)

    def __str__(self):
        return self.message[:20]

    class Meta():
        ordering = ['-date']



class CustomPermission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(get_user_model(), related_name="custom_permissions", blank=True)

    def __str__(self):
        return self.name

