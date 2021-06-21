from django.core.management.base import BaseCommand, CommandError
from swapshop.models import Item, ItemImage, Profile, Category
from faker import Faker
from faker.providers import internet, phone_number, address, lorem
from faker_vehicle import VehicleProvider
from django.contrib.auth.models import User
import random
import itertools
from django.utils import timezone
from django.utils.text import slugify


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
    "Networking",
    "Audio Visual",
    "Books",
    "Hardware",
    "Retro",
    "PC",
    "Mac",
    "Linux",
    "Phones",
    "Spares or Repairs",
]

ITEM_CONDITION = ["Like New", "Excelllent", "Good", "Used", "Poor", "Spares or Repair"]


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

        if users:
            for i in range(total):
                if admin:
                    try:
                        newuser = User.objects.create_user(
                            username=fakeuser.user_name(),
                            password=fakeuser.password(),
                            first_name=fakeuser.first_name(),
                            last_name=fakeuser.last_name(),
                            email=fakeuser.ascii_free_email(),
                            is_staff=True,
                            is_superuser=True,
                            last_login=timezone.now(),
                        )

                    except newuser.AlreadyExists:
                        raise CommandError(f"User { newuser.username } already exists")

                    num = random.choice(range(50))
                    newuser.profile.bio = fakeuser.paragraph(nb_sentences=5)
                    newuser.profile.phone = fakeuser.phone_number()
                    newuser.profile.birth_date = fakeuser.date_of_birth()
                    newuser.profile.image = f"profile_images/dummy-avatar{num}.jpg"
                    newuser.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created Superuser { newuser.username }"
                        )
                    )

                else:
                    try:
                        newuser = User.objects.create_user(
                            username=fakeuser.user_name(),
                            password=fakeuser.password(),
                            first_name=fakeuser.first_name(),
                            last_name=fakeuser.last_name(),
                            email=fakeuser.ascii_free_email(),
                            last_login=timezone.now(),
                        )

                    except newuser.AlreadyExists:
                        raise CommandError(f"User { newuser.username } already exists")

                    num = random.choice(range(50))
                    newuser.profile.bio = fakeuser.paragraph(nb_sentences=5)
                    newuser.profile.phone = fakeuser.phone_number()
                    newuser.profile.birth_date = fakeuser.date_of_birth()
                    newuser.profile.image = f"profile_images/dummy-avatar{num}.jpg"

                    newuser.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created User { newuser.username }"
                        )
                    )

        if category:
            for cat in CATEGORIES:
                try:
                    if not Category.objects.filter(title=cat).exists():
                        newcat = Category.objects.create(
                            title=cat, slug=slugify(cat, allow_unicode=True)
                        )
                        newcat.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created Category { newcat.title }"
                            )
                        )
                    elif Category.objects.filter(title=cat).exists():
                        print(f"Category { cat } already exists")

                except newcat.category.AlreadyExists:
                    raise CommandError(f"Category { newcat.category } already exists")

        if items:
            for i in range(total):
                try:
                    num = random.choice(range(50))
                    itm = fakeitem.vehicle_make_model()
                    categories = Category.objects.all()
                    if not Item.objects.filter(title=itm).exists():
                        newitem = Item.objects.create(
                            title=itm,
                            slug=slugify(itm, allow_unicode=True),
                            description=fakeitem.paragraph(nb_sentences=5),
                            image=f"items/dummy-item{num}.jpg",
                            condition=random.choice(ITEM_CONDITION),
                            created_by=User.objects.get(
                                id=603
                            ),  # Pick and arbitrary number from your usersid's
                        )
                        newitem.category.add(random.choice(categories))
                        newitem.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Successfully created New Item { newitem.title }"
                            )
                        )
                    elif Item.objects.filter(title=itm).exists():
                        print(f"Item { newitem.title } already exists")

                except newitem.AlreadyExists:
                    raise CommandError(f"Item { newcat.title } already exists")
