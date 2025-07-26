from django.contrib import admin
from .models import Pet

# Register your models here.


class PetModelAdmin(admin.ModelAdmin):
    pass


admin.sites.site.register(Pet, PetModelAdmin)
