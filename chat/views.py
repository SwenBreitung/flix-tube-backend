from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from chat.models import Chat, Message, RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers

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


# Create your views here.
