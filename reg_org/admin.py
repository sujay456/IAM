from django.contrib import admin

from .models import Organization,IsRoot,PartOf
# Register your models here.

admin.site.register(Organization)
admin.site.register(IsRoot)
admin.site.register(PartOf)

