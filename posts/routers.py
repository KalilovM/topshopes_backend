from rest_framework import routers

from posts.views import PostViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
