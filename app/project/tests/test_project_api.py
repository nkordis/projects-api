"""
Tests for project API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from project.serializers import ProjectSerializer, ProjectDetailSerializer


PROJECTS_URL = reverse('project:project-list')


def detail_url(project_id):
    """Create and return a project detail URL."""
    return reverse('project:project-detail', args=[project_id])


def create_project(user, **params):
    """Create and return a sample project."""
    defaults = {
        'title': 'Sample Project',
        'bodyText': 'Sample Description',
    }
    defaults.update(params)

    project = Project.objects.create(user=user, **defaults)
    return project


class PublicProjectApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PROJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProjectApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_projects(self):
        """Test retrieving a list of projects."""
        create_project(user=self.user)
        create_project(user=self.user)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_projects_limited_to_user(self):
        """Test list of projects is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_project(user=other_user)
        create_project(user=self.user)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.filter(user=self.user)
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_project_detail(self):
        """Test get project detail."""
        project = create_project(user=self.user)

        url = detail_url(project.id)
        res = self.client.get(url)

        serializer = ProjectDetailSerializer(project)
        self.assertEqual(res.data, serializer.data)
