from django.urls import path
from .views import (EventListView,
                    EventListDetailView,
                    EventEditView,
                    EventDeleteView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "events/",
        EventListView.as_view(),
        name="event-list"),
    path(
        "events/<slug:slug>/",
        EventListDetailView.as_view(),
        name="event-detail"),
    path(
        "events/edit/<slug:slug>/",
        EventEditView.as_view(),
        name="event-edit"),
    path(
        "events/delete/<slug:slug>/",
        EventDeleteView.as_view(),
        name="event-delete"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
