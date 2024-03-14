from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils import timezone
from rescuenetApp.models import CustomUser, AreaOfExpertise, Resource, ResourceQuantity
import random

# Function to generate random coordinates within the middle region of India
def generate_random_coordinates():
    # Middle region of India's geographical bounds
    min_longitude, max_longitude = 73.0, 86.0
    min_latitude, max_latitude = 19.0, 26.0
    
    latitude = round(random.uniform(min_latitude, max_latitude), 4)
    longitude = round(random.uniform(min_longitude, max_longitude), 4)
    
    return longitude, latitude

# Command class to populate the database with rescue agency entries in the middle region of India
class Command(BaseCommand):
    help = 'Populates the database with rescue agency entries in the middle region of India'

    def handle(self, *args, **options):
        # Create 10 rescue agency entries
        for i in range(1, 10):
            username = f"agency_{i}"
            email = f"agency{i}@example.com"
            location = Point(*generate_random_coordinates())
            area_of_expertise_id = random.randint(1, 10)  # Randomly select area of expertise ID
            last_activity_type = "Emergency Response"
            last_activity_location = "City Name"
            last_activity_timestamp = timezone.now()
            role = "regular_user"
            password = "Qwerty@123"  # Set the password for all agencies

            # Create rescue agency entry
            rescue_agency = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                location=location,
                area_of_expertise_id=area_of_expertise_id,
                last_activity_type=last_activity_type,
                last_activity_location=last_activity_location,
                last_activity_timestamp=last_activity_timestamp,
                role=role
            )

            self.stdout.write(self.style.SUCCESS(f"Rescue agency {username} created in the middle region of India."))
