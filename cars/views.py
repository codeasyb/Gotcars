from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Car

def cars(requests):
    
    car_list  = Car.objects.all().order_by('-created_date')
    paginator = Paginator(car_list, 2)
    page = requests.GET.get('page')
    paged_cars = paginator.get_page(page)

    data = {
        'car_list': car_list,
        'car_list': paged_cars,
    }
    return render(requests, 'cars/cars.html', data)

def car_details(requests, id):
    
    single_car = get_object_or_404(Car, pk=id)
    
    data = {
        'single_car': single_car
    }
    return render(requests, 'cars/car_details.html', data)

def search(requests):
    
    car_list = Car.objects.order_by('-created_date')
    
    if 'keyword' in requests.GET:
        keyword = requests.GET['keyword']
        if keyword:
            car_list = car_list.filter(description__icontains=keyword)
            
    if 'model' in requests.GET:
        model = requests.GET['model']
        if model:
            car_list = car_list.filter(model__iexact=model)

    if 'state' in requests.GET:
        state = requests.GET['state']
        if state:
            car_list = car_list.filter(state__iexact=state)

    if 'year' in requests.GET:
        year = requests.GET['year']
        if year:
            car_list = car_list.filter(year__iexact=year)

    if 'body_style' in requests.GET:
        body_style = requests.GET['body_style']
        if body_style:
            car_list = car_list.filter(body_style__iexact=body_style)
            
    if 'min_price' in requests.GET:
        min_price = requests.GET['min_price']
        max_price = requests.GET['max_price']
        if max_price:
            car_list = car_list.filter(price__gte=min_price, price__lte=max_price)
    
    model_fields = Car.objects.values_list('model', flat=True).distinct()
    make_fields = Car.objects.values_list('make', flat=True).distinct()
    state_fields = Car.objects.values_list('state', flat=True).distinct()
    year_fields = Car.objects.values_list('year', flat=True).distinct()
    type_fields = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_fields = Car.objects.values_list('transmission', flat=True).distinct()
    
    data = {
        'car_list': car_list,
        'model_fields': model_fields,
        'make_fields': make_fields,
        'state_fields': state_fields,
        'year_fields': year_fields,
        'type_fields': type_fields,    
        'transmission_fields': transmission_fields
    }
    return render(requests, 'cars/search.html', data)    