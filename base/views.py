from django.shortcuts import render,redirect
from .models import Room,Topic,User,Message
from django.db.models import Q
from django.http import HttpResponse
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def registerUser(request):

    # page='register'
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})
def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__contains=q)|
                              Q(description__icontains=q)|
                              Q(name__icontains=q)
                              )
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,
             'room_messages':room_messages}
    return render(request,"base/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    roommessages = room.message_set.all()
    participents=room.participents.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participents.add(request.user)
        return redirect('room',pk=room.id)
    

    context={'room':room,'roommessages':roommessages,'participents':participents}
    return render(request,"base/room.html",context)
@login_required(login_url='/login')
def createRoom(request):
    form=RoomForm
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    roommessages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':roommessages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('your not allowed to do this')
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('your not allowed to do this')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='/login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('your not allowed to do this')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})