from django.shortcuts import render, redirect
from .forms import NewUserForm, User
from .models import UserPersonal
from django.contrib import messages
from django.contrib.auth import login as authLogin, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random


CODE = "123"


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # judge whether this is an administrator
        if username == 'admin' and password == '123456':
            print("Entering administration page...")
            return redirect("/administration/user/")

        o = User.objects.filter(username=username)
        # check username exist
        if o:
            # check password
            check = authenticate(request, username=username, password=password)
            user_for_check = User.objects.get(username=username)
            print(user_for_check.is_active)

            if check:
                user_for_check = User.objects.get(username=username)
                # check if it's the first time to login
                if user_for_check.is_active:
                    # it's a old user, login directly
                    authLogin(request, check)
                    return redirect("/")

                # it's a new user, verify email
                else:
                    print('It is the first time')
                    randomCode = sendVerifyEmail(user_for_check)
                    return render(request, "login.html",
                                  {'isNew': True, 'user': user_for_check, 'randomCode': randomCode})

            # wrong password, print hint message
            else:
                print('wrong password')
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "This username not exists.")

    return render(request, "login.html", {'isNew': False})

def firstLogin(request, nid):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')

        # check password
        if authenticate(request, username=username, password=password):
            # check verification code
            print('ver', CODE)
            if code == CODE:
                print('code is right')
                user = User.objects.get(id=nid)
                # set user status to 'active'
                user.is_active = True
                user.save()

                # successful login
                authLogin(request, user)
                return redirect("/")
            else:
                messages.error(request, "The verification code is wrong.")
                return render(request, "login.html", {'isNew': True, 'user': User.objects.get(id=nid)})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", {'isNew': True, 'user': User.objects.get(id=nid)})

def register(request):
    form = NewUserForm()
    if request.method == 'POST':
        print(request.POST.get('userType'))
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save()

            user = UserPersonal()

            # set un-active status to new user
            current_user = getLastUser(request)
            current_user.is_active = False
            current_user.save()

            user.user_form = current_user
            user.user_type = request.POST.get('userType')
            user.save()

            messages.success(request, "Registration successful.")
            return redirect("./login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    context = {'form': form}
    return render(request, "register.html", context)
@login_required
def UserProfile(request):
    user = User.objects.get(id=request.user.id)
    if user:
        return render(request, 'UserProfile.html', {'user': user})
    else:
        return render(request, "login.html")


def EditProfile(request, nid):
    print(nid)

    if request.method == 'GET':
        user = User.objects.get(pk=nid)
        return render(request, 'EditProfile.html', {'user': user})

    if request.method == 'POST':
        updateInfo(request, nid)

    user = User.objects.get(pk=nid)
    return render(request, 'UserProfile.html', {'user': user})

def updateInfo(request, nid):
    user = User.objects.get(pk=nid)
    print('Updating user: ', user)
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.save()

def getLastUser(request):
    users = User.objects.all()
    return users[len(users)-1]

def sendVerifyEmail(user):
    print('send!')
    randomCode = generateCode()
    title = "SpareFoodShare - " + " Verification code for your first login"
    msg = "Hi " + user.username + ",\n\n        Welcome to join SpareFoodShare! \n\n" \
          "        The following is your verification code: " + randomCode +\
          "\n\n\n\n        We have been looking forward to your joining for a long time. Start your sharing at http://localhost:8000." \
          "\n\n\n\nBest,\nSpareFoodShare"

    send_mail(title, msg, settings.EMAIL_HOST_USER, [user.email])
    return randomCode

def generateCode():
    code = ""
    for i in range(4):
        code += str(random.randint(0, 9))

    global CODE
    CODE = code
    print(CODE)

    return code

def checkPassword(name, password_input):
    user = User.objects.get(username=name)
    print(user.username)
    print(user.password)
    if user.username == name and user.password == password_input:
        return True
    else:
        return False
