from rest_framework import permissions
from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Post viewset for list and retrieve
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
