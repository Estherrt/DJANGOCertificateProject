from django.shortcuts import render,redirect
from .models import Participant
from .forms import PForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin,logout as authlogout
from django.templatetags.static import static

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import utils
from reportlab.lib.units import cm 
from reportlab.platypus import Frame, Image 

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
            return redirect(reverse('login'))
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

    # recent_visits = request.session.get('recent_visits', [])
    # if pk not in recent_visits:
    #     recent_visits.insert(0, pk)
    # request.session['recent_visits'] = recent_visits

    content = {'form': form}
    return render(request, 'create.html', content)

def get_image(path, width=1*cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return path, width, width * aspect


def generate_certificate(request,pk):
    buf=io.BytesIO()
    bg='C:/Django_project/cert/static/image/cert_template.png'

    c=canvas.Canvas(buf,pagesize=landscape(A4))

    document_width, document_height = landscape(A4)
    img = utils.ImageReader(bg)
    image_width, image_height = img.getSize()
    image_aspect = image_height / float(image_width)

    print_width = document_width
    print_height = document_width * image_aspect
    c.drawImage(bg, document_width - print_width, document_height - print_height, width=print_width,height=print_height)

    participant=Participant.objects.get(pk=pk)

    c.translate(inch, inch)
    c.setFont("Times-BoldItalic", 30)
    c.setFillColorRGB(155/255, 122/255, 1/255)
    c.drawCentredString(350,230,participant.name)

    c.setFont("Times-Bold", 14)
    c.setFillColorRGB(0/255, 0/255, 0/255)
    c.drawCentredString(350,150,participant.course)

    sign1='C:/Django_project/cert/static/image/sign1.png'
    sign2='C:/Django_project/cert/static/image/sign2.png'

    sign1_path, sign1_width, sign1_height = get_image(sign1, width=4*cm)
    sign2_path, sign2_width, sign2_height = get_image(sign2, width=4*cm)

    c.drawImage(sign1_path, 140, 90, width=sign1_width, height=sign1_height)
    c.drawImage(sign2_path, 450, 90, width=sign2_width, height=sign2_height)

    c.showPage()
    c.save()
    buf.seek(0)

    return buf

@login_required(login_url='login')
def form_download(request,pk):
    buf = generate_certificate(request,pk)
    return FileResponse(buf, as_attachment=True, filename='certificate.pdf')

@login_required(login_url='login')
def form_view(request,pk):
    buf = generate_certificate(request,pk)
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    return response
