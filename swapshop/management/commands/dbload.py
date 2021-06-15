from django.core.management.base import BaseCommand, CommandError
from swapshop.models import Item, ItemImage, AppUser, Category
from faker import Faker
from faker.providers import internet
from django.contrib.auth.models import User
import random
import itertools

fake = Faker()
fake.add_provider(internet)


class Command(BaseCommand):
    help = "Loads Dummy Data to the DB"

    def add_arguments(self, parser):
        parser.add_argument("number_users", nargs="+", type=int)
        parser.add_argument("number_appusers", nargs="+", type=int)
        # parser.add_argument("number_items", nargs="+", type=int)
        # parser.add_argument("number_category", nargs="+", type=int)

    def handle(self, *args, **options):
        users = options["number_users"][0]
        for count in range(int(users)):
            try:
                newuser = User.objects.create_user(
                    fake.user_name(),
                    fake.password(),
                    fake.ascii_free_email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )

            except newuser.AlreadyExists:
                raise CommandError(f"User { newuser.username } already exists")

            newuser.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created User { newuser.username }")
            )

        users = options["number_appusers"][0]
        for count in range(int(users)):
            try:
                used_id = set(AppUser.objects.values_list("user_id", flat=True))
                muid = max(
                    set(User.objects.values_list("id", flat=True)), key=lambda x: int(x)
                )
                id = random.randint(5, muid)

                if id not in used_id:
                    appuser = AppUser.objects.create(
                        full_name=fake.name(),
                        address=fake.address(),
                        user_id=id,
                    )
                else:
                    pass

            except appuser.AlreadyExists:
                raise CommandError(f"User { appuser.full_name } already exists")

            appuser.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully created User { appuser.full_name }")
            )
