# rescuenetApp/serializers.py
from django.contrib.gis.geos import Point
from rest_framework import serializers
from .models import AreaOfExpertise, Resource, ResourceQuantity, CustomUser, Hospital, School,Disaster,AgencyGroup

class AreaOfExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfExpertise
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ResourceQuantitySerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)

    class Meta:
        model = ResourceQuantity
        fields = ['id', 'quantity', 'resource', 'agency', 'resource_name']

    def update(self, instance, validated_data):
        # Ensure 'quantity' field is provided and is a positive integer
        quantity = validated_data.get('quantity')
        if quantity is None:
            raise serializers.ValidationError({'quantity': 'Quantity field is required'})
        if not isinstance(quantity, int) or quantity <= 0:
            raise serializers.ValidationError({'quantity': 'Quantity must be a positive integer'})

        # Update the quantity field of the instance
        instance.quantity = quantity
        instance.save()

        return instance

class CustomUserSerializer(serializers.ModelSerializer):
    location = serializers.DictField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        # Extract location data
        location_data = validated_data.pop('location', None)

        # Create a Point object if location data is provided
        if location_data and 'coordinates' in location_data:
            coordinates = location_data['coordinates']
            location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
        else:
            location = None

        # Include 'role' in validated_data and remove it
        role = validated_data.pop('role', None)

        # Create the CustomUser instance
        user = CustomUser.objects.create(location=location, **validated_data, role=role)

        return user

class CustomUserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'location']  # Include only the necessary fields

    def get_location(self, obj):
        # Convert Point object to a dictionary with 'type' and 'coordinates' keys
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None

class CustomUserDetailSerializerspecific(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    resources = ResourceSerializer(many=True, read_only=True)  # Nested serializer for resources

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'location', 'last_activity_type', 'last_activity_location', 'last_activity_timestamp', 'resources']

    def get_location(self, obj):
        # Convert Point object to a dictionary with 'type' and 'coordinates' keys
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None


class HospitalSerializer(serializers.ModelSerializer):
    location = serializers.DictField(write_only=True)
    location_data = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'location', 'address', 'location_data']

    def get_location_data(self, obj):
        # Convert Point object to a dictionary with 'type' and 'coordinates' keys
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None

    def create(self, validated_data):
        # Extract location data
        location_data = validated_data.pop('location', None)

        # Create a Point object if location data is provided
        if location_data and 'coordinates' in location_data:
            coordinates = location_data['coordinates']
            location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
        else:
            location = None

        # Create the Hospital instance
        hospital = Hospital.objects.create(location=location, **validated_data)

        return hospital

    def update(self, instance, validated_data):
        # Extract and handle location data if provided
        location_data = validated_data.pop('location', None)
        if location_data and 'coordinates' in location_data:
            coordinates = location_data['coordinates']
            instance.location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
        else:
            instance.location = None

        # Update other fields of the instance
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)

        # Save and return the updated instance
        instance.save()
        return instance


class SchoolSerializer(serializers.ModelSerializer):
    location = serializers.DictField(write_only=True)
    location_data = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'location', 'address', 'location_data']

    def get_location_data(self, obj):
        # Convert Point object to a dictionary with 'type' and 'coordinates' keys
        if obj.location:
            return {
                'type': 'Point',
                'coordinates': [obj.location.x, obj.location.y]
            }
        return None

    def create(self, validated_data):
        # Extract location data
        location_data = validated_data.pop('location', None)

        # Create a Point object if location data is provided
        if location_data and 'coordinates' in location_data:
            coordinates = location_data['coordinates']
            location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
        else:
            location = None

        # Create the School instance
        school = School.objects.create(location=location, **validated_data)

        return school

    def update(self, instance, validated_data):
        # Extract and handle location data if provided
        location_data = validated_data.pop('location', None)
        if location_data and 'coordinates' in location_data:
            coordinates = location_data['coordinates']
            instance.location = Point(x=coordinates[0], y=coordinates[1], srid=4326)
        else:
            instance.location = None

        # Update other fields of the instance
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)

        # Save and return the updated instance
        instance.save()
        return instance
#Disaster serializer

class DisasterSerializer(serializers.ModelSerializer):
    # Serializer method field to serialize PointField
    location = serializers.DictField(write_only=True)

    class Meta:
        model = Disaster
        fields = ['id', 'name', 'location', 'address', 'disaster_type', 'timestamp', 'details']

    def create(self, validated_data):
        # Extract location data
        location_data = validated_data.pop('location', None)

        # Create a Point object if location data is provided
        if location_data and 'latitude' in location_data and 'longitude' in location_data:
            location = Point(x=location_data['longitude'], y=location_data['latitude'], srid=4326)
        else:
            location = None

        # Create the Disaster instance
        disaster = Disaster.objects.create(location=location, **validated_data)
        return disaster

    def update(self, instance, validated_data):
        # Extract and handle location data if provided
        location_data = validated_data.pop('location', None)
        if location_data and 'latitude' in location_data and 'longitude' in location_data:
            instance.location = Point(x=location_data['longitude'], y=location_data['latitude'], srid=4326)
        else:
            instance.location = None

        # Update other fields of the instance
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.disaster_type = validated_data.get('disaster_type', instance.disaster_type)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.details = validated_data.get('details', instance.details)

        # Save and return the updated instance
        instance.save()
        return instance

class AgencyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyGroup
        fields = ['id', 'name', 'disaster', 'agencies', 'dissolution_time']
