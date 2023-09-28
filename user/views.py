from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    LeadershipUserSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import (
    MultiPartParser, FormParser, FileUploadParser
)
from django.db.models import Case, Value, When, IntegerField


class UserLoginView(TokenObtainPairView):
    pass


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


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
