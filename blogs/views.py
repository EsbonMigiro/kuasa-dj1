from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import (
    Blog,
    Comment,
    CommentReply,
    Upvote,
    CommentUpvote,
    CommentReplyUpvote,
)
from .serializers import (
    BlogSerializer,
    BlogDetailSerializer,
    CommentSerializer,
    CommentReplySerializer,
    CommentUpvoteSerializer,
    CommentReplyUpvoteSerializer,
    UpvoteSerializer,
)
from .permissions import IsOwnerOrReadOnly


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by("-created_at", "title")
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlogPageView(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        blog.views += 1
        blog.save()
        return Response({"views": blog.views}, status=status.HTTP_200_OK)


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        blog = self.get_object()

        # Access the 'cover_image' data from the request
        cover_image = self.request.data.get("cover_image", None)

        # Check if the cover image has been updated or removed
        if cover_image is not None:
            # Check if there was a cover image already, and delete it if exists
            if blog.cover_image:
                # Delete the existing cover image
                blog.cover_image.delete(save=False)

        # Perform the update with serializer
        serializer.save()

    def perform_destroy(self, instance):
        # Delete the cover image if it exists before deleting the blog
        if instance.cover_image:
            instance.cover_image.delete(save=False)

        instance.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]


class CommentReplyListCreateView(generics.ListCreateAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer

    def perform_create(self, serializer):
        serializer.save(replier=self.request.user)


class CommentReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]


class CommentUpvoteCreateView(generics.CreateAPIView):
    queryset = CommentUpvote.objects.all()
    serializer_class = CommentUpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(upvoted_by=self.request.user)


class CommentUpvoteDetailView(generics.DestroyAPIView):
    queryset = CommentUpvote.objects.all()
    serializer_class = CommentUpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        upvoted_by = self.request.user
        comment = kwargs.get("pk")

        try:
            comment_upvote = CommentUpvote.objects.filter(
                upvoted_by=upvoted_by, comment=comment
            )

        except CommentUpvote.DoesNotExist:
            return Response({"error": "Comment upvote not found"},
                            status=status.HTTP_404_NOT_FOUND)

        comment_upvote.delete()
        return Response("Comment upvote removed successfully", status=204)


class CommentReplyUpvoteCreateView(generics.CreateAPIView):
    queryset = CommentReplyUpvote.objects.all()
    serializer_class = CommentReplyUpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(upvoted_by=self.request.user)


class CommentReplyUpvoteDetailView(generics.DestroyAPIView):
    queryset = CommentReplyUpvote.objects.all()
    serializer_class = CommentReplyUpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        upvoted_by = self.request.user
        reply = kwargs.get("pk")

        try:
            reply_upvote = CommentReplyUpvote.objects.filter(
                upvoted_by=upvoted_by, reply=reply
            )
        except CommentReplyUpvote.DoesNotExist:
            return Response({"error": "Reply upvote not found"},
                            status=status.HTTP_404_NOT_FOUND)

        reply_upvote.delete()
        return Response("Reply upvote removed successfully", status=204)


class UpvoteCreateView(generics.CreateAPIView):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(upvoted_by=self.request.user)


class UpvoteDetailView(generics.DestroyAPIView):
    queryset = Upvote.objects.all()
    serializer_class = UpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        upvoted_by = self.request.user
        post = kwargs.get("pk")

        try:
            upvote = Upvote.objects.filter(upvoted_by=upvoted_by, post=post)
        except Upvote.DoesNotExist:
            return Response({"error": "Post upvote not found"},
                            status=status.HTTP_404_NOT_FOUND)

        upvote.delete()
        return Response("Post upvote removed successfully", status=204)
