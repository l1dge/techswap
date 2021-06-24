import random

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Max, Min

from swapshop.models import Category, Item, Location


class ModelTests(TestCase):
    def test_category_str(self):
        title = Category.objects.create(title="Django Testing")
        self.assertEqual(str(title), "Django Testing django-testing")

    def test_item_str(self):
        imgnum = random.choice(range(50))
        testuser = User.objects.create_user(username="testuser", password="12345")
        cat = Category.objects.create(title="Django Testing")
        uid = User.objects.filter(pk=testuser.pk).first()
        title, created = Item.objects.get_or_create(
            title="Django Testing",
            slug="Django Testing",
            description="Django Testing",
            image=f"items/dummy-item{imgnum}.jpg",
            condition="Like New",
            created_by=uid,
        )

        if created:
            title.category.add(cat.pk)
            title.save()

        self.assertEqual(str(title), "Django Testing django-testing")

    def test_location_str(self):
        name = Location.objects.create(
            name="Django Street", town="Django Town", country="Django"
        )
        self.assertEqual(str(name), "Django Street Django Town Django")
