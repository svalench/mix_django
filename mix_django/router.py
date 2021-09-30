from rest_framework import routers
from catalog import viewset as categories
from user import viewset as user

router_catalog = routers.DefaultRouter()
router_user = routers.DefaultRouter()


# user

# categories
router_catalog.register(r'categories', categories.CategoriesListViewSet)

