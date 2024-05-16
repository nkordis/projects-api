"""
Views for the project API.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Project, Tag, Link
from project import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'links',
                OpenApiTypes.STR,
                description='Comma separated list of link IDs to filter',
            ),
        ]
    )
)
class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage project APIs."""
    serializer_class = serializers.ProjectDetailSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve projects for authenticated user."""
        tags = self.request.query_params.get('tags')
        links = self.request.query_params.get('links')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if links:
            link_ids = self._params_to_ints(links)
            queryset = queryset.filter(links__id__in=link_ids)

        queryset = queryset.filter(user=self.request.user).order_by('-id')
        return queryset.distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProjectSerializer
        elif self.action == 'upload_image':
            return serializers.ProjectImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new project."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to project."""
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to user',
            ),
        ]
    )
)
class BaseProjectAttrViewSet(mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """Base viewset for project attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TagViewSet(BaseProjectAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Retrieve tags for authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        # Start with the queryset filtered by the user
        queryset = self.queryset.filter(user=self.request.user)
        # Apply filter for assigned_only if specified
        if assigned_only:
            queryset = queryset.filter(project__isnull=False)
        # Return the filtered queryset ordered by name and distinct
        return queryset.order_by('-name').distinct()


class LinkViewSet(BaseProjectAttrViewSet):
    """Manage links in the database."""
    serializer_class = serializers.LinkSerializer
    queryset = Link.objects.all()

    def get_queryset(self):
        """Retrieve links for authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        # Start with the queryset filtered by the user
        queryset = self.queryset.filter(user=self.request.user)
        # Apply filter for assigned_only if specified
        if assigned_only:
            queryset = queryset.filter(project__isnull=False)
        # Return the filtered queryset ordered by text and distinct
        return queryset.order_by('-text').distinct()
