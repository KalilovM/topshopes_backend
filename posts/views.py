from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema

from posts.models import Post
from posts.serializers import PostSerializer


@extend_schema(
    description="Post viewset for list and retrieve",
    responses={200: PostSerializer},
    tags=["All"],
)
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Post viewset for list and retrieve
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
