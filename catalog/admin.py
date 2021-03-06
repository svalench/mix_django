from django.contrib import admin
from django.utils.html import format_html

from catalog.models import FirstCategory, SecondCategory, DocumentsCard


class ChildCatInline(admin.TabularInline):
    model = SecondCategory

class FirstCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_', 'img', 'date_upd', 'date_add')
    list_display_links = ('id', 'img', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    readonly_fields = ('image_',)
    list_filter = ('date_add', 'date_upd')
    inlines = [ChildCatInline]
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


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'date_upd', 'date_add')
    list_display_links = ('id', 'parent', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('date_add', 'date_upd', 'parent')
    list_per_page = 50



admin.site.register(FirstCategory, FirstCategoryAdmin)
admin.site.register(SecondCategory, SecondCategoryAdmin)
admin.site.register(DocumentsCard, CertificateAdmin)