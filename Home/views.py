from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm_email,LoginForm,ResumeUploadForm,ScoreForm,UserRegistrationForm
from django.contrib.auth.hashers import check_password
from .models import User
from django.conf import settings
from .Parsing_Model import parsing_only,similarity_scoring,dynamic_scoring
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password


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


def send_otp(email):
    otp = ''.join(random.choices('0123456789', k=6))  # Generate 6-digit OTP
    message = f'Your OTP is: {otp}'
    send_mail('OTP Verification', message, settings.DEFAULT_FROM_EMAIL, [email])
    return otp

def verify_otp(request):
    message={
        "error":""
    }
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        otp_sent = request.session.get('otp_sent')
        if otp_entered==otp_sent:
            print("hello")
            messages.success(request, 'OTP verified. You have signed up successfully.')
            return redirect('user_detail')  # Redirect to login page
        else:
            message['error']= 'Invalid OTP / Email Not Found'
    return render(request, 'Home/verify_otp.html',message)

def user_detail(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match.')
            else:
                # Assuming User model has 'name' and 'password' fields
                user = User(
                    name=name,  # Assuming you are using the 'username' field for the name
                    email = request.session['email'],
                    password=make_password(password)  # Hashing the password
                )
                user.save()
                messages.success(request, 'User registered successfully.')
                return redirect('Option_page')  

    else:
        form = UserRegistrationForm()

    return render(request, 'Home/user_details.html', {'form': form})
    
def Signup_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm_email(request.POST)
        if form.is_valid():
            person_mail = form.cleaned_data['email']
            request.session['email'] = person_mail
            request.session['otp_sent'] = send_otp(person_mail)
            return redirect('verify_otp')
    else:
        form = UserRegistrationForm_email()
    return render(request, 'Home/signup_page_email.html', {'form':form})

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

def Passwordreset_page(request):
    
    return render(request, 'Home/passwordreset_page.html', {})
    
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
        
        scoring_option = request.POST.get('scoring_option')
        
        if scoring_option=='simple':
            print(scoring_option)
            if not resumes:
                form.add_error('Please upload at least one resume')
            
            if not job_description:
                form.add_error('Please add job description')
                
            else:
                csv_filename=similarity_scoring(resumes,job_description)
                return csv_filename
        else :
            criteria_options = request.POST.getlist('criteria_options[]')
            csv_filename=dynamic_scoring(resumes,job_description,criteria_options)
            return csv_filename
    else:
        form = ScoreForm()
        
    return render(request, 'Home/scoring_page.html',{'form':form})
