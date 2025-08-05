from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

FULL_ADMIN_GROUP = "Full Admin"
STAFF_ADMIN_GROUP = "Staff Admin"

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.filter(name="Restaurant Admins").delete()
    full_admin, _ = Group.objects.get_or_create(name=FULL_ADMIN_GROUP)
    if not full_admin.permissions.exists():
        full_admin.permissions.set(Permission.objects.all())
    staff_admin, _ = Group.objects.get_or_create(name=STAFF_ADMIN_GROUP)
    if not staff_admin.permissions.exists():
        allowed_codenames = [
            "add_restaurant", "change_restaurant",
            "add_menuitem", "change_menuitem",
            "add_reservation", "change_reservation",
        ]
        staff_permissions = Permission.objects.filter(codename__in=allowed_codenames)
        staff_admin.permissions.set(staff_permissions)