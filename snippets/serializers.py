from rest_framework import serializers
from .models import Snippet, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','title',)

class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'content', 'timestamp', 'tags')


class SnippetCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ('title', 'content', 'tags')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        snippet = Snippet.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            snippet.tags.add(tag)
        return snippet