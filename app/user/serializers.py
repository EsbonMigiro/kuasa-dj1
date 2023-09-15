from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'email',
            'alternative_email',
            'registration_no',
            'phone_number',
            'year_of_study')

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        password = validated_data.get('password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create_user(**validated_data)
        return user


class LeadershipUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'first_name',
            'last_name',
            'leadership_role',
            'linkedin',
            'profile_image')


class UserListSerializer(serializers.ModelSerializer):
    is_member = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'alternative_email',
            'registration_no',
            'phone_number',
            'year_of_study',
            'leadership_role',
            'linkedin',
            'is_member',
            'bio')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    is_member = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'alternative_email',
            'registration_no',
            'phone_number',
            'year_of_study',
            'leadership_role',
            'linkedin',
            'profile_image',
            'is_member',
            'bio')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])

        instance = super().update(instance, validated_data)
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
