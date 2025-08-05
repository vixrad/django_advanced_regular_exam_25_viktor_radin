from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from restaurants.models import Restaurant
from reservations.models import Reservation
from menu.models import MenuCategory, MenuItem

class Command(BaseCommand):
    help = "Initialize default groups and permissions"

    def handle(self, *args, **kwargs):
        # Create or get group
        group, created = Group.objects.get_or_create(name="Restaurant Admins")
        if created:
            self.stdout.write(self.style.SUCCESS("Created group 'Restaurant Admins'"))
        else:
            self.stdout.write("Group 'Restaurant Admins' already exists")

        # Assign permissions
        models_to_grant = [Restaurant, Reservation, MenuCategory, MenuItem]
        perms = []
        for model in models_to_grant:
            content_type = ContentType.objects.get_for_model(model)
            for codename in ["view", "add", "change"]:
                perm = Permission.objects.get(codename=f"{codename}_{model._meta.model_name}", content_type=content_type)
                perms.append(perm)

        group.permissions.set(perms)
        group.save()

        self.stdout.write(self.style.SUCCESS("Permissions assigned to 'Restaurant Admins'"))