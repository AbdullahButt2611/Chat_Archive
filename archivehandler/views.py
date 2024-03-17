from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate

# Create your views here.
def index(request):
    return render(request, "index.html")

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        verification = verify_login(request)
        if verification == "Verified":
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request, 'login.html', {"error": "Invalid Credentials! Please Try Again."})
        else:
            return render(request, 'login.html', {"error": verification})

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    context = {}

    # if request.method == "POST":
    #     firstname = request.POST['firstname']
    #     lastname = request.POST['lastname']
    #     email = request.POST['email']
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     country = request.POST['country']
    #     dob = request.POST['dob']
    #     verification = verify_signup(request)

    #     if(verification == "Verified"):
    #         try:
    #             data = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
    #             data.save()
    #             user = UserMeta.objects.create(user=data, country=country, dob=dob)
    #             user.save()
    #             return redirect('login')

    #         except Exception as e:
    #             context['error'] = "Username is already taken"
    #             return render(request, 'signup.html', context)
    #     else:
    #         context['form_values'] = {"firstname": firstname, "lastname": lastname, "email": email, "username": username}
    #         context['error'] = verification
    #         return render(request, 'signup.html', context)


    return render(request, 'user_registration.html', context)

# ======================    HELPER FUNCTIONS    =========================

def verify_signup(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    country = request.POST['country']
    dob = request.POST['dob']
    
    if not firstname.strip() or not lastname.strip():
        return "Firstname and Lastname cannot be empty."
    
    if not firstname.isalpha() or not lastname.isalpha():
        return "Firstname and Lastname should only contain alphabet."
    
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Email Should be in a proper format"
    
    if len(username) < 4 and len(username) > 16:
        return "Username length should be between 3 and 15 characters."
    
    print("Username ", username.isalnum())
    if not (username.isalnum() or '_' in username):
        return "Username can only contain alphanumeric characters or underscores."
    
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
    username = request.POST['username']
    password = request.POST['password']
    if username and password:
        return "Verified"
    else:
        return "Username and Password are Required for Logging In"
