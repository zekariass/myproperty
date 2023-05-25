from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                        BaseUserManager, 
                                        Group, 
                                        PermissionsMixin, 
                                        Permission)
from django.utils import timezone
from django.contrib import auth
from django.conf import settings

class Role(models.Model):
    """User roles for specific group"""
    name = models.CharField(verbose_name="Role Name", max_length=255)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, 
                              verbose_name = "User group this role belongs  to", 
                              related_name="role_set",
                              related_query_name="role",
                              on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, 
                                         help_text="Permissions specific to this user!", 
                                         related_name="role_set",
                                         related_query_name="role",
                                         blank=True)
    added_on = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Role: {self.name}, User group: {self.group}"


class MypropertyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """Create normal user"""
        if not email:
            raise ValueError('You must provide email address!')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print("==============>>>>>>>>>HEYYYY NOOP!!!")

        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """Create super user"""

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True for superuser')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for superuser')
        
        print("==============>>>>>>>>>HEYYYY SUPER!!!")

        return self.create_user(email, first_name, last_name, password, **extra_fields)
    

 
# A helper function to get permissions from supported backend for the current user.
# for a specific object if object is not None. Othersise it return all permissions 
# the user has based on from_name param which can be user, group or role
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions
   

class MypropertyPermissionMixin:
   
    def get_role_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        roles. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "role")

class MypropertyUser(AbstractBaseUser, 
                     PermissionsMixin,
                     MypropertyPermissionMixin
                     ):
    """
    Custom user model which replaces built is User model
    """
    first_name = models.CharField(max_length=50, blank=False, null=False)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(verbose_name='email address', unique=True, blank=False, null=False)
    # group = models.ForeignKey(Group, related_name='users', related_query_name='user',
    #                                  null=True, blank=True, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, 
                                   verbose_name="User Roles", 
                                   related_name="user_set",
                                   related_query_name="user",
                                   blank=True)
    is_active = models.BooleanField(default=True)
    # is_blocked = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(editable=False, null=True)
    registered_on = models.DateTimeField(default=timezone.now, editable=False)

    objects = MypropertyUserManager()

    # print("===========================>>>HOHO!")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "User"
        ordering = ["-registered_on"]

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.email)

    def get_full_name(self):
        return '%s %s %s' % (self.first_name, self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    # def has_perm(self, perm, obj=None):
    #     '''Check if the user has specific permission'''
    #     if not self.is_active and not self.is_blocked:
    #         return False
    #     else:
    #         return True
    
    # def has_module_perms(self, app_label):
    #     '''Check if the user has module level permission'''
    #     if not self.is_active and not self.is_blocked:
    #         return False
    #     else:
    #         return True

