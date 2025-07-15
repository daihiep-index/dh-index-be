from dh_index.apps.user.routers import *

from dh_index.apps.user.views import (
    UserDetailViewSet,
)

urlpatterns = [
    path('user/me/', UserDetailViewSet.as_view(), name='user-detail'),
]
