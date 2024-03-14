from django.core.management.base import BaseCommand
from rescuenetApp.models import Resource

resources_data = [
    {'name': 'Ambulances', 'group': 'Non-consumable', 'type': 'Emergency Vehicles'},
    {'name': 'Rescue Trucks', 'group': 'Non-consumable', 'type': 'Emergency Vehicles'},
    {'name': 'Helicopters for air rescue', 'group': 'Non-consumable', 'type': 'Emergency Vehicles'},
    {'name': 'Radios', 'group': 'Non-consumable', 'type': 'Communication Equipment'},
    {'name': 'Satellite Phones', 'group': 'Non-consumable', 'type': 'Communication Equipment'},
    {'name': 'Two-way communication devices', 'group': 'Non-consumable', 'type': 'Communication Equipment'},
    {'name': 'First Aid Kits', 'group': 'Consumable', 'type': 'Medical Supplies'},
    {'name': 'Medications', 'group': 'Consumable', 'type': 'Medical Supplies'},
    {'name': 'Stretchers and medical equipment', 'group': 'Non-consumable', 'type': 'Medical Supplies'},
    {'name': 'Thermal Imaging Cameras', 'group': 'Non-consumable', 'type': 'Search and Rescue Equipment'},
    {'name': 'Searchlights', 'group': 'Non-consumable', 'type': 'Search and Rescue Equipment'},
    {'name': 'Rope and Climbing Gear', 'group': 'Non-consumable', 'type': 'Search and Rescue Equipment'},
    {'name': 'Emergency Shelters', 'group': 'Non-consumable', 'type': 'Shelters and Tents'},
    {'name': 'Portable Tents for Field Operations', 'group': 'Non-consumable', 'type': 'Shelters and Tents'},
    {'name': 'Potable Water', 'group': 'Consumable', 'type': 'Water and Food Supplies'},
    {'name': 'Non-perishable Food Items', 'group': 'Consumable', 'type': 'Water and Food Supplies'},
    {'name': 'Portable Generators', 'group': 'Non-consumable', 'type': 'Power Generators'},
    {'name': 'Solar Power Kits', 'group': 'Non-consumable', 'type': 'Power Generators'},
    {'name': 'GPS Devices', 'group': 'Non-consumable', 'type': 'Navigation Tools'},
    {'name': 'Maps and Compasses', 'group': 'Non-consumable', 'type': 'Navigation Tools'},
]

class Command(BaseCommand):
    help = 'Populate the Resource model with initial data'

    def handle(self, *args, **options):
        for resource_info in resources_data:
            Resource.objects.create(**resource_info)

        self.stdout.write(self.style.SUCCESS('Resources populated successfully'))
