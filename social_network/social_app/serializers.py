from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FriendRequest


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            firstname=validated_data["firstname"],
            lastname=validated_data["lastname"],
        )
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_full_name = serializers.SerializerMethodField()
    to_user_full_name = serializers.SerializerMethodField()
    from_user_name = serializers.SerializerMethodField()
    to_user_name = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = "__all__"

    def get_from_user_full_name(self, obj):
        return f"{obj.from_user.first_name} {obj.from_user.last_name}"

    def get_to_user_full_name(self, obj):
        return f"{obj.to_user.first_name} {obj.to_user.last_name}"

    def get_from_user_name(self, obj):
        return obj.from_user.username

    def get_to_user_name(self, obj):
        return obj.to_user.username
