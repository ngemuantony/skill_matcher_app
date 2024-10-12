from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from django.template.loader import get_template

############ Index page ##################################

def index(request):
    return render(request, 'accounts/index.html', {'title': 'Index Page'})

########### register here ##################################### 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            ######################### mail system #################################### 
            htmly = get_template('accounts/Email.html')
            d = {'username': username}
            subject, from_email, to = 'Welcome to Skill Matcher App', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 

            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Register here'})


################ login forms################################################### 
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('job_listings')  # Redirect to job listings page after login
        else:
            messages.info(request, f'Account does not exist. Please sign up.')
    
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': 'Log In'})
