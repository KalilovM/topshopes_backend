from rest_framework import routers

from head.views import (
    AdminBrandTypeViewSet,
    AdminBrandViewSet,
    AdminCategoryViewSet,
    AdminProductViewSet,
    AdminShopViewSet,
    AdminUsersViewSet,
    AdminPostViewSet,
    AdminPageNavigationCategoryViewSet,
    AdminPageNavigationViewSet,
    AdminPageViewSet,
)

router = routers.SimpleRouter()
router.register(r"users", AdminUsersViewSet)
router.register(r"shops", AdminShopViewSet)
router.register(r"categories", AdminCategoryViewSet)
router.register(r"brand/type", AdminBrandTypeViewSet)
router.register(r"brand", AdminBrandViewSet)
router.register(r"products", AdminProductViewSet)
router.register(r"posts", AdminPostViewSet)
router.register(r"pages/navigations/categories", AdminPageNavigationCategoryViewSet)
router.register(r"pages/navigations", AdminPageNavigationViewSet)
router.register(r"pages", AdminPageViewSet)
