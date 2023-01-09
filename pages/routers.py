from rest_framework.routers import SimpleRouter

from .views import PageCategoriesViewSet, PageViewSet

router = SimpleRouter()
router.register("pages/categories", PageCategoriesViewSet, basename="page-category")
router.register("pages", PageViewSet, basename="page")
