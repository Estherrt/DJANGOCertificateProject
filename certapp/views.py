from django.shortcuts import render,redirect
from .models import Participant
from .forms import PForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin,logout as authlogout


# Create your views here.
def form_login(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user:
            print(user)
            authlogin(request,user)
            return redirect('create')
        else:
            error_message="Invalid Credentials"
    return render(request,'login.html',{'error_message':error_message})

def form_signup(request):
    users=None
    error_message=None

    if request.POST:
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        try:
            users=User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
        except Exception as e:
            error_message=str(e)
            

    return render(request,'signup.html',{'user':users,'error_message':error_message})

def form_logout(request):
    authlogout(request)
    return redirect('login')

def form_create(request):
    form=PForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        participant = form.save(commit=False)
        participant.user = request.user  # Associate the participant with the current user
        participant.save()
    else:
        form=PForm()
    context={'form':form}
    return render(request,"create.html",context)

@login_required(login_url='login') 
def form_display(request):
    data=None
    recent_visits=request.session.get('recent_visits',[])
    count=request.session.get('count',0)
    count=int(count)
    count+=1
    recent_data_set=Participant.objects.filter(pk__in=recent_visits, user=request.user)
    request.session['count']=count
    data = Participant.objects.filter(user=request.user)
    response=render(request,'display.html',{'data':data,'visits':count,'recent_data_set':recent_data_set})
    
    
    return response


@login_required(login_url='login') 
def form_delete(request,pk):
    instance_to_be_deleted=Participant.objects.get(pk=pk)
    instance_to_be_deleted.delete()
    return HttpResponseRedirect(reverse('display'))

@login_required(login_url='login') 
def form_edit(request,pk):
    instance_to_be_edited=Participant.objects.get(pk=pk)
    if request.method == 'POST':
        form = PForm(request.POST, instance=instance_to_be_edited)
        if form.is_valid():
            form.save()
            return redirect('display')
    else:
        form = PForm(instance=instance_to_be_edited)

    recent_visits = request.session.get('recent_visits', [])
    if pk not in recent_visits:
        recent_visits.insert(0, pk)
    request.session['recent_visits'] = recent_visits

    content = {'form': form}
    return render(request, 'create.html', content)