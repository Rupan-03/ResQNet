from django.core.management.base import BaseCommand
from django.utils import timezone
from rescuenetApp.models import AgencyGroup

class Command(BaseCommand):
    help = 'Delete expired agency groups'

    def handle(self, *args, **options):
        expired_groups = AgencyGroup.objects.filter(dissolution_time__lte=timezone.now())
        expired_groups.delete()
        self.stdout.write(self.style.SUCCESS('Expired agency groups deleted successfully.'))
