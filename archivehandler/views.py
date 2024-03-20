import re
from datetime import datetime
from django.db.models import Count
from .models import Friend, Chat, Message
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

SYSTEM_MESSAGES = [
    "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.",
    "",
    "Messages and calls are end",
    "<Media omitted>"
]
date_pattern = r'^\d{4}-\d{2}-\d{2}'

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
                return redirect('dashboard')
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

@login_required
def dashboard(request):
    total_friends_count = str(Friend.objects.filter(user=request.user).count()).zfill(2)
    # Get the total count of chats associated with the current user's friends
    total_chats_count = str(Chat.objects.filter(friend__user=request.user).count()).zfill(2)
    # Get the friend with the maximum number of messages exchanged with the current user
    friend_with_max_messages = Friend.objects.filter(chats__friend__user=request.user) \
                                           .annotate(num_messages=Count('chats__messages')) \
                                           .order_by('-num_messages', 'id') \
                                           .first()
    friends_chats = get_friends_chats(request)
    context = {
        'total_friends_count': total_friends_count,
        'total_chats_count': total_chats_count,
        'friend_with_max_messages': friend_with_max_messages,
        'friends_chats': friends_chats,
    }
    return render(request, "dashboard.html", context)

@login_required
def add_friend(request):
    friends_chats = get_friends_chats(request)
    context = {
        'friends_chats': friends_chats,
    }

    if request.method == "POST":
        name = request.POST['name']
        display_name = request.POST['display_name']
        verification = verify_names(name, display_name)
        if verification == 'Verified':
            try:
                Friend.objects.create(name=name, display_name=display_name, user=request.user)
                return redirect('dashboard')
            except Exception as e:
                context["error"] = e
                context['form_values'] = {"name": name, "display_name": display_name}
                return render(request, "add_friend.html", context)
        else:
            context["error"] = verification
            context['form_values'] = {"name": name, "display_name": display_name}
            return render(request, "add_friend.html", context)
    return render(request, "add_friend.html", context)

@login_required
def upload_chat(request):
    context = {}
    friends_chats = get_friends_chats(request)

    context["friends"] = Friend.objects.filter(user=request.user)
    context['friends_chats'] = friends_chats

    if request.method == 'POST': 
        verification, file_content = verify_chats(request)
        if verification == 'Verified':
            chats, chat = process_chat(request, file_content, context)
            create_message_for_friend(chats, chat)
            return redirect('dashboard') 
        else:
            context['error'] = verification
            render(request, 'upload_chat.html', context)

        
    return render(request, 'upload_chat.html', context)

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

def verify_names(complete_name, display_name):
    """
    Verify the completeness and validity of a friend's complete name and display name.

    Args:
    complete_name (str): The complete name of the friend.
    display_name (str): The display name of the friend.

    Returns:
    str: A message indicating the verification result.
    """
    # Check if complete_name is provided
    if not complete_name:
        return "Complete name is required."

    # Check if complete_name contains only alphabetic characters and spaces
    if not complete_name.replace(' ', '').isalpha():
        return "Complete name should contain only alphabetic characters and spaces."

    # Check if display_name is provided
    if not display_name:
        return "Display name is required."

    # Check if display_name contains only alphabetic characters, spaces, underscores, and numbers
    if not all(char.isalpha() or char.isspace() or char.isdigit() or char == '_' for char in display_name):
        return "Display name should contain only alphabetic characters, spaces, underscores, and numbers."

    # All checks passed
    return "Verified"

def verify_chats(request):
    friend_slug = request.POST['friend_slug']
    name = request.POST['name'] 

    if not name:
        return "Complete name is required.", None

    if not friend_slug:
        return 'Please select a friend from the list', None

    if not Friend.objects.filter(user=request.user, slug=friend_slug).exists():
        return 'Choose one of your friends or Create a new one', None
    
    if not 'chat_file' in request.FILES:
        return 'You must choose a file from your system', None
    
    uploaded_file = request.FILES['chat_file']
    if not uploaded_file.name.endswith('.txt'):
        return 'File must be a .txt file', None

    # Read the file content
    file_content = uploaded_file.read().decode('utf-8')
    
    # Reset file pointer to the beginning of the file
    uploaded_file.seek(0)
    
    if name not in file_content:
        return 'Write your username of WhatsApp. You can copy from file', None
    
    return 'Verified', file_content

def extract_dates(first_line, last_line):
    # Extracting start date from the first line
    start_date_str = first_line.split('-')[0].strip().replace('\u202f', ' ')
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y, %I:%M %p')

    # Extracting end date from the last line
    end_date_str = last_line.split('-')[0].strip().replace('\u202f', ' ')
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y, %I:%M %p')

    # # Formatting the dates
    start_date_formatted = start_date.strftime('%b %d, %Y')
    end_date_formatted = end_date.strftime('%b %d, %Y')

    return start_date_formatted, end_date_formatted

def extract_datetime(complete_datetime):
    date_time_split = complete_datetime.split(',')
    # Extracting start date from the first line
    start_date_str = complete_datetime.strip().replace('\u202f', ' ')
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y, %I:%M %p')
    start_date_formatted = start_date.strftime('%b %d, %Y')

    dt = datetime.strptime(str(start_date), "%Y-%m-%d %H:%M:%S")
    am_pm_time = dt.strftime("%I:%M %p")
    
    return start_date_formatted, am_pm_time

def process_chat(request, file_content, context):
    friend = Friend.objects.get(user=request.user, slug=request.POST['friend_slug'])
    first_line = None
    last_line = ''
    chats = []

    for line in file_content.split('\n'):
        if first_line is None:
            first_line = line
        
        if line.strip() != '':
            last_line = line

        try:
            chat_dict = {}
            parts_of_line = line.split('-')
            chat_dict['chat_date'], chat_dict['chat_time'] = extract_datetime(parts_of_line[0])

            if parts_of_line[1].strip() in SYSTEM_MESSAGES:
                continue

            right_part_list = parts_of_line[1].split(':')
            if right_part_list[1].strip() in SYSTEM_MESSAGES:
                continue

            chat_dict['message'] = right_part_list[1].strip()
            if right_part_list[0].strip() == request.POST['name']:
                chat_dict['is_user'] = True
            else:
                chat_dict['is_user'] = False
            
            chats.append(chat_dict)
        except:
            if not bool(re.match(date_pattern, line)):
                chats[-1]['message'] += '\n' + line
    
    start_date, end_date = extract_dates(first_line, last_line)

    try: 
        chat = Chat.objects.create(friend=friend, start_date=start_date, end_date=end_date)
        chat.save()
    except Exception as e:
        context['error'] = e
        return render(request, 'upload_chat.html', context)

    return chats, chat

def create_message_for_friend(chats, chat_object):
    for chat in chats:
        try:
            message = Message.objects.create(date=chat['chat_date'], time=chat['chat_time'], chat=chat_object, is_user=chat['is_user'], text=chat['message'])
            message.save()
        except Exception as e:
            pass

def get_friends_chats(request):
    friends = Friend.objects.filter(user=request.user)
    friends_chats = {}
    for friend in friends:
        chats = Chat.objects.filter(friend=friend)
        friends_chats[friend] = chats
    return friends_chats
