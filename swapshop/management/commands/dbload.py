from django.core.management.base import BaseCommand, CommandError
from swapshop.models import Item, ItemImage, AppUser, Category
from faker import Faker
from faker.providers import internet, phone_number, address
from django.contrib.auth.models import User
import random
import itertools

fake = Faker()
fake.add_provider(internet)
fake.add_provider(phone_number)
fake.add_provider(address)


class Command(BaseCommand):
    help = "Loads Dummy Data to the DB"

    def add_arguments(self, parser):
        parser.add_argument("number_susers", nargs="+", type=int)
        parser.add_argument("number_ausers", nargs="+", type=int)
        # parser.add_argument("number_items", nargs="+", type=int)
        # parser.add_argument("number_category", nargs="+", type=int)

    def handle(self, *args, **options):
        susers = options["number_susers"][0]
        for count in range(int(susers)):
            try:
                newuser = AppUser.objects.create_user(
                    username=fake.user_name(),
                    password=fake.password(),
                    email=fake.ascii_free_email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    mobile=fake.phone_number(),
                    is_staff=True,
                    is_superuser=True,
                )

            except newuser.AlreadyExists:
                raise CommandError(f"User { newuser.username } already exists")

            newuser.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created Superuser { newuser.username }"
                )
            )

        ausers = options["number_ausers"][0]
        for count in range(int(ausers)):
            try:
                newuser = AppUser.objects.create_user(
                    username=fake.user_name(),
                    password=fake.password(),
                    email=fake.ascii_free_email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    mobile=fake.phone_number(),
                )

            except newuser.AlreadyExists:
                raise CommandError(f"AppUser { newuser.username } already exists")

            newuser.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created AppUser { newuser.username }")
            )
