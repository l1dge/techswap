from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Max, Min


from swapshop.models import Category, Item
import random

# Create your tests here.


class ModelTests(TestCase):
    def test_category_str(self):
        title = Category.objects.create(title="Django Testing")
        self.assertEqual(str(title), "Django Testing django-testing")

    def test_item_str(self):
        imgnum = random.choice(range(50))
        all_users = User.objects.all()
        maxid = all_users.aggregate(maxid=Max("id"))["maxid"]
        minid = all_users.aggregate(minid=Min("id"))["minid"]
        pk = random.randint(minid, maxid)
        uid = User.objects.filter(pk=pk).first()
        categories = Category.objects.all()
        title, created = Item.objects.get_or_create(
            title="Django Testing",
            slug="Django Testing",
            description="Django Testing",
            image=f"items/dummy-item{imgnum}.jpg",
            condition="Like New",
            created_by=uid,  # Pick and arbitrary number from your usersid's
        )

        if created:
            title.category.add(random.choice(categories))
            title.save()

        self.assertEqual(str(title), "Django Testing django-testing")
