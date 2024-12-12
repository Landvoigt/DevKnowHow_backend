from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from category.models import Category
from .models import Command


class CommandViewSetTestCase(APITestCase):

    def setUp(self):
        # Set up any initial data here if needed
        self.admin_password = settings.DIRECT_ACTIVATION_PASSWORD
        self.category_title = "Test Category"
        self.command_data = {
            "command": "Test Command",
            "category": self.category_title,
            "description": "Test description",
            "creator_name": "Test Creator",
            "creator_email": "test@example.com",
        }
        self.admin_url = reverse('command_admin')

    def test_create_command_normal(self):
        """
        Test creating a command with a category (active=False).
        """
        response = self.client.post(reverse('command-list'), self.command_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the category was created with active=False
        category = Category.objects.get(title=self.category_title)
        self.assertFalse(category.active)

        # Check if the command was created with active=False
        command = Command.objects.get(command=self.command_data['command'])
        self.assertFalse(command.active)

    def test_create_command_admin(self):
        """
        Test creating a command with a category (active=True) using admin access.
        """
        admin_data = self.command_data.copy()
        admin_data["param"] = self.admin_password  # Include the password for admin

        response = self.client.post(self.admin_url, admin_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the category was created with active=True
        category = Category.objects.get(title=self.category_title)
        self.assertTrue(category.active)

        # Check if the command was created with active=True
        command = Command.objects.get(command=self.command_data['command'])
        self.assertTrue(command.active)

    def test_create_command_with_invalid_admin_password(self):
        """
        Test creating a command with an invalid admin password.
        """
        admin_data = self.command_data.copy()
        admin_data["param"] = "wrongpassword"  # Invalid password

        response = self.client.post(self.admin_url, admin_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "Invalid password")

    def test_category_is_not_created_with_missing_title(self):
        """
        Test that the category is not created if the category title is missing.
        """
        invalid_data = self.command_data.copy()
        invalid_data["category"] = ""  # Empty category title
        
        response = self.client.post(reverse('command-list'), invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Category title must be provided.")

    def test_create_command_with_existing_category(self):
        """
        Test that if the category already exists, it is not created again.
        """
        existing_category = Category.objects.create(title=self.category_title, active=False)

        # Use existing category
        self.command_data['category'] = self.category_title

        response = self.client.post(reverse('command-list'), self.command_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the existing category is used and not created again
        category = Category.objects.get(title=self.category_title)
        self.assertEqual(category, existing_category)

    def test_create_command_with_category_admin(self):
        """
        Test that if category exists, it should be marked active=True when created via admin.
        """
        existing_category = Category.objects.create(title=self.category_title, active=False)
        
        admin_data = self.command_data.copy()
        admin_data["category"] = self.category_title
        admin_data["param"] = self.admin_password  # Admin access
        
        response = self.client.post(self.admin_url, admin_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure category is updated to active=True
        category = Category.objects.get(title=self.category_title)
        self.assertTrue(category.active)
