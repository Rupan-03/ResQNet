from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from rescuenetApp.models import Hospital

hospital_data = [
    {
        'name': 'City General Hospital',
        'location': {'type': 'Point', 'coordinates': [77.5946, 12.9716]},
        'address': '334 Main Street, Coimbatore'
    },
    {
        'name': 'Central Hospital',
        'location': {'type': 'Point', 'coordinates': [77.2201, 28.6328]},
        'address': '123 Central Avenue, New Delhi'
    },
    {
        'name': 'Metro Hospital',
        'location': {'type': 'Point', 'coordinates': [77.2266, 28.6139]},
        'address': '456 XYZ Street, New Delhi'
    },
    {
        'name': 'Apollo Hospital',
        'location': {'type': 'Point', 'coordinates': [72.8777, 19.0760]},
        'address': '789 PQR Road, Mumbai'
    },
    {
        'name': 'Greenview Hospital',
        'location': {'type': 'Point', 'coordinates': [77.2167, 28.6139]},
        'address': '101 Green Road, New Delhi'
    },
    {
        'name': 'Fortis Hospital',
        'location': {'type': 'Point', 'coordinates': [77.1025, 28.7041]},
        'address': '12 Fortis Avenue, Gurgaon'
    },
    {
        'name': 'AIIMS Hospital',
        'location': {'type': 'Point', 'coordinates': [77.2089, 28.5665]},
        'address': 'AIIMS Campus, New Delhi'
    },
    {
        'name': 'Max Super Specialty Hospital',
        'location': {'type': 'Point', 'coordinates': [77.0636, 28.4945]},
        'address': '1 Max Road, Saket, New Delhi'
    },
    {
        'name': 'Medanta - The Medicity',
        'location': {'type': 'Point', 'coordinates': [77.0428, 28.4214]},
        'address': 'Chowk to Medanta Road, Gurgaon'
    },
    {
        'name': 'Artemis Hospital',
        'location': {'type': 'Point', 'coordinates': [77.0723, 28.4396]},
        'address': 'Artemis Avenue, Gurgaon'
    },
]

class Command(BaseCommand):
    help = 'Populate the Hospital model with initial data'

    def handle(self, *args, **options):
        for hospital_info in hospital_data:
            location_data = hospital_info.pop('location')
            coordinates = location_data['coordinates']
            location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
            Hospital.objects.create(location=location, **hospital_info)

        self.stdout.write(self.style.SUCCESS('Hospitals populated successfully'))
