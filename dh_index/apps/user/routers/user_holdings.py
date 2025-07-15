from rest_framework import routers
from dh_index.apps.user.routers import *
from dh_index.apps.user.views import (UserHoldingsViewSet)

router = routers.DefaultRouter(trailing_slash=False)
router.register('', UserHoldingsViewSet)

urlpatterns = [
    path("user_holdings/", include(router.urls)),
]
