from django.contrib import admin
from .models import Registeration,TaxiBooking,TaxiDetails,DriverRegisteration,TaxiDetailsHistory
from django.contrib.auth.models import Group,User

admin.site.unregister(Group)
admin.site.unregister(User)


# Register your models here.
admin.site.site_header = 'Taxi Booking Administration'                   
admin.site.index_title = 'Admin Panel'             
admin.site.site_title = 'Taxi Booking Administration'

# admin.site.register([TaxiBooking,Registeration,TaxiDetails,TaxiDetailsHistory,DriverRegisteration])

class TaxiBookingAdmin(admin.ModelAdmin):
    model=TaxiBooking
    list_display = ('user','taxi','booked_time','is_booked','is_finished')

admin.site.register(TaxiBooking,TaxiBookingAdmin)

class TaxiDetailsHistoryAdmin(admin.ModelAdmin):
    model=TaxiDetailsHistory
    list_display=('driver','taxi','user','booked')

admin.site.register(TaxiDetailsHistory,TaxiDetailsHistoryAdmin)

class RegisterationAdmin(admin.ModelAdmin):
    model=Registeration
    list_display = ('name','email','mobile','city','country','pincode')

admin.site.register(Registeration,RegisterationAdmin)

class DriverRegisterationAdmin(admin.ModelAdmin):
    model=DriverRegisteration
    list_display=('name','email','mobile','badge_number')

admin.site.register(DriverRegisteration,DriverRegisterationAdmin)

class TaxiDetailsAdmin(admin.ModelAdmin):
    model=TaxiDetails
    list_display=('taxi_no','driver','source','destination','price','is_booked','is_accepted')

admin.site.register(TaxiDetails,TaxiDetailsAdmin)