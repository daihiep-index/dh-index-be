from dh_index.apps.user.models import User, UserHoldings
from dh_index.apps.user.serializers_container import serializers


class UserHoldingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserHoldings
        fields = '__all__'


class UserHoldingsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHoldings
        fields = ['stock_code', 'quantity', 'value']

    def create(self, validated_data):
        current_user = self.context['request'].user
        validated_data['user'] = current_user
        user_holdings = UserHoldings.objects.create(**validated_data)
        return user_holdings


class UserHoldingsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHoldings
        fields = ['stock_code', 'quantity', 'value']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
