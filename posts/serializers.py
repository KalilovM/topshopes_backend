from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.first_name")

    class Meta:
        model = Post
        fields = "__all__"
