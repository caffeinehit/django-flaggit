from django.contrib import admin
from flaggit.models import Flag, FlagInstance

class FlagAdmin(admin.ModelAdmin):
    list_filters = ('status',)
    list_display = ('status', 'num_flags', 'content_object', 'created',
        'reviewer', 'reviewed', 'num_flags')

admin.site.register(Flag, FlagAdmin)
admin.site.register(FlagInstance)

