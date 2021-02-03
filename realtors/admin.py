from django.contrib import admin

from .models import Realtor

class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_realtor_name', 'get_realtor_email', 'hire_date')
    list_display_links = ('id', 'get_realtor_name')
    search_fields = ('get_realtor_name',)
    list_per_page = 25

admin.site.register(Realtor, RealtorAdmin)