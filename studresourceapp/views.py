from django.shortcuts import render
from .models import Resource
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

def home(request):
    resources = Resource.objects.all()
    return render(request, 'home.html', {'resources': resources})

def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists!'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid Username or Password'
        })

    return render(request, 'login.html')