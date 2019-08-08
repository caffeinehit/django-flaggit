from django.contrib import admin
from flaggit.models import Flag, FlagInstance, CONTENT_APPROVED, \
    CONTENT_REJECTED
from datetime import datetime

class FlagAdmin(admin.ModelAdmin):
    readonly_fields = ('related_object', 'num_flags')
    list_filter = ('status',)
    list_display = ('status', 'created',
        'reviewer', 'reviewed', 'num_flags')
    
    actions = ['approve', 'reject']
    actions_on_bottom = True
    
    def num_flags(self, obj):
        return obj.flags.all().count()
    
    def approve(self, request, queryset):
        for obj in queryset:
            obj.status = CONTENT_APPROVED
            obj.reviewer = request.user
            obj.reviewed = datetime.now()
            obj.save()
    approve.short_description = "Approve content on selected flags. (Save content)"
    
    def reject(self, request, queryset):
        for obj in queryset:
            obj.status = CONTENT_REJECTED
            obj.save()
    reject.short_description = "Reject content on selected flags. (Delete content)"    
    
    def get_actions(self, request):
        actions = super(FlagAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def related_object(self, obj):                                                                                     
        return f"{obj.content_object}"   

admin.site.register(Flag, FlagAdmin)
admin.site.register(FlagInstance)

