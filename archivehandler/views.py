import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

# Create your views here.
def index(request):
    return render(request, "index.html")

def login_user(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        verification = verify_login(request)
        if verification == "Verified":
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request, 'user_registration.html', {"login_error": "Invalid Credentials! Please Try Again."})
        else:
            return render(request, 'user_registration.html', {"login_error": verification})

    return render(request, 'user_registration.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    context = {}

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        print(name, email, password)
        verification = verify_signup(request)

        if(verification == "Verified"):
            try:
                data = User.objects.create_user(first_name=name, email=email, username=email, password=password)
                data.save()
                return redirect('login')

            except Exception as e:
                context['error'] = "Email is already taken"
                return render(request, 'user_registration.html', context)
        else:
            context['form_values'] = {"name": name,  "email": email}
            context['signup_error'] = verification
            return render(request, 'user_registration.html', context)


    return render(request, 'user_registration.html', context)

def dashboard(request):
    return render(request, "dashboard.html")

# ======================    HELPER FUNCTIONS    =========================

def verify_signup(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    
    if not name.strip():
        return "Name Field cannot be empty."
    
    if not all(char.isalpha() or char.isspace() for char in name):
        return "Name should only contain alphabets and spaces."
    
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Email Should be in a proper format"
    
    if len(password) < 8:
        return "Password length should be at least 8 characters."
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not has_upper or not has_lower or not has_digit:
        return "Password should contain at least one uppercase letter, one lowercase letter, and one digit."
    
    try:
        user = User.objects.get(email__iexact=email)
        if user is not None:
            return "Email is already in use"
    except:
        pass

    return "Verified"

def verify_login(request):
    email = request.POST['email']
    password = request.POST['password']
    if email and password:
        return "Verified"
    else:
        return "Email and Password are Required for Logging In"
