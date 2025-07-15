from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path, include
from dh_index.apps.user.routers import register


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='login_api'),
    path("auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # path('', include(stadium.router.urls)),
    # path('', include(soccer_field.router.urls)),
    path('', include('dh_index.apps.user.routers.user')),
    path('', include('dh_index.apps.user.routers.register')),
]
