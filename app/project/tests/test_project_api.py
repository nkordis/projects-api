"""
Tests for project API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project, Tag

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


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com',
                                password='testpass123')
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
        other_user = create_user(email='other@example.com',
                                 password='XXXXXXXXX')
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

    def test_create_project(self):
        """Test creating a project."""
        payload = {
            'title': 'Sample Project',
            'bodyText': 'Sample Description',
        }
        res = self.client.post(PROJECTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(project, k), v)
        self.assertEqual(project.user, self.user)

    def test_partial_update(self):
        """Test partial update of a project."""
        original_title = 'Sample Project'
        project = create_project(
            user=self.user,
            title=original_title
        )

        payload = {'title': 'New Project Title'}
        url = detail_url(project.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.title, payload['title'])
        self.assertEqual(project.user, self.user)

    def test_full_update(self):
        """Test full update of project."""
        original_title = 'Sample Project'
        project = create_project(
            user=self.user,
            title=original_title
        )

        payload = {'title': 'New Project Title',
                   'bodyText': 'New Description'}
        url = detail_url(project.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(project, k), v)
        self.assertEqual(project.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the project user results in an error."""
        new_user = create_user(email='user2@example.com',
                               password='XXXXXXXXXXX')
        project = create_project(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(project.id)
        self.client.patch(url, payload)

        project.refresh_from_db()
        self.assertEqual(project.user, self.user)

    def test_delete_project(self):
        """Test deleting a project successful."""
        project = create_project(user=self.user)

        url = detail_url(project.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=project.id).exists())

    def test_delete_other_users_project_error(self):
        """Test trying to delete another users project gives error."""
        new_user = create_user(email='user2@example.com',
                               password='XXXXXXXXXXX')
        project = create_project(user=new_user)

        url = detail_url(project.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Project.objects.filter(id=project.id).exists())

    def test_create_project_with_new_tags(self):
        """Test creating a project with new tags."""
        payload = {
            'title': 'Sample Project',
            'bodyText': 'Sample Description',
            'tags': [{'name': 'Python'}, {'name': 'Java'}]
        }
        res = self.client.post(PROJECTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        projects = Project.objects.filter(user=self.user)
        self.assertEqual(projects.count(), 1)
        project = projects[0]
        self.assertEqual(project.tags.count(), 2)
        for tag in payload['tags']:
            exists = project.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_project_with_existing_tags(self):
        """Test creating a project with existing tag."""
        tag_python = Tag.objects.create(user=self.user, name='Python')
        payload = {
            'title': 'Sample Project',
            'bodyText': 'Sample Description',
            'tags': [{'name': 'Python'}, {'name': 'Java'}]
        }
        res = self.client.post(PROJECTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        projects = Project.objects.filter(user=self.user)
        self.assertEqual(projects.count(), 1)
        project = projects[0]
        self.assertEqual(project.tags.count(), 2)
        self.assertIn(tag_python, project.tags.all())
        for tag in payload['tags']:
            exists = project.tags.filter(
                name=tag['name'],
                user=self.user
            ).exists()
            self.assertTrue(exists)
