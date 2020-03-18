from django.contrib import admin

# Register your models here.
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from portfolio.models import Profile, Expertise

@admin.register(Profile)
class ProfileAdmin(LeafletGeoAdmin):
    model = Profile
    list_display = ['first_name', 'last_name', 'get_email', 'phone']
    search_fields = ['first_name', 'last_name', 'phone', 'user__email']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = '-user__id'

    def get_queryset(self, request):
        """
        Filter Profile Queryset based on user status.
        :return: If user is superuser, return all Profile. If not, only return associated Profile.
        """
        if request.user.is_superuser == True:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        """
            Set user field as readonly, based on user status.
            Each profile is associated with CustomUser through user field.
            :return: If user is not superuser, set user field as readonly so user cannot edit it.
                     If superuser, user can edit all field.
        """
        if request.user.is_superuser == False:
            return self.readonly_fields + ('user',)
        return self.readonly_fields

admin.site.register(Expertise)