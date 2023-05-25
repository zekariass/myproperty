from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.core.exceptions import ValidationError

from apps.users import models
# Register your models here.

class MypropertyUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = models.MypropertyUser
        fields = "__all__"

    def clean_password2(self):
        """Check if the two passowords match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password does not match!")
        return password2
    
    def save(self, commit=True):
        """Save the user with hashed password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class MypropertyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = models.MypropertyUser
        fields = "__all__"


class MypropertyUserAdmin(UserAdmin):
    form = MypropertyUserChangeForm
    add_form = MypropertyUserCreationForm
    list_display = ["id", "first_name", "last_name", "email", "is_superuser", "is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "middle_name", "last_name", "groups"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "is_active", "user_permissions", "roles"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide", "extrapretty"],
                "fields": ["email", "password1", "password2"],
            }
        ),
        (
         "Personal Information",
            {
                "classes": ["wide", "extrapretty"],
                "fields": ["groups", "first_name", "middle_name", "last_name"],
            }
        ),
        (
         "Permissions",
            {
                "classes": ["wide", "extrapretty"],
                "fields": ["is_superuser", "is_staff", "is_active", "user_permissions", "roles"],
            }
        ),
    ]


    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ("roles", "groups", "user_permissions")


admin.site.register(models.MypropertyUser, MypropertyUserAdmin)

class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ("permissions",)

admin.site.register(models.Role, RoleAdmin)
admin.site.register(Permission)