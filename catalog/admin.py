from django.contrib import admin
from django.utils.html import format_html

from catalog.models import FirstCategory, SecondCategory


class FirstCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_', 'img', 'date_upd', 'date_add')
    list_display_links = ('id', 'img', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    readonly_fields = ('image_',)
    list_filter = ('date_add', 'date_upd')
    list_per_page = 50

    def image_(self, obj):
        return format_html('<img width="50" height="50"  src="{}" />'.format(obj.img.url))



class SecondCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'img', 'image_', 'date_upd', 'date_add')
    list_display_links = ('id', 'img', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name', 'parent')
    readonly_fields = ('image_',)
    list_filter = ('date_add', 'date_upd', 'parent')
    list_per_page = 50

    def image_(self, obj):
        return format_html('<img width="50" height="50"  src="{}" />'.format(obj.img.url))


admin.site.register(FirstCategory, FirstCategoryAdmin)
admin.site.register(SecondCategory, SecondCategoryAdmin)