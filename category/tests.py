from django.test import TestCase
from .models import Category, SubCategory


class CategoryDeletionTest(TestCase):
    def test_subcategory_deletion_on_category_delete(self):
        category = Category.objects.create(title="Test Category")
        subcategory = SubCategory.objects.create(category=category, title="Test SubCategory")
        
        category.delete()
        
        self.assertFalse(SubCategory.objects.filter(title="Test SubCategory").exists(), "SubCategory was not deleted.")

class SubCategoryCreationTest(TestCase):
    def test_single_subcategory_creation(self):
        category = Category.objects.create(title="Test Category")
        SubCategory.objects.create(category=category, title="Test SubCategory")
        
        self.assertEqual(SubCategory.objects.count(), 1, "More than one SubCategory created.")
