from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AreaOfExpertise, Resource, ResourceQuantity,Hospital,School,AgencyGroup,Disaster

class ResourceQuantityInline(admin.TabularInline):
    model = ResourceQuantity
    extra = 1

class CustomUserAdmin(UserAdmin):
    # Customize the display fields if needed
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined', 'location', 'area_of_expertise', 'last_activity_type', 'last_activity_location', 'last_activity_timestamp', 'role')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    # Add the additional fields to the UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('location', 'area_of_expertise', 'last_activity_type', 'last_activity_location', 'last_activity_timestamp', 'role'),
        }),
    )

    # Add ManyToManyField resources separately using filter_horizontal
    filter_vertical = ('resources', )

    inlines = [ResourceQuantityInline]

class AgencyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'disaster', 'dissolution_time')  
    # Add filter_horizontal or filter_vertical to display associated agencies
    filter_horizontal = ('agencies',)    # Customize displayed fields

      # Set column header name

# Register AgencyGroup with the admin site
#admin.site.register(AgencyGroup, AgencyGroupAdmin)

# Register the models with the admin site
admin.site.register(AreaOfExpertise)
admin.site.register(Resource)
admin.site.register(ResourceQuantity)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hospital)
admin.site.register(School)
admin.site.register(AgencyGroup,AgencyGroupAdmin)
admin.site.register(Disaster)
