import os

from datetime import timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import (viewsets, mixins, status, permissions, generics)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView

from dh_index.apps.user.models import *
from dh_index.apps.utils.constant_status import AppStatus
from dh_index.apps.utils.dynamic_param import DynamicQueryParams
from dh_index.apps.utils.send_mail import sent_mail_verification, TypeEmailEnum
from dh_index.apps.utils.constant_status import Enum

# from dh_index.apps.utils.uts_invalid_value import is_valid_uuid4
# from dh_index.apps.utils.uts_depen import IsAdmin, IsUser, IsAuthenticated
