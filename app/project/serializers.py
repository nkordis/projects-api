"""
Serializers for the project API View.
"""
from rest_framework import serializers

from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the projects."""

    class Meta:
        model = Project
        fields = ("id", 'title', 'bodyText')
        read_only_fields = ('id',)
