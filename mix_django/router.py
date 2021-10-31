from rest_framework import routers
from catalog import viewset as categories
from user import viewset as user
from product import viewset as products

router_catalog = routers.DefaultRouter()
router_user = routers.DefaultRouter()
router_product = routers.DefaultRouter()


# user
router_user.register(r'user/cart', user.CartsViewSet)

# categories
router_catalog.register(r'categories', categories.CategoriesListViewSet)

# products
router_product.register(r'product', products.ProductsListViewSet)
router_product.register(r'characteristics/values', products.CharacteristicsByCatListViewSet)
router_product.register(r'characteristics', products.CharacteristicsListViewSet)
