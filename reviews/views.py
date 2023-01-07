from rest_framework import mixins, viewsets
from rest_framework import permissions
from .models import Review
from .serializers import CreateReviewSerializer, ReviewSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    description="Review viewset to get all reviews",
    request=CreateReviewSerializer,
    responses={201: ReviewSerializer},
    tags=["Reviews"],
)
class ReviewViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset to get current product reviews
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Returns only current product reviews
        """
        return Review.objects.filter(product=self.kwargs["product_pk"])

    def perform_create(self, serializer):
        """
        On create review set user to current user
        """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateReviewSerializer
        return ReviewSerializer
