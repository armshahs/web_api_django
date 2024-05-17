from django.contrib import admin
from .models import User
from django.contrib.auth.hashers import make_password

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # Hash the password before saving
        obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
