from rest_framework import routers

from head.views import (
    AdminBrandTypeViewSet,
    AdminBrandViewSet,
    AdminCategoryViewSet,
    AdminPageCategoryViewSet,
    AdminPageViewSet,
    AdminPostViewSet,
    AdminProductVariantViewSet,
    AdminProductViewSet,
    AdminShopViewSet,
    AdminSliderViewSet,
    AdminSlideViewSet,
    AdminUsersViewSet,
    AdminAttributesViewSet
)

router = routers.SimpleRouter()
router.register(r"users", AdminUsersViewSet)
router.register(r"shops", AdminShopViewSet)
router.register(r"categories", AdminCategoryViewSet)
router.register(r"brand/type", AdminBrandTypeViewSet)
router.register(r"brand", AdminBrandViewSet)
router.register(r"products/variants", AdminProductVariantViewSet)
router.register(r"products", AdminProductViewSet,basename="products")
router.register(r"posts", AdminPostViewSet)
router.register(r"page/categories", AdminPageCategoryViewSet)
router.register(r"pages", AdminPageViewSet)
router.register(r"sliders/slides", AdminSlideViewSet)
router.register(r"sliders", AdminSliderViewSet)
router.register(r"attributes", AdminAttributesViewSet)
