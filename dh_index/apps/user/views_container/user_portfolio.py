from dh_index.apps.user.serializers import (
    UserPortfolioSerializers, UserPortfolioCreateSerializer, UserPortfolioUpdateSerializer, serializers
)
from dh_index.apps.user.views_container import (
    swagger_auto_schema, openapi, permissions, mixins,
    LimitOffsetPagination, GenericViewSet, MultiPartParser, FormParser, AppStatus, Response, UserPortfolio
)


class UserPortfolioViewSet(GenericViewSet, mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = UserPortfolio.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserPortfolioCreateSerializer
        if self.request.method == 'PUT':
            return UserPortfolioUpdateSerializer
        return UserPortfolioSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        name = self.request.query_params.get("name", None)
        queryset = UserPortfolio.objects.filter(user=user)
        if name:
            queryset = queryset.filter(stock_code__icontains=name)

        queryset = queryset.order_by("-created_at")
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="name", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def get_object(self):
        pk_id = self.kwargs['pk']
        object_ = UserPortfolio.objects.filter(id=pk_id).first()
        if not object_:
            raise serializers.ValidationError(AppStatus.INVALID_ID.message)
        return object_

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(AppStatus.SUCCESS.message)

