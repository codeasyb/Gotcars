from django.shortcuts import render, redirect
from django.contrib import messages, auth
# https://docs.djangoproject.com/en/3.1/topics/auth/default/
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

def login(requests):

    if requests.method == "POST":
        username = requests.POST['username']
        password = requests.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(requests, user)
            messages.success(requests, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(requests, 'Invalid login credentials')
            return redirect('login')
    return render(requests, "accounts/login.html")

def logout(requests):
    
    if requests.method == "POST":
        auth.logout(requests)
        # messages.success(requests, 'You have succesfully logged out!')
        return redirect('home')
    return redirect('home')

def register(requests):
    
    if requests.method == 'POST':
        
        first_name = requests.POST['firstname']
        last_name = requests.POST['lastname']
        user_name = requests.POST['username']
        email = requests.POST['email']
        password = requests.POST['password']
        confirm_password = requests.POST['confirm_password']
        # Validate
        if password == confirm_password:
            # check for username
            if User.objects.filter(username=user_name).exists():
                # check for email
                messages.error(requests, 'User exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(requests, 'Email exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=user_name,
                        email=email,
                        password=password
                    )
                    user.save()
                    auth.login(requests, user)
                    messages.success(requests, 'You are now logged in!')
                    return redirect(requests, 'dashboard')
                    # messages.SUCCESS('You are now logged in!')
        else:
            messages.error(requests, 'Password does not mathc')
            return redirect('register')
    else:
        return render(requests, "accounts/register.html")

@login_required(login_url = 'login')
def dashboard(requests):
    user_inquiries = Contact.objects.order_by('-create_date').filter(user_id=requests.user.id)
    data = {
        'inquiries': user_inquiries,
    }
    return render(requests, "accounts/dashboard.html", data) 
