from dh_index.apps.user.serializers import (
    UserHoldingsSerializers, UserHoldingsCreateSerializer, UserHoldingsUpdateSerializer, serializers
)
from dh_index.apps.user.views_container import (
    swagger_auto_schema, openapi, permissions, mixins,
    LimitOffsetPagination, GenericViewSet, MultiPartParser, FormParser, AppStatus, Response, UserHoldings
)


class UserHoldingsViewSet(GenericViewSet, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = UserHoldings.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserHoldingsCreateSerializer
        if self.request.method == 'PUT':
            return UserHoldingsUpdateSerializer
        return UserHoldingsSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        name = self.request.query_params.get("stock_code", None)
        queryset = UserHoldings.objects.filter(user=user)
        if name:
            queryset = queryset.filter(stock_code__icontains=name)

        queryset = queryset.order_by("-created_at")
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="stock_code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def get_object(self):
        author_id = self.kwargs['pk']
        author = UserHoldings.objects.filter(id=author_id).first()
        if not author:
            raise serializers.ValidationError(AppStatus.INVALID_ID.message)
        return author

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(AppStatus.SUCCESS.message)

