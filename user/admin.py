from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from user.models import User


class UserAdmins(UserAdmin):
    list_display = ('username', 'email', 'last_login', 'date_joined', 'sex', 'is_active')
    list_display_links = ('username',)
    search_fields = ('username', 'email','date_joined')
    list_filter = ('sex', 'last_login', 'date_joined')
    list_editable = ('sex', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'sex', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'birth_date')}),
        (_('More info'), {'fields': ( 'location','img', 'background_img','country_f', 'region_f', 'city_f')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )



admin.site.register(User, UserAdmins)
#admin.site.register(User, UserMoreAdmin)
