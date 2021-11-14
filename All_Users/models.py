from django.db import models
import time
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def create_user(self, Phone,First_Name,Last_Name, password=None,is_staff=False,is_admin=False,is_active=True):

        if not Phone and not password and not First_Name and not Last_Name:
            raise ValueError("Field not Provided")
        user = self.model(Phone=Phone)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.First_Name = First_Name
        user.Last_Name = Last_Name
        user.save(using=self._db)
        return user
 
    def create_staffuser(self, Phone,First_Name,Last_Name, password):

        user = self.create_user(
            Phone,
            First_Name,
            Last_Name,
            password=password,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, Phone,First_Name,Last_Name, password):

        user = self.create_user(
            Phone,
            First_Name,
            Last_Name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    Phone = models.CharField(max_length=10, blank=False, null=False,unique=True)
    First_Name = models.CharField(max_length=50,blank=False, null=False)
    Last_Name = models.CharField(max_length=50,blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    USERNAME_FIELD = 'Phone'
    REQUIRED_FIELDS = ['First_Name','Last_Name'] 

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.First_Name} {self.Last_Name}"

    def get_phone(self):
        return f"{self.Phone}"

    def __str__(self):             
        return f"{self.First_Name} {self.Last_Name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Profile(models.Model):
    Phone = models.CharField(max_length=10, blank=False, null=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    date = models.FloatField(default= time.time(), blank=False, null=False)
    First_Name = models.CharField(max_length=50,blank=False, null=False)
    Last_Name = models.CharField(max_length=50,blank=False, null=False)
    is_validate = models.BooleanField(default=False,null=True,blank=True)
    video = models.CharField(max_length=500,null=True,blank=True)
    is_video_validated = models.BooleanField(default=False)
    user = models.ManyToManyField(User)
    request_receive = models.ManyToManyField(User,related_name="request_receive")
    request_sent = models.ManyToManyField(User,related_name="request_sent")
    bio = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to="Profile_pics", null=True,blank=True,default='images.png')
    is_private = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.Phone}"
    