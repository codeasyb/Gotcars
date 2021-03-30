from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages

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
    
    if requests.method == 'POST':
        name = requests.POST['name']
        email = requests.POST['email']
        subject = requests.POST['subject']
        phone = requests.POST['phone']
        message = requests.POST['message']
        
        #https://django.readthedocs.io/en/stable/topics/email.html
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        email_subject = 'You have a new message from Carzone website regarding '+ subject
        message_body = 'Name: ' + name + '\nEmail: ' + email + '\nPhone: ' + phone + '\nMessage: ' + message
        send_mail(
            email_subject,
            message_body,
            'techamir25@gmail.com',
            [admin_email],
            fail_silently=False,
        )
        messages.success(requests, 'Thank you for contacting us. We will get back to you soon')
        return redirect('contact')
        
    return render(requests, 'navlinks/contact.html')