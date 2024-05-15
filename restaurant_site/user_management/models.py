from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator



# This class is created to modify the authentication requirements
class CustomUserManager(BaseUserManager):
    def create_user(self, emp_id, name, password):
        if not emp_id:
            raise ValueError('An employee number is needed.')
        if not name:
            raise ValueError('Please enter your full name.')
        if not password:
            raise ValueError('A password is needed.')
        
        user = self.model(emp_id=emp_id, name=name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, emp_id, name, password):
        if not emp_id:
            raise ValueError('An employee number is needed.')
        if not name:
            raise ValueError('Please enter your full name.')
        if not password:
            raise ValueError('A password is needed.')
        
        user = self.create_user(self, emp_id, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# Custom user class 
class User(AbstractBaseUser, PermissionsMixin):
    emp_id = models.CharField(primary_key=True, unique=True, null=False, max_length=4, validators=[RegexValidator(regex='^\d{4}$', message='Length has to be 4', code='nomatch')])
    name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
  
    USERNAME_FIELD = 'emp_id'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
    
    def __str__(self):
        return f"EMP_ID: {self.emp_id}, NAME: {self.name}"
    