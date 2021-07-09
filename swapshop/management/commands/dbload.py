import itertools
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max, Min
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker
from faker.providers import address, internet, lorem, phone_number
from faker_vehicle import VehicleProvider
from swapshop.models import Category, Item, ItemImage, Profile

fakeuser = Faker()
fakeuser.add_provider(internet)
fakeuser.add_provider(phone_number)
fakeuser.add_provider(address)
fakeuser.add_provider(lorem)

fakeitem = Faker()
fakeitem.add_provider(VehicleProvider)
fakeuser.add_provider(lorem)
fakeuser.add_provider(internet)


CATEGORIES = [
    "Antiques",
    "Art",
    "Audio Visual",
    "Bath & Body Products",
    "Bathroom Fixtures, Accessories & Supplies",
    "Bikes",
    "Books",
    "Books, Comics & Magazines",
    "Building Materials & Supplies",
    "Cameras & Photography Equipment",
    "Cars, Motorcycles & Vehicles",
    "Coins- Coins, Banknotes & Bullion",
    "Collectables",
    "Computer Components & Parts",
    "Computers, Tablets & Network Hardware",
    "Costume Jewellery",
    "Cycling Equipment",
    "DIY Tools & Workshop Equipment",
    "DVDs & Blu-rays",
    "DVDs, Films & TV",
    "Electrical Equipment & Supplies",
    "Electronics",
    "Everything Else",
    "Fashion",
    "Fragrances & Aftershaves",
    "Furniture",
    "Garden & Patio",
    "Hardware",
    "Home Bedding",
    "Home Garden",
    "Home Office Furniture",
    "Household Accessories & Supplies",
    "Jewellery & Watches",
    "Linux",
    "Mac",
    "Make-Up Products",
    "Media",
    "Militaria",
    "Model Railways & Trains",
    "Motors",
    "Music",
    "Musical Instruments",
    "Networking",
    "Office Equipment & Supplies",
    "PC",
    "Pet Supplies",
    "Pet Supplies",
    "Phones",
    "Retro",
    "Sound & Vision",
    "Spares or Repairs",
    "Sporting Goods",
    "Sports Memorabilia",
    "Sports, Hobbies & Leisure",
    "Stamps",
    "Toys & Games",
    "Vehicle Parts & Accessories",
    "Video Games & Consoles",
]

CITIES = [
    ("London", "51.509865,-0.118092"),
    ("New York", "40.730610,-73.935242"),
    ("Alicante", "38.34517,-0.48149"),
    ("Barcelona", "41.3850639,2.1734035"),
    ("Sydney", "-33.869061,151.209681"),
    ("Glasgow", "55.860916,-4.251433"),
    ("Perth", "-31.953512,115.857048"),
    ("San Francisco", "37.773972,-122.431297"),
    ("Paris", "48.864716,2.349014"),
    ("Milan", "35.91979,-88.75895"),
]

ITEM_CONDITION = ["Like New", "Excellent", "Good", "Used", "Poor", "Spares or Repair"]


class Command(BaseCommand):
    help = "Loads Dummy Data to the DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users/items to be created"
        )

        parser.add_argument(
            "-u",
            "--users",
            action="store_true",
            help="Add Users",
        )

        parser.add_argument(
            "-c",
            "--category",
            action="store_true",
            help="Add Categories",
        )

        parser.add_argument(
            "-i",
            "--items",
            action="store_true",
            help="Add Dummy Items",
        )

        parser.add_argument(
            "-a", "--admin", action="store_true", help="Create an admin account"
        )

    def handle(self, *args, **options):
        total = options["total"]
        users = options["users"]
        admin = options["admin"]
        category = options["category"]
        items = options["items"]

        def make_user():
            imgnum = random.choice(range(50))
            uname = fakeuser.user_name()
            password = fakeuser.password()
            first_name = fakeuser.first_name()
            last_name = fakeuser.last_name()
            email = fakeuser.ascii_free_email()

            if not User.objects.filter(username=uname).exists():
                user = User.objects.create_user(
                    username=uname,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )

                user.last_login = timezone.now()
                user.profile.bio = fakeuser.paragraph(nb_sentences=5)
                user.profile.phone = fakeuser.phone_number()
                user.profile.birth_date = fakeuser.date_of_birth()
                user.profile.image = f"profile_images/dummy-avatar{imgnum}.jpg"
                if admin:
                    user.is_staff = True
                    user.is_superuser = True

                user.save()
                return user
            else:
                print(f"User { uname } already exists")

        def make_item():
            imgnum = random.choice(range(50))
            itm = fakeitem.vehicle_make_model()
            all_users = User.objects.all()
            maxid = all_users.aggregate(maxid=Max("id"))["maxid"]
            minid = all_users.aggregate(minid=Min("id"))["minid"]
            pk = random.randint(minid, maxid)
            categories = Category.objects.all()
            place, lat = random.choice(CITIES)

            uid = User.objects.filter(pk=pk).first()
            item, created = Item.objects.get_or_create(
                title=itm,
                slug=str(random.randint(50000, 600000)) + " " + str(uid) + " " + itm,
                description=fakeitem.paragraph(nb_sentences=5),
                image=f"items/dummy-item{imgnum}.jpg",
                condition=random.choice(ITEM_CONDITION),
                city=place,
                location=lat,
                created_by=uid,  # Pick and arbitrary number from your usersid's
            )

            if not created:
                print(f"Item { item.title } already exists")
            else:
                item.category.add(random.choice(categories))
                item.save()

        # Do the stuff

        if users:
            for _ in range(total):
                make_user()
            self.stdout.write(self.style.SUCCESS(f"Successfully created {total} Users"))

        if category:
            for cat in CATEGORIES:
                category, created = Category.objects.get_or_create(
                    title=cat, slug=slugify(cat, allow_unicode=True)
                )

                if not created:
                    print(f"Category { category.title } already exists")
                else:
                    print(f"Successfully created Category { category.title }")

        if items:
            for i in range(total):
                make_item()
            self.stdout.write(self.style.SUCCESS(f"Successfully created {total} Items"))
