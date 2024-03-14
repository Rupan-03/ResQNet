from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    AreaOfExpertiseListView, AreaOfExpertiseDetailView,
    ResourceListView, ResourceDetailView,
    ResourceQuantityListView, ResourceQuantityDetailView,
    RescueAgencyRegisterView, RescueAgencyDetailView,
    UserLoginView, RescueAgencyUpdateLastActivityView,
    RescueAgencyListView,AddResourceQuantityView,UpdateResourceQuantityView,DeleteResourceQuantityView,
    HospitalListView,HospitalDetailView,SchoolListView,SchoolDetailView,DisasterAPIView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),

    path('rescue-agencies/register/', RescueAgencyRegisterView.as_view(), name='rescue-agency-register'),
    
    path('resource-quantities/', ResourceQuantityListView.as_view(), name='resource-quantity-list'),
    
    path('resource-quantities/add/', AddResourceQuantityView.as_view(), name='add-resource-quantity'),
    
    path('resource-quantities/update/', UpdateResourceQuantityView.as_view(), name='update-resource-quantity'),
    
    path('resource-quantities/delete/', DeleteResourceQuantityView.as_view(), name='delete-resource-quantity'),
    
    path('rescue-agencies/<int:pk>/update-last-activity/', RescueAgencyUpdateLastActivityView.as_view(), name='update-last-activity'),

    #above are important API endpoint 
    path('hospitals/', HospitalListView.as_view(), name='hospital-list'),

    path('hospitals/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),

    path('schools/', SchoolListView.as_view(), name='school-list'),
    
    path('schools/<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),
    
    #above are endpoints for CURD of hospitals and schools

    path('disasters/', DisasterAPIView.as_view(), name='disaster-list-create'),
    
    path('disasters/<int:pk>/', DisasterAPIView.as_view(), name='disaster-detail'),
    #above path to handle disaster data
    path('resource-quantities/<int:pk>/', ResourceQuantityDetailView.as_view(), name='resource-quantity-detail'),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path('expertises/', AreaOfExpertiseListView.as_view(), name='area-of-expertise-list'),
    
    path('expertises/<int:pk>/', AreaOfExpertiseDetailView.as_view(), name='area-of-expertise-detail'),
    
    path('resources/', ResourceListView.as_view(), name='resource-list'),
    
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    
    path('rescue-agencies/', RescueAgencyListView.as_view(), name='rescue-agency-list'),
    
    path('rescue-agencies/<int:pk>/', RescueAgencyDetailView.as_view(), name='rescue-agency-detail'),

]
    