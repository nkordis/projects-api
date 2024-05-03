"""
Views for the project API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Project
from project import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage project APIs."""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve projects for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
