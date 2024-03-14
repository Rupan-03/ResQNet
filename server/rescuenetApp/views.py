from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate, login
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics

from .models import AreaOfExpertise, Resource, ResourceQuantity, CustomUser,Hospital,School,Disaster,AgencyGroup
from .serializers import (
    AreaOfExpertiseSerializer, ResourceSerializer,
    ResourceQuantitySerializer, CustomUserSerializer,CustomUserDetailSerializer,CustomUserDetailSerializerspecific,HospitalSerializer,
    SchoolSerializer,DisasterSerializer,AgencyGroupSerializer
)
class AreaOfExpertiseListView(generics.ListCreateAPIView):
    queryset = AreaOfExpertise.objects.all()
    serializer_class = AreaOfExpertiseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AreaOfExpertiseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AreaOfExpertise.objects.all()
    serializer_class = AreaOfExpertiseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ResourceListView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ResourceQuantityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceQuantity.objects.all()
    serializer_class = ResourceQuantitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

class RescueAgencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializerspecific
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user has the role 'rescue_agency'
        if user.role != 'regular_user':
            return Response({'error': 'Permission denied. Not a rescue agency.'}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'id':user.id,'token': token.key}, status=status.HTTP_200_OK)

class RescueAgencyRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        role = 'regular_user'
        serializer.save(role=role)


class RescueAgencyUpdateLastActivityView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if not request.user.is_superuser and request.user.id != instance.id:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save(
            last_activity_type=self.request.data.get('last_activity_type'),
            last_activity_location=self.request.data.get('last_activity_location'),
            last_activity_timestamp=self.request.data.get('last_activity_timestamp')
        )

class RescueAgencyListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


#CURD opertion
class ResourceQuantityListView(generics.ListAPIView):
    serializer_class = ResourceQuantitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        agency_id = self.request.query_params.get('agency_id')
        if agency_id is not None:
            return ResourceQuantity.objects.filter(agency_id=agency_id)
        else:
            return ResourceQuantity.objects.none()

class AddResourceQuantityView(generics.CreateAPIView):
    serializer_class = ResourceQuantitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the agency ID from the URL query parameter
        agency_id = self.request.query_params.get('agency_id')

        # Get the resource ID and quantity from the request data
        resource_id = request.data.get('resource_id')
        quantity = request.data.get('quantity')

        # Check if the agency ID, resource ID, and quantity are provided
        if not (agency_id and resource_id and quantity):
            return Response({'error': 'Agency ID, resource ID, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the agency and resource exist
            agency = CustomUser.objects.get(pk=agency_id)
            resource = Resource.objects.get(pk=resource_id)

            # Check if a resource quantity entry already exists for the agency and resource
            existing_entry = ResourceQuantity.objects.filter(agency=agency, resource=resource).first()

            if existing_entry:
                # Return a 409 Conflict response if a duplicate entry exists
                return Response({'error': 'Resource quantity entry already exists for this agency and resource'}, status=status.HTTP_409_CONFLICT)

            # Create a new resource quantity instance
            instance = ResourceQuantity.objects.create(resource=resource, agency=agency, quantity=quantity)
            serializer = self.get_serializer(instance)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Agency not found'}, status=status.HTTP_404_NOT_FOUND)
        except Resource.DoesNotExist:
            return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateResourceQuantityView(generics.UpdateAPIView):
    serializer_class = ResourceQuantitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        agency_id = self.request.query_params.get('agency_id')
        resource_id = request.data.get('resource_id')  # Assuming the resource_id is provided in the request data
        quantity = request.data.get('quantity')

        # Check if the agency ID, resource ID, and quantity are provided
        if not (agency_id and resource_id and quantity):
            return Response({'error': 'Agency ID, resource ID, and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the resource quantity entry exists for the agency and resource
            resource_quantity = ResourceQuantity.objects.get(agency_id=agency_id, resource_id=resource_id)
            resource_quantity.quantity = quantity
            resource_quantity.save()
            serializer = self.get_serializer(resource_quantity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResourceQuantity.DoesNotExist:
            return Response({'error': 'Resource quantity entry does not exist'}, status=status.HTTP_404_NOT_FOUND)


class DeleteResourceQuantityView(generics.DestroyAPIView):
    serializer_class = ResourceQuantitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Get the agency ID and resource ID from the URL query parameters
        agency_id = self.request.query_params.get('agency_id')
        resource_id = self.request.query_params.get('resource_id')

        # Get the resource quantity instance to delete
        try:
            instance = ResourceQuantity.objects.get(agency_id=agency_id, resource_id=resource_id)
        except ResourceQuantity.DoesNotExist:
            return Response({'error': 'Resource quantity not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the deleted instance
        serializer = self.get_serializer(instance)
        
        # Delete the resource quantity
        instance.delete()
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


#CURD for schools and hospitals
class HospitalListView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class HospitalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class SchoolListView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DisasterAPIView(APIView):

    
    def get(self, request, *args, **kwargs):
        # Retrieve the latest disaster object
        latest_disaster = Disaster.get_last_disaster()
        serializer = DisasterSerializer(latest_disaster)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DisasterSerializer(data=request.data)
        if serializer.is_valid():
            disaster = serializer.save()
        
        # Create agency group and notify agencies
            disaster.create_agency_group()
        
        # Get the associated agency group
            agency_group = AgencyGroup.objects.filter(disaster=disaster).first()
        
        # Get the IDs of agencies in the group
            valuable_entry = list(agency_group.agencies.values_list('id', flat=True)) if agency_group else []

        # Prepare response data
            response_data = {
                "disaster": serializer.data,
                "group_name": agency_group.name if agency_group else None,
                "valuable_entry": valuable_entry
            }

            #from .consumers import DisasterConsumer  # Assuming your consumer is in the same directory
            from asyncio import run
            async def broadcast_disaster_update(disaster_data):
                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    "disaster_updates",
                    {
                        "type": "disaster.update",
                        "disaster_data": disaster_data
                    }
                )

            run(broadcast_disaster_update(response_data))
    
        
            return Response(response_data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            disaster = Disaster.objects.get(pk=pk)
        except Disaster.DoesNotExist:
            return Response({'error': 'Disaster not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DisasterSerializer(disaster, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            disaster = Disaster.objects.get(pk=pk)
        except Disaster.DoesNotExist:
            return Response({'error': 'Disaster not found'}, status=status.HTTP_404_NOT_FOUND)

        disaster.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        