from django.shortcuts import render
from .models import Resource,DownloadHistory,ContactMessage
from django.contrib.auth.models import User
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.db.models import Q
def home(request):

    search_query = request.GET.get('search')

    if search_query:

        resources = Resource.objects.filter(
            Q(title__icontains=search_query) |
            Q(subject__icontains=search_query)
        )

    else:

        resources = Resource.objects.all()

    return render(request, 'home.html', {
        'resources': resources
    })

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
def logout_view(request):
    logout(request)
    return redirect('login')

def about(request):

    return render(request,'aboutus.html')


def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(

            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']

        )

        return render(request,
                      'contact.html',
                      {'success': 'Message sent successfully!'})

    return render(request, 'contact.html')


@login_required

def profile(request):

    downloads = DownloadHistory.objects.filter(
        user=request.user
    ).order_by('-downloaded_at')

    return render(request,
                  'profile.html',
                  {
                      'downloads': downloads
                  })

def download_resource(request, id):

    resource = get_object_or_404(Resource, id=id)

    if request.user.is_authenticated:

        DownloadHistory.objects.create(
            user=request.user,
            resource=resource
        )

    return FileResponse(
        resource.file.open('rb'),
        as_attachment=True
    )