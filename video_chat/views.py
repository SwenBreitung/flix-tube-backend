from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from video_chat.models import Chat, Message, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers


"""
Handles both GET and POST requests for a chat application.

- For POST requests: Creates a new message in the chat and returns the serialized message as JSON.
- For GET requests: Retrieves and displays all messages from a specific chat.

Requires the user to be logged in.

:param request: The HTTP request object.
:return: For POST requests, returns a JsonResponse with the serialized new message.
        For GET requests, returns an HTML response with chat messages.
"""
@login_required(login_url="/login/")
def index(request):
    if(request.method =='POST'):
        print(request.POST['textmessage'])
        my_chat = Chat.objects.get(id = 1)
        new_message = Message.objects.create(text= request.POST['textmessage'], chat = my_chat, author =request.user, receiver = request.user,)
        serialized_obj = serializers.serialize('json', [new_message,])
        return JsonResponse(serialized_obj[1:-1], safe = False)

    chat_messages = Message.objects.filter(chat__id = 1)
    print(chat_messages)
    return render(request, 'chat/index.html', {'name': 'Junus', 'chat_messages': chat_messages})



def login_view(request):
    redirect = request.GET.get('next')
    print(redirect)
    if(request.method =='POST'):
        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect','/chat/'))
        else:
            return render(request, 'auth/login.html',{'worngPassword':True, 'redirect':redirect})

    return render(request, 'auth/login.html',{'redirect':redirect})


"""
Handles user login requests.

- For POST requests: Authenticates the user with the provided username and password.
If authentication is successful, logs in the user and redirects them to the 'next' page or default page.
If authentication fails, displays an error message.

- For GET requests: Displays the login form, with an optional redirect URL.

:param request: The HTTP request object.
:return: For POST requests, an HttpResponseRedirect to the next page or '/chat/' if login is successful.
    If authentication fails or for GET requests, renders the login page with an optional redirect URL.
"""
def register_view(request):
    print('userinformation')
    if request.method == 'POST':
        print('userinformation')

        form = RegisterForm(request.POST)
        if form.is_valid():  
            form.save() 
            return redirect('/login/')  
        else:
            print(form.errors)  
    else:
        form = RegisterForm()
        print(form.errors)
    return render(request, 'auth/register.html', {'form': form})

