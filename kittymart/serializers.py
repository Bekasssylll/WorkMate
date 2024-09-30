from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from kittymart import models
from kittymart.models import Kitten, Rating


class KittenSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Kitten
        fields = ['id', 'color', 'age_in_months', 'description', 'breed','average_rating']
        read_only_fields = ['user']

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('score'))['score__avg'] or 0


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'kitten', 'user', 'score']
