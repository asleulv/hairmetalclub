from rest_framework import serializers
from .models import Album, Tag, TagGroup

class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagGroup
        fields = ['name', 'color']

class TagSerializer(serializers.ModelSerializer):
    tag_group = TagGroupSerializer()  # Serialize the related tag group

    class Meta:
        model = Tag
        fields = ['name', 'tag_group']

class AlbumSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # Serialize the related tags

    class Meta:
        model = Album
        fields = '__all__'  # You can specify the fields you want to include here