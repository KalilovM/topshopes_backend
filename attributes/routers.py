from rest_framework.routers import SimpleRouter

from .views import AttributesViewset

router = SimpleRouter()
router.register("attributes/", AttributesViewset, basename="attribute_values")
