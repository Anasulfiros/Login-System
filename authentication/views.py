from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Login_System import settings
from django.core.mail import send_mail

# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request,"Username is already exist ! . Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered !")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 character")

        if password1 != password2:
            messages.error(request, "Password doesn't match")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('home')


        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, Please confirm your email in order to activate your account.")

        #Welcome email

        subject = "Welcome to Login system"
        message = "Hello " + myuser.first_name +"!! \n" + "Welcome to Login system by Anasul Firos \n Thank you for visiting our Website \n We have also sent you a confirmation email, Please confirm email in order to activate your account. \n\n Thanking you\n Anasul Firos"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'authentication/index.html', {'firstname' : firstname})
        
        else:
            messages.error(request, 'Bad credential')
            return redirect('home')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')