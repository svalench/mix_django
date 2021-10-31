from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from user.models import User, Carts
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html


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


class CartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_email', 'user_phone', 'date_upd', 'date_add')
    list_display_links = ('id', 'user_name', 'user_email', 'date_upd')
    search_fields = ('id', 'user_name', 'user_email', 'user_phone')
    list_filter = ('date_add', 'date_upd', 'user_email')
    list_per_page = 50

    def view_produts_link(self, obj):
        count = obj.products.all().count()
        url = (
                reverse("admin:product_product_changelist")
                + "?"
                + urlencode({"carts_set__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">кол-во продуктов {}</a>', url, count)


admin.site.register(User, UserAdmins)
admin.site.register(Carts, CartsAdmin)
