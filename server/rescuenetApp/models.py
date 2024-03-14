from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.gis.measure import D
from datetime import timedelta

class AreaOfExpertise(models.Model):
    expertise = models.CharField(max_length=255)

    def __str__(self):
        return self.expertise

class Resource(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ResourceQuantity(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    agency = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.agency.username} - {self.resource.name} - {self.quantity}'

class CustomUser(AbstractUser):
    location = models.PointField(null=True, blank=True)
    area_of_expertise = models.ForeignKey(AreaOfExpertise, on_delete=models.CASCADE, null=True, blank=True)
    last_activity_type = models.CharField(max_length=255, null=True)
    last_activity_location = models.CharField(max_length=255, null=True)
    last_activity_timestamp = models.DateField(null=True)
    resources = models.ManyToManyField(Resource, through=ResourceQuantity)
    role = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Disaster(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()
    address = models.CharField(max_length=255)
    disaster_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return self.name
    
    @classmethod
    def get_last_disaster(cls):
        return cls.objects.latest('timestamp')
    
    def create_agency_group(self):
        # Logic to create agency group for this disaster goes here
        nearby_agencies = CustomUser.objects.filter(location__distance_lte=(self.location, D(km=100)))
        
        # Create an agency group for the nearby agencies
        name=self.name
        name='_'.join(name.split(' '))

        group_name = f"Group_for_Disaster_{name}"
        agency_group = AgencyGroup.objects.create(disaster=self, name=group_name)
        agency_group.agencies.add(*nearby_agencies)
        
        dissolution_time = timezone.now() + timedelta(days=1)
        
        # The issue might be here, ensure to set the dissolution_time before saving
        #print("Dissolution Time:", dissolution_time)
        agency_group.dissolution_time = dissolution_time
        agency_group.save()
    
    def delete_agency_group(self):
        # Logic to delete agency group for this disaster goes here
        # This method will be called automatically when a disaster is deleted
        AgencyGroup.objects.filter(disaster=self).delete()

class AgencyGroup(models.Model):
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    agencies = models.ManyToManyField(CustomUser)
    dissolution_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

