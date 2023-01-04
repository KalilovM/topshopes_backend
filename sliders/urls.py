from django.urls import path

from .views import SliderViewSet

urlpatterns = [
    path("slider/<slug:slug>", SliderViewSet.as_view({"get": "retrieve"})),
]
