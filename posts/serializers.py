from rest_framework import serializers
from posts.models import Post
from rest_framework.serializers import Field


class PostSerializer(serializers.ModelSerializer):
    author: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
