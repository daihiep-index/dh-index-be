from dh_index.apps.user.models import UserPortfolio
from dh_index.apps.user.serializers_container import serializers


class UserPortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'


class UserPortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = ['name', 'description']

    def create(self, validated_data):
        current_user = self.context['request'].user
        validated_data['user'] = current_user
        user_holdings = UserPortfolio.objects.create(**validated_data)
        return user_holdings


class UserPortfolioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = ['name', 'description']

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
