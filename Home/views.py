from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm,LoginForm,ResumeUploadForm,ScoreForm
from django.contrib.auth.hashers import check_password
from .models import User
import csv
import os
from django.http import HttpResponse,FileResponse
from django.conf import settings
from .Parsing_Model import parsing_only,similarity_scoring

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
            return redirect('Option_page')
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
                    return redirect('Option_page')  # Redirect to a success page.
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
    
def Option_page(request):
    return render(request, 'Home/option_page.html')
    
def Parsing_page(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if(not request.FILES):
            csv_filename=""
            form.add_error(None,'Please select at least one resume')
        elif form.is_valid():
            resumes = request.FILES.getlist('resumes')
            csv_filename = parsing_only(resumes)
            return csv_filename
    else:
        form = ResumeUploadForm()
    return render(request,'Home/parsing_page.html', {'form':form})

def Scoring_page(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST,request.FILES)
        resumes = request.FILES.getlist('resumes[]')
        job_description = request.FILES.get('job_description')
        
        # Handle scoring options
        scoring_option = request.POST.get('scoring_option')
        
        print(resumes,' ',job_description)
        
        if not resumes:
            form.add_error('Please upload at least one resume')
        
        if not job_description:
            form.add_error('Please add job description')
            
        if scoring_option == 'dynamic':
            criteria_order = request.POST.get('criteria_order', '').split(',')
        
        else:
            print('Hello')
            csv_filename=similarity_scoring(resumes,job_description)
            return csv_filename
    else:
        form = ScoreForm()
        
    return render(request, 'Home/scoring_page.html',{'form':form})