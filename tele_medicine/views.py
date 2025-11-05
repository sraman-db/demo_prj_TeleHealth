from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser, MedicalCenter, ContactMessage
import json
from django.db import connection
from datetime import datetime


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def navigation(request):
    # Load centers via ORM
    centers = MedicalCenter.objects.all()
    centers_data = []
    
    for c in centers:
        try:
            lat = float(c.latitude) if c.latitude is not None else None
            lng = float(c.longitude) if c.longitude is not None else None
        except (ValueError, TypeError):
            continue
            
        if lat is None or lng is None:
            continue
            
        centers_data.append({
            'name': c.name,
            'latitude': lat,
            'longitude': lng,
            'center_type': c.center_type,
        })

    context = {
        'medical_centers': json.dumps(centers_data),
        'bhubaneswar_lat': 20.2961,
        'bhubaneswar_lng': 85.8245
    }
    return render(request, 'tele_medicine/navigation.html', context)


def diagnosis(request):
    return render(request, 'tele_medicine/Diagnosis.html')

def home(request):
    return render(request, 'tele_medicine/home.html')

def about(request):
    return render(request, 'tele_medicine/about.html')

def services(request):
    return render(request, 'tele_medicine/services.html')

def main_page(request):
    return render(request, 'tele_medicine/mainPage.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO contact_message (name, email, message, timestamp)
                    VALUES (%s, %s, %s, %s)
                """
                values = (name, email, message, datetime.now())
                cursor.execute(query, values)
                connection.commit()

            return render(request, 'tele_medicine/contact.html', {'success': True})

        except Exception as e:
            print("Database Error:", e)
            return render(request, 'tele_medicine/contact.html', {'success': False, 'error': True})

    return render(request, 'tele_medicine/contact.html', {'success': False, 'error': False})
def signup(request):
    if request.method == 'POST':
        # Collect data safely
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Basic validation
        if not (first_name and last_name and email and password):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'tele_medicine/signup.html')

        # Hash the password before saving
        hashed_password = make_password(password)

        try:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date_of_birth=date_of_birth if date_of_birth else None,
                phone_number=phone_number,
                password=hashed_password,
            )
            user.save()
        except IntegrityError:
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'tele_medicine/signup.html')

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    return render(request,'tele_medicine/signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user and user.password and check_password(password, user.password):
                # Set up session
                request.session['user_id'] = user.id
                # messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('mainpage')
            else:
                messages.error(request, 'Invalid credentials')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'tele_medicine/login.html')

def doctors(request):
    """
    Display the doctors listing page
    """
    return render(request, 'tele_medicine/doctors.html')