from django.contrib import admin
from .models import (Siege, Siege_army, Army, City)
# Register your models here.
admin.site.register(Siege)
admin.site.register(Siege_army)
admin.site.register(Army)
admin.site.register(City)

