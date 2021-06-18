from django.core.management.base import BaseCommand, CommandError
from swapshop.models import Item, ItemImage, Profile, Category
from faker import Faker
from faker.providers import internet, phone_number, address, lorem, profile
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

fakecategory = Faker()

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


class Command(BaseCommand):
    help = "Loads Dummy Data to the DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users to be created"
        )

        parser.add_argument(
            "-c",
            "--category",
            action="store_true",
            help="Add Categories",
        )

        parser.add_argument(
            "-a", "--admin", action="store_true", help="Create an admin account"
        )

    def handle(self, *args, **options):
        total = options["total"]
        admin = options["admin"]
        category = options["category"]

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

                newuser.profile.bio = fakeuser.paragraph(nb_sentences=5)
                newuser.profile.phone = fakeuser.phone_number()
                newuser.profile.birth_date = fakeuser.date_of_birth()
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

                newuser.profile.bio = fakeuser.paragraph(nb_sentences=5)
                newuser.profile.phone = fakeuser.phone_number()
                newuser.profile.birth_date = fakeuser.date_of_birth()
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
