from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        if self.instance and self.instance.creator != user:
            raise serializers.ValidationError("Вы не можете изменять чужие объявления")

        # TODO: добавьте требуемую валидацию
        # Проверка лимита объявлений (не более 3 открытых)
        if data.get('status') == 'OPEN' or (self.instance and self.instance.status == 'OPEN'):
            open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_ads_count >= 3 and (not self.instance or self.instance.status != 'OPEN'):
                raise serializers.ValidationError("Нельзя иметь более 3 открытых объявлений")

        return data
