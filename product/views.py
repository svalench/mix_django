from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product


@api_view(http_method_names=['GET'])
def filter_cats(request):
    """Возвращает только те характеристики которые определены в переданной категории"""
    data = {}
    res = {}
    cat = request.GET.get('category', None)
    if cat is None:
        return Response({"error": 'необходимо передать ключ category в гет параметрах'},
                        status=status.HTTP_400_BAD_REQUEST)
    products = Product.objects.filter(parent__category_id=cat)
    for product in products:
        characteristics = product.characteristics.all()
        for ch in characteristics:
            if ch.parent in res.keys():
                if not ch.id in res[ch.parent]['id_list']:
                    res[ch.parent.id]['values'].append({"value": ch.value, "unit": ch.units.name, 'id': ch.id})
                    res[ch.parent.id]['id_list'].append(ch.id)
            else:
                res[ch.parent.id] = {'name': ch.parent.name,
                                  'id': ch.parent.id,
                                  'id_list': [ch.id],
                                  'values': [{"value": ch.value, "unit": ch.units.name, 'id': ch.id}]
                                  }
    data = [res[i] for i in res]
    return Response(data, status=status.HTTP_200_OK)
