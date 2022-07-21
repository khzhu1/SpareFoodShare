from django.shortcuts import render
from django.contrib.auth import get_user_model
from chatbox.models import Message
from django.contrib.auth.decorators import login_required

# get user model
User = get_user_model()

# login required decorator to check if user is logged in, if not redirect to login page
@login_required
# view to display the list of user who sent messages to request user
def index(request):
    users = Message.objects.filter(sendto= request.user.username).values('sender').distinct()
    users = User.objects.filter(username__in=users).exclude(username=request.user.username)
    return render(request, 'index.html', context={'users': users})

@login_required
# view to assign the user to a chat box wrt the selected user
def chatPage(request, username):
    users = Message.objects.filter(sendto= request.user.username).values('sender').distinct()
    users = User.objects.filter(username__in=users).exclude(username=request.user.username)
    user_obj = User.objects.get(username=username)

    if int(request.user.id) > (user_obj.id):
        room_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        room_name = f'chat_{user_obj.id}-{request.user.id}'
    message = Message.objects.filter(thread_name=room_name)
    return render(request, 'main_chat.html', context={'user': user_obj, 'users': users, 'messages': message})




