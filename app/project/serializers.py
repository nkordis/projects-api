"""
Serializers for the project API View.
"""
from rest_framework import serializers

from core.models import Project, Tag


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the projects."""

    class Meta:
        model = Project
        fields = ("id", 'title', 'bodyText')
        read_only_fields = ('id',)


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for the project detail."""
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
