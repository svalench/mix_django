from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from dynamic_raw_id.admin import DynamicRawIDMixin

from product.models import ProductsImages, Characteristics, CharacteristicValue, FiltersValue, Filters, CardProduct, \
    Product, Units


class UnitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('date_add', 'date_upd')
    list_per_page = 50


class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('date_add', 'date_upd')
    list_per_page = 50


class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'value')
    list_editable = ('value',)
    list_filter = ('date_add', 'date_upd', 'units')
    list_per_page = 50


class FiltersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('date_add', 'date_upd')
    list_per_page = 50


class FiltersValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'units', 'parent', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'value')
    list_editable = ('value', 'units')
    list_filter = ('date_add', 'date_upd', 'units')
    list_per_page = 50


class ProductsImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'date_upd', 'date_add', 'image_')
    list_display_links = ('img', 'id')
    list_filter = ('date_add', 'date_upd')
    readonly_fields = ('image_',)
    list_per_page = 50

    def image_(self, obj):
        return format_html('<img width="50" height="50"  src="{}" />'.format(obj.img.url))


class ProductsImagesInline(admin.TabularInline):
    model = ProductsImages

class ProductInline(admin.StackedInline):
    model = Product

class CardProductAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'image_', 'view_filters_link', 'date_upd', 'date_add')
    list_display_links = ('id', 'date_upd')
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('date_add', 'date_upd')
    readonly_fields = ('image_',)
    dynamic_raw_id_fields  = ("filters","child")
    inlines = [ProductsImagesInline, ProductInline]
    list_per_page = 50

    def image_(self, obj):
        return format_html('<img width="50" height="50"  src="{}" />'.format(obj.img.url))

    def view_filters_link(self, obj):
        count = obj.filters.count()
        url = (
                reverse("admin:product_filtersvalue_changelist")
                + "?"
                + urlencode({"product__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">кол-во фильтров {}</a>', url, count)

    view_filters_link.short_description = "Фильтра"



class ProductAdmin(DynamicRawIDMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'article', 'count', 'weight', 'price', 'date_upd', 'date_add')
    list_display_links = ('id', 'name', 'date_upd')
    search_fields = ('id', 'name', 'count', 'weight', 'price', 'article')
    list_editable = ('count', 'weight', 'price')
    list_filter = ('date_add', 'date_upd', 'characteristics')
    dynamic_raw_id_fields = ('characteristics',)
    list_per_page = 50


admin.site.register(Units, UnitsAdmin)
admin.site.register(Characteristics, CharacteristicsAdmin)
admin.site.register(CharacteristicValue, CharacteristicValueAdmin)
admin.site.register(Filters, FiltersAdmin)
admin.site.register(FiltersValue, FiltersValueAdmin)
admin.site.register(ProductsImages, ProductsImagesAdmin)
admin.site.register(CardProduct, CardProductAdmin)
admin.site.register(Product, ProductAdmin)
