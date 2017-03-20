from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(SystemUser)

admin.site.register(GsmDevice)
admin.site.register(Patient)
admin.site.register(Practitioner)
admin.site.register(SmsData)

# Register your models here.
