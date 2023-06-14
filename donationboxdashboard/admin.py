from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Donor)
admin.site.register(Volunteer)
admin.site.register(DonationArea)
admin.site.register(Donation)
admin.site.register(Gallery)
admin.site.register(Request)
admin.site.register(VolunteerProfile)
