from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    # Disallow create and edit actions for superusers
    def has_add_permission(self, request):
        return not request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser

    # Restrict delete permission for superusers to delete only one object at a
    # time
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and obj is None:
            return False  # Superuser can't delete multiple objects
        return super().has_delete_permission(request, obj)


admin.site.register(Blog, BlogAdmin)
