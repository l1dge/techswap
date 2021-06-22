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
from django.db.models import Max, Min
from django.contrib.auth.hashers import make_password


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

        def makeuser():
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
                return 0
            else:
                print(f"User { uname } already exists")
                pass

        def makeitem():
            imgnum = random.choice(range(50))
            itm = fakeitem.vehicle_make_model()
            maxid = User.objects.all().aggregate(maxid=Max("id"))["maxid"]
            minid = User.objects.all().aggregate(minid=Min("id"))["minid"]
            pk = random.randint(minid, maxid)
            categories = Category.objects.all()
            uid = User.objects.filter(pk=pk).first()
            item, created = Item.objects.get_or_create(
                title=itm,
                slug=str(random.randint(50000, 600000)) + " " + str(uid) + " " + itm,
                description=fakeitem.paragraph(nb_sentences=5),
                image=f"items/dummy-item{imgnum}.jpg",
                condition=random.choice(ITEM_CONDITION),
                created_by=uid,  # Pick and arbitrary number from your usersid's
            )

            if created:
                item.category.add(random.choice(categories))
                item.save()
            else:
                raise CommandError(f"Item { item.title } already exists")
                pass

        # Do the stuff

        if users:
            for _ in range(total):
                makeuser()
            self.stdout.write(self.style.SUCCESS(f"Successfully created {total} Users"))

        if category:
            for cat in CATEGORIES:
                category, created = Category.objects.get_or_create(
                    title=cat, slug=slugify(cat, allow_unicode=True)
                )

                if created:
                    return f"Successfully created Category { category.title }"
                else:
                    raise CommandError(f"Category { category.title } already exists")

        if items:
            for i in range(total):
                makeitem()
            self.stdout.write(self.style.SUCCESS(f"Successfully created {total} Items"))
