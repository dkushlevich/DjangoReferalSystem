from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SignUpView, TokenView, UserViewSet

router_v1 = DefaultRouter()

router_v1.register("users", UserViewSet, basename="user")

auth_patterns = [
    path("signup/", SignUpView.as_view()),
    path("token/", TokenView.as_view()),
]

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/", include(auth_patterns)),
]
