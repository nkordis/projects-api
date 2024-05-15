"""
Views for the project API.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Project, Tag, Link
from project import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage project APIs."""
    serializer_class = serializers.ProjectDetailSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve projects for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

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
        return self.queryset.filter(user=self.request.user).order_by('-name')


class LinkViewSet(BaseProjectAttrViewSet):
    """Manage links in the database."""
    serializer_class = serializers.LinkSerializer
    queryset = Link.objects.all()

    def get_queryset(self):
        """Retrieve links for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-text')
