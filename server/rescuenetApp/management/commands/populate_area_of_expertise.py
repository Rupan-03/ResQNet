from django.core.management.base import BaseCommand
from rescuenetApp.models import AreaofExpertise

class Command(BaseCommand):
    help = 'Populate Area of Expertise entries'

    def handle(self, *args, **kwargs):
        expertises = ['Rescue', 'Medical', 'FireFighters']

        for expertise in expertises:
            AreaofExpertise.objects.create(expertise=expertise)

        self.stdout.write(self.style.SUCCESS('Successfully populated Area of Expertise entries'))
