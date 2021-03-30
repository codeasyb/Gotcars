from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#https://stackoverflow.com/questions/58174003/errno-8-nodename-nor-servname-provided-or-not-known-when-using-django-ses

@login_required(login_url = 'login')
def inquiry(requests):
    
    if requests.method == "POST":
        first_name = requests.POST['first_name']
        last_name = requests.POST['last_name']
        user_id = requests.POST['user_id']
        car_id = requests.POST['car_id']
        car_title = requests.POST['car_title']
        customer_interest = requests.POST['customer_interest']
        email = requests.POST['email']
        phone = requests.POST['phone']
        state = requests.POST['state']
        city = requests.POST['city']
        message = requests.POST['message']
        
        if requests.user.is_authenticated:
            user_id = requests.user.id
            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(requests, 'You have already made an iquire about this. Please wait for someone to get abck to you')
                return redirect('/cars/'+car_id)
        
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            car_id=car_id,
            car_title=car_title,
            customer_interest=customer_interest,
            email=email,
            phone=phone,
            state=state,
            city=city,
            message=message
        )
        #https://django.readthedocs.io/en/stable/topics/email.html
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        
        send_mail(
            'New Car inquiry',
            'You have a new car inquiry about '+ str(car_title)+' this car. Please check',
            'techamir25@gmail.com',
            [admin_email],
            fail_silently=False,
        )
        contact.save()
        messages.success(requests, 'Thank you for your inquiry. We will get back to you')
        return redirect('/cars/'+car_id)
    else:
        return redirect(requests, 'home.html')        
