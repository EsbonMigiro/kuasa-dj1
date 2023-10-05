from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    LeadershipUserSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer,
    EmailVerificationSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import (
    MultiPartParser, FormParser, FileUploadParser
)
from django.db.models import Case, Value, When, IntegerField

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from .utils import Util
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data["username"])
            if not user.is_verified:
                current_site = get_current_site(request)
                relative_link = reverse("verify-email")
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                absurl = f"http://{current_site.domain}{relative_link}?token={token}"

                email_body = (
                    "Hi "
                    + user.first_name
                    + " "
                    + user.last_name
                    + ", \n"
                    + " \n Click the link below to verify your email \n"
                    + absurl
                    + "\n"
                    + "\n Your username is: "
                    + user.username
                    + " in case you forgot. \n \n"
                    + "You received this message because you signed up for kuasa website. \n"
                    + "KUASA \n"
                    + "Kenyatta University Aerospace Engineering Students Association."
                )

                data = {
                    "email_body": email_body,
                    "to_email": user.email,
                    "email_subject": "Verify your email",
                }

                Util.send_email(data)

                return Response(
                    {"message": "A verification email has been sent."},
                    status=status.HTTP_200_OK,
                )

        return response


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        refresh = RefreshToken.for_user(user)

        # Create a verification token and send it via email
        token = str(refresh.access_token)
        current_site = get_current_site(request)
        relative_link = reverse("verify-email")
        absurl = f"http://{current_site.domain}{relative_link}?token={token}"

        email_body = (
            "Hi "
            + user.first_name
            + " "
            + user.last_name
            + ", \n"
            + " \n Click the link below to verify your email \n"
            + absurl
            + "\n"
            + "\n You are username is: "
            + user.username
            + " incase you forgot. \n \n"
            + "You received this message because you sign up for kuasa website. \n"
            + "KUASA \n"
            + "Kenyatta University Aerospace Engineering Students Association."
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(TemplateView):
    serializer_class = EmailVerificationSerializer
    template_name = "user/verification_response.html"

    def get(self, request):
        context = {}
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                context["verification_status"] = "Successfully activated"
            else:
                context["verification_status"] = "Already verified"

        except jwt.ExpiredSignatureError as identifier:
            context["verification_status"] = "Activation Expired"
        except jwt.exceptions.DecodeError as identifier:
            context["verification_status"] = "Invalid token"
        return render(request, self.template_name, context)



class LeadershipUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeadershipUserSerializer

    def get_queryset(self):
        # Get the queryset and order it based on the custom order
        queryset = User.objects.exclude(leadership_role__isnull=True).order_by(
            Case(
                *[When(leadership_role=choice[0], then=Value(order)) for order,
                    choice in enumerate(User.LEADERSHIP_CHOICES)],
                default=Value(len(User.LEADERSHIP_CHOICES)),
                output_field=IntegerField()
            )
        )

        return queryset


class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('first_name', 'last_name')
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserProfileView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileUpdateSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileUpdateSerializer(
            user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def change_password(self, request):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_new_password = serializer.validated_data.get(
                'confirm_new_password')

            if not user.check_password(old_password):
                return Response(
                    {'detail': 'Old password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response(
                    {'detail': 'New passwords do not match.'},
                    status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response(
                {'detail': 'Password successfully changed.'},
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class UserProfileImageView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def update_profile_image(self, user, image):
        user.profile_image = image
        user.save()
        return user.profile_image.url

    def upload_image(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if the 'profile_image' key is in the request data
            if 'profile_image' in request.data:
                image = request.data['profile_image']
                self.update_profile_image(request.user, image)

            return Response(
                {'profile_image': request.user.profile_image.url,
                    'detail': 'Profile image updated successfully.'},
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def remove_image(self, request):
        user = request.user
        if user.profile_image:
            user.profile_image.delete()
            user.profile_image = None
            user.save()
            return Response({'detail': 'Profile image removed successfully.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No profile image to remove.'},
                            status=status.HTTP_400_BAD_REQUEST)
