from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm_email,LoginForm,ResumeUploadForm,ScoreForm,UserRegistrationForm,passwordreset
from django.contrib.auth.hashers import check_password
from .models import User
from django.conf import settings
from .Parsing_Model import parsing_only,similarity_scoring,dynamic_scoring
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
from django.urls import reverse

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
            messages.success(request, 'OTP verified. You have signed up successfully.')
            return redirect('user_detail')  # Redirect to login page
        else:
            message['error']= 'Invalid OTP / Email Not Found'
    return render(request, 'Home/verify_otp.html',message)

def verify_otp1(request):
    message={
        "error":""
    }
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        otp_sent = request.session.get('otp_sent')
        if otp_entered==otp_sent:
            messages.success(request, 'OTP verified. You can change password now.')
            return redirect('change_password')  # Redirect to login page
        else:
            message['error']= 'Invalid OTP / Email Not Found'
    return render(request, 'Home/verify_otp1.html',message)

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
                    password=make_password(password),  # Hashing the password
                    ip_address = request.META['REMOTE_ADDR']
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
        curr_ip = request.META['REMOTE_ADDR']
        stat = User.objects.filter(ip_address=curr_ip).exists()
        if stat:
            form.add_error(None,'This IP address already has one account.')
        else:
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
                    request.session['email']=email
                    return redirect('Option_page')  
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
    message={
        'error':'',
        'success':''
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email']=email
        stat = User.objects.filter(email=email).exists()
        if not stat:
            message['error']='User does not exists.'
        else:
            request.session['otp_sent']=send_otp(email)
            return redirect('verify_otp1')
    return render(request, 'Home/passwordreset_page.html', message)
    
def change_password(request):
    if request.method == 'POST':
        form = passwordreset(request.POST)
        if form.is_valid():
            email = request.session['email']
            user = get_object_or_404(User, email=email)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('Login_page')
    else:
        form = passwordreset()
    return render(request,'Home/change_password.html',{'form':form})
    
def Option_page(request):
    email = request.session['email']
    user = get_object_or_404(User, email=email)
    message= {
        'name': user.name
    }
    return render(request, 'Home/option_page.html',message)

def Account_page(request):
    email = request.session['email']
    user = get_object_or_404(User, email=email)
    message={
      'name':user.name,
      'email':user.email,
      'trials_left': user.trials,
      'max_cv': user.cv_limit
    }
    return render(request,'Home/account_page.html',message)
 
def Parsing_page(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        email = request.session['email']
        user = get_object_or_404(User, email=email)
        if(not request.FILES):
            csv_filename=""
            form.add_error(None,'Please select at least one resume')
        elif form.is_valid():
            resumes = request.FILES.getlist('resumes')
            if len(resumes) > user.cv_limit:
                form.add_error(None,f'You can input upto {user.cv_limit} resumes at maximum')
            else:
                email = request.session['email']
                user = get_object_or_404(User, email=email)
                if user.trials>0:
                    csv_filename = parsing_only(resumes)
                    user.trials = user.trials-1
                    user.save()
                    if user.trials==0:
                        text = '''
                        Hello User,
                        Your plan is expired, please contact us for continuing the service.
                        Thank You
                        '''
                        send_mail('Plan expired', text, settings.DEFAULT_FROM_EMAIL, [email])
                    return csv_filename
                else:
                    form.add_error(None,'Your Plan is expired, please contact us to continue.')
    else:
        form = ResumeUploadForm()
    return render(request,'Home/parsing_page.html', {'form':form})


def Scoring_page(request):
    if request.method == 'POST':
        form = ScoreForm(request.POST,request.FILES)
        resumes = request.FILES.getlist('resumes[]')
        job_description = request.FILES.get('job_description')
        
        scoring_option = request.POST.get('scoring_option')
        
        email = request.session['email']
        user = get_object_or_404(User, email=email)
        
        if len(resumes)>user.cv_limit:
            form.add_error(None,f'You can upload a maximum of {user.cv_limit} resumes')
        else:
            if scoring_option=='simple':
                print(scoring_option)
                if not resumes:
                    form.add_error('Please upload at least one resume')
                
                if not job_description:
                    form.add_error('Please add job description')
                    
                else:
                    if user.trials>0:
                        user.trials = user.trials-1
                        user.save()
                        if user.trials==0:
                            text = '''
                            Hello User,
                            Your plan is expired, please contact us for continuing the service.
                            Thank You
                            '''
                            send_mail('Plan expired', text, settings.DEFAULT_FROM_EMAIL, [email])
                        csv_filename=similarity_scoring(resumes,job_description)
                        return csv_filename
                    else:
                        form.add_error(None,'Your plan is expired please contact us to continue')
            else :
                if user.trials>0:
                    user.trials = user.trials - 1
                    user.save()
                    if user.trials==0:
                        text = '''
                        Hello User,
                        Your plan is expired, please contact us for continuing the service.
                        Thank You
                        '''
                        send_mail('Plan expired', text, settings.DEFAULT_FROM_EMAIL, [email])
                    criteria_options = request.POST.getlist('criteria_options[]')
                    csv_filename=dynamic_scoring(resumes,job_description,criteria_options)
                    return csv_filename
                else:
                    form.add_error(None,'Your plan is expired please contact us to continue')
    else:
        form = ScoreForm()
        
    return render(request, 'Home/scoring_page.html',{'form':form})
