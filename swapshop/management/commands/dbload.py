from django.core.management.base import BaseCommand, CommandError
from swapshop.models import Item, ItemImage, Profile, Category
from faker import Faker
from faker.providers import internet, phone_number, address
from django.contrib.auth.models import User
import random
import itertools
from django.utils import timezone

fakeuser = Faker()
fakeuser.add_provider(internet)
fakeuser.add_provider(phone_number)
fakeuser.add_provider(address)

fakeitem = Faker()


class Command(BaseCommand):
    help = "Loads Dummy Data to the DB"

    def add_arguments(self, parser):
        parser.add_argument("number_susers", nargs="+", type=int)
        parser.add_argument("number_ausers", nargs="+", type=int)
        # parser.add_argument("number_items", nargs="+", type=int)
        # parser.add_argument("number_category", nargs="+", type=int)

    def handle(self, *args, **options):
        susers = options["number_susers"][0]
        for count in range(1, int(susers) + 1):
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

            newuser.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created Superuser { newuser.username }"
                )
            )

        ausers = options["number_ausers"][0]
        for count in range(1, int(ausers) + 1):
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

            newuser.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created User { newuser.username }")
            )
