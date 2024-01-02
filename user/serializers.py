from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "email",
            "alternative_email",
            "registration_no",
            "phone_number",
            "year_of_study",
        )

    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password", None)
        password = validated_data.get("password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LeadershipUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "leadership_role",
            "linkedin",
            "profile_image",
        )


class UserListSerializer(serializers.ModelSerializer):
    is_member = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "first_name",
            "last_name",
            "email",
            "alternative_email",
            "registration_no",
            "profile_image",
            "phone_number",
            "year_of_study",
            "leadership_role",
            "linkedin",
            "is_member",
            "is_corporate_member",
            "bio",
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    is_member = serializers.ReadOnlyField()
    is_corporate_member = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "first_name",
            "last_name",
            "email",
            "alternative_email",
            "registration_no",
            "phone_number",
            "year_of_study",
            "leadership_role",
            "linkedin",
            "profile_image",
            "is_member",
            "is_staff",
            "is_corporate_member",
            "bio",
        )

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(
                validated_data["password"])

        instance = super().update(instance, validated_data)
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:  # noqa: F841
            raise AuthenticationFailed("The reset link is invalid", 401)
        return super().validate(attrs)
