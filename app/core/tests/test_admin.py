"""Test for Django admin modifications"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_last_login_field_is_read_only(self):
        """Test that the last_login field is read-only in admin"""
        url = reverse("admin:core_user_change", args=[self.user.id])

        res = self.client.get(url)

        # Check that the last_login field is not editable
        self.assertContains(res, 'Last login:')
        self.assertNotContains(res, 'id="id_last_login_0"')
        self.assertNotContains(res, 'id="id_last_login_1"')
