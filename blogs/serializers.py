from rest_framework import serializers
from .models import (
    Blog,
    Comment,
    CommentReply,
    Upvote,
    CommentUpvote,
    CommentReplyUpvote,
)


class CommentUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUpvote
        fields = "__all__"


class CommentReplyUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReplyUpvote
        fields = "__all__"


class CommentReplySerializer(serializers.ModelSerializer):
    upvotes = CommentReplyUpvoteSerializer(many=True, read_only=True)

    class Meta:
        model = CommentReply
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    replies = CommentReplySerializer(many=True, read_only=True)
    upvotes = CommentUpvoteSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    upvotes = UpvoteSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "description",
            "upvotes",
            "comments",
            "link",
            "cover_image",
            "is_project",
            "created_at",
            "slug",
            "author",
        )


class BlogDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    upvotes = UpvoteSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"
