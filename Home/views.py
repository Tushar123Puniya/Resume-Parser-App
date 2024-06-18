from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth.hashers import check_password
from .models import User
import csv
import os
from .forms import ResumeUploadForm
from django.http import HttpResponse,FileResponse
from django.conf import settings
from .Parsing_Model import main

# Create your views here.
def Home_page(request):
    reviews = [
        {
            'image_url': 'https://via.placeholder.com/100',
            'name': 'John Doe',
            'text': 'ParseMinds has revolutionized our hiring process. It quickly and accurately parses resumes, saving us countless hours of manual review.'
        },
        {
            'image_url': 'https://via.placeholder.com/100',
            'name': 'Jane Smith',
            'text': 'Using ParseMinds has streamlined our recruitment. The accuracy and speed of the parsing allow us to focus on interviewing the best candidates.'
        },
        {
            'image_url': 'https://via.placeholder.com/100',
            'name': 'Alice Johnson',
            'text': 'Our team has greatly benefited from the efficiency brought by ParseMinds. It integrates seamlessly with our existing systems and improves our candidate selection process.'
        }
    ]
    return render(request, 'Home/home_page.html',{'reviews' : reviews})

def Signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('Parsing_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'Home/signup_page.html', {'form':form})

def Login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    return redirect('Parsing_page')  # Redirect to a success page.
                else:
                    form.add_error(None, 'Invalid email or password')
            except User.DoesNotExist:
                    form.add_error(None, 'Invalid email or password')
        else:
            form.add_error(None, 'Invalid email or password format')
    else:
        form = LoginForm()
    return render(request, 'Home/login_page.html', {'form': form})

def AboutUs_page(request):
    return render(request, 'Home/aboutus_page.html', {})

def ContactUs_page(request):
    return render(request, 'Home/contactus_page.html', {})

def download_csv(request,filename):
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'), as_attachment=True)
        return response
    else:
        return HttpResponse(status=404)
    
def Parsing_page(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if(not request.FILES):
            csv_filename=""
            form.add_error(None,'Please select at least one resume')
        elif form.is_valid():
            resumes = request.FILES.getlist('resumes')
            main(resumes)
            csv_filename = "parsed_data.csv"
    else:
        form = ResumeUploadForm()
        csv_filename=""
    return render(request,'Home/parsing_page.html', {'form':form,'csv_filename':csv_filename})