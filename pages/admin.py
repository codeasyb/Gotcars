from django.contrib import admin
from .models import Team
# thumbnail for admin purposes
from django.utils.html import format_html

# Customizing the admin dashboard for Teams
class TeamAdmin(admin.ModelAdmin):
    
    def thumbnail(self, object):
        return format_html("<img src='{}' width='40' style='border-radius:50px'/>".format(object.image.url))
    
    thumbnail.short_description = 'Image'
    list_display = ('id', 'thumbnail','first_name', 'designation', 'created_at')
    list_display_links = ('thumbnail',)
    # search field for your model to search people based on property
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation', 'created_at')
    

admin.site.register(Team, TeamAdmin)