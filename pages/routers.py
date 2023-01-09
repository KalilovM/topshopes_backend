from rest_framework.routers import SimpleRouter

from .views import PageCategoriesViewSet

router = SimpleRouter()
router.register("pages", PageCategoriesViewSet, basename="page")
