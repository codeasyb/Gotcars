from django.contrib import admin
from .models import Car
from django.utils.html import format_html

class CarAdmin(admin.ModelAdmin):
    
    def thumbnail(self, object):
        return format_html("<img src='{}' width='60' style='border-radius:50px'/>".format(object.car_photo.url))
    
    thumbnail.short_description = 'Photo'
        
    list_display = ('id', 'thumbnail','car_title', 'price', 'milage', 'created_date', 'is_featured')
    list_display_links = ('thumbnail',)
    list_editable = ('is_featured',)
    search_fields = ('id', 'car_title', 'model', 'city', 'body_style', 'year')
    list_filter = ('city', 'created_date', 'model')

admin.site.register(Car, CarAdmin)