from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from rescuenetApp.models import School

school_data = [
    {
        'name': 'City Public School',
        'location': {'type': 'Point', 'coordinates': [77.5946, 12.9716]},
        'address': '123 City Avenue, Coimbatore'
    },
    {
        'name': 'Central School',
        'location': {'type': 'Point', 'coordinates': [77.2201, 28.6328]},
        'address': '456 Central Street, New Delhi'
    },
    {
        'name': 'Metro International School',
        'location': {'type': 'Point', 'coordinates': [77.2266, 28.6139]},
        'address': '789 Metro Road, New Delhi'
    },
    {
        'name': 'Apollo Public School',
        'location': {'type': 'Point', 'coordinates': [72.8777, 19.0760]},
        'address': '101 Apollo Road, Mumbai'
    },
    {
        'name': 'Greenview High School',
        'location': {'type': 'Point', 'coordinates': [77.2167, 28.6139]},
        'address': '12 Greenview Avenue, New Delhi'
    },
    {
        'name': 'Fortis Academy',
        'location': {'type': 'Point', 'coordinates': [77.1025, 28.7041]},
        'address': 'Fortis Campus, Gurgaon'
    },
    {
        'name': 'AIIMS Public School',
        'location': {'type': 'Point', 'coordinates': [77.2089, 28.5665]},
        'address': 'AIIMS Road, New Delhi'
    },
    {
        'name': 'Max International School',
        'location': {'type': 'Point', 'coordinates': [77.0636, 28.4945]},
        'address': '1 Max Road, Saket, New Delhi'
    },
    {
        'name': 'Medanta Public School',
        'location': {'type': 'Point', 'coordinates': [77.0428, 28.4214]},
        'address': 'Medanta Avenue, Gurgaon'
    },
    {
        'name': 'Artemis High School',
        'location': {'type': 'Point', 'coordinates': [77.0723, 28.4396]},
        'address': 'Artemis Road, Gurgaon'
    },
]

class Command(BaseCommand):
    help = 'Populate the School model with initial data'

    def handle(self, *args, **options):
        for school_info in school_data:
            location_data = school_info.pop('location')
            coordinates = location_data['coordinates']
            location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
            School.objects.create(location=location, **school_info)

        self.stdout.write(self.style.SUCCESS('Schools populated successfully'))
