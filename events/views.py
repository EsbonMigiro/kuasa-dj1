from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Event
from .serializers import EventSerializer
from .permissions import IsStaffOrReadOnly


class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-event_date", "title")
    serializer_class = EventSerializer

    permission_classes = [IsStaffOrReadOnly]


class EventListDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "slug"


class EventEditView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "slug"

    permission_classes = [IsStaffOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Get the new cover image from the request data
            new_cover_image = serializer.validated_data.get('cover_image')

            # Check if the event already has a cover image
            if instance.cover_image and new_cover_image:
                # If it does, delete the old cover image from storage
                default_storage.delete(instance.cover_image.name)

            # Update the event data
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "slug"

    permission_classes = [IsStaffOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the event has a cover image
        if instance.cover_image:
            # If it does, delete the cover image from storage
            default_storage.delete(instance.cover_image.name)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
