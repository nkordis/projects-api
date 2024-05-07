"""
Serializers for the project API View.
"""
from rest_framework import serializers

from core.models import Project, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the projects."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ("id", 'title', 'bodyText', 'tags')
        read_only_fields = ('id',)

    def _get_or_create_tags(self, tags, project):
        """Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            project.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a new project."""
        tags = validated_data.pop('tags', [])
        project = Project.objects.create(**validated_data)
        self._get_or_create_tags(tags, project)

        return project

    def update(self, instance, validated_data):
        """Update a project."""
        tags = validated_data.pop('tags', [])
        if tags is not None:
            instance.tags.clear()
            if tags:
                self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for the project detail."""
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ()
