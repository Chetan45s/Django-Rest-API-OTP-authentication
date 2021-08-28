from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User,Profile

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm  # Update View
    add_form = UserAdminCreationForm # Create View

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','Phone', 'admin')
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('Phone', 'password')}),
        ('Personal info', {'fields': ('First_Name','Last_Name')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id','Phone', 'password1', 'password2')}
        ),
    )
    search_fields = ('Phone','First_Name','Last_Name')
    ordering = ('Phone',)
    filter_horizontal = ()

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)