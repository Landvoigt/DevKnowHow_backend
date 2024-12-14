from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            title="Category 1", description="Description 1", active=True
        )
        self.category2 = Category.objects.create(
            title="Category 2", description="Description 2", active=False
        )
        self.create_url = reverse("category-list")

    def test_list_categories(self):
        """
        Test listing all categories (GET /category/)
        """
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], self.category1.title)
        self.assertEqual(response.data[1]["title"], self.category2.title)

    def test_retrieve_category(self):
        """
        Test retrieving a single category (GET /category/{id}/)
        """
        url = reverse("category-detail", args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.category1.title)
        self.assertEqual(response.data["description"], self.category1.description)

    def test_create_category(self):
        """
        Test creating a new category (POST /category/)
        """
        data = {
            "title": "Category 3",
            "description": "Description 3",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.last().title, "Category 3")

    def test_update_category(self):
        """
        Test updating an existing category (PUT /category/{id}/)
        """
        url = reverse("category-detail", args=[self.category1.id])
        data = {
            "title": "Updated Category",
            "description": "Updated Description",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.title, "Updated Category")
        self.assertEqual(self.category1.description, "Updated Description")

    def test_partial_update_category(self):
        """
        Test partially updating a category (PATCH /category/{id}/)
        """
        url = reverse("category-detail", args=[self.category1.id])
        data = {
            "description": "Partially Updated Description",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.description, "Partially Updated Description")

    def test_delete_category(self):
        """
        Test deleting a category (DELETE /category/{id}/)
        """
        url = reverse("category-detail", args=[self.category1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
        self.assertFalse(Category.objects.filter(id=self.category1.id).exists())
