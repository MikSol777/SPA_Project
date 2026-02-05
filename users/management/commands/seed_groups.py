from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from users.permissions import MODERATOR_GROUP


class Command(BaseCommand):
    help = "Create default groups (moderators)."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name=MODERATOR_GROUP)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Group '{MODERATOR_GROUP}' created"))
        else:
            self.stdout.write(self.style.WARNING(f"Group '{MODERATOR_GROUP}' already exists"))










