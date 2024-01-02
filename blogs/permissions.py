from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the blog, comment, or reply
        if hasattr(obj, "author"):  # Checking for Blog model
            if obj.author == request.user:
                return True
            # Allow superuser to delete blogs
            if request.user.is_superuser:
                return True
        elif hasattr(obj, "commenter"):  # Checking for Comment model
            return obj.commenter == request.user
        elif hasattr(obj, "replier"):  # Checking for CommentReply model
            return obj.replier == request.user

        # If the object doesn't have an author, commenter, or replier, deny
        # permission
        return False
