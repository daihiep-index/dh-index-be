from dh_index.apps.user.models import User
from dh_index.apps.user.serializers_container import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}, 'verify_code': {'write_only': True}}
