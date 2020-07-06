from django.contrib import admin

# Register your models here.
from backend.models import NemData


class NewDataAdmin(admin.ModelAdmin):
    search_fields = ('serialNumber', )


admin.site.register(NemData, NewDataAdmin)
