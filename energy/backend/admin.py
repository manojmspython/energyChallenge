from django.contrib import admin

from backend.models import NemData


class NewDataAdmin(admin.ModelAdmin):
    """
    The model helps in creating a search item for the NemData model in the
    Django Admin site based on serialNumber.
    """
    search_fields = ('serialNumber', )


admin.site.register(NemData, NewDataAdmin)
