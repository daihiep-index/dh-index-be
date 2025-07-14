from dh_index.apps.user.routers import *

from dh_index.apps.user.views import (
    RegisterViewSet,
    VerifyCodeViewSet,
)

urlpatterns = [
    path('auth/register/', RegisterViewSet.as_view(), name='register-user'),
    path('auth/veryfi_code/', VerifyCodeViewSet.as_view(), name='verify-code'),

]