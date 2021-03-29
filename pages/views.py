from django.shortcuts import render
from .models import Team
from cars.models import Car

def home(requests):
    teams = Team.objects.all() 
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    cars = Car.objects.order_by('-created_date')
    # search_fields = Car.objects.values('model', 'state', 'year', 'body_style') nota good way to implement filter
    model_fields = Car.objects.values_list('model', flat=True).distinct()
    state_fields = Car.objects.values_list('state', flat=True).distinct()
    year_fields = Car.objects.values_list('year', flat=True).distinct()
    type_fields = Car.objects.values_list('body_style', flat=True).distinct()
    make_fields = Car.objects.values_list('make', flat=True).distinct()
    
    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'cars': cars,
        # 'search_fields': search_fields
        'model_fields': model_fields,
        'state_fields': state_fields,
        'year_fields': year_fields,
        'type_fields': type_fields,
        'make_fields': make_fields,
    }
    return render(requests, 'index.html', data)

def about(requests):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(requests, 'navlinks/about.html', data)

def services(requests):
    return render(requests, 'navlinks/services.html')

def contact(requests):
    return render(requests, 'navlinks/contact.html')