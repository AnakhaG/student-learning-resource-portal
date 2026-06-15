from django.shortcuts import render, redirect, get_object_or_404
from studresourceapp.models import Resource
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def admin_dashboard(request):
    resources = Resource.objects.all()
    return render(request, 'admin/dashboard.html', {
        'resources': resources
    })


def add_resource(request):

    if request.method == 'POST':

        Resource.objects.create(
            title=request.POST['title'],
            subject=request.POST['subject'],
            description=request.POST['description'],
            url=request.POST.get('url'),
            file=request.FILES.get('file')
        )

        return redirect('dashboard')

    return render(request, 'admin/add_resource.html')


def edit_resource(request, id):

    resource = get_object_or_404(Resource, id=id)

    if request.method == "POST":

        resource.title = request.POST.get("title")
        resource.subject = request.POST.get("subject")
        resource.description = request.POST.get("description")
        resource.url = request.POST.get("url")

        if request.FILES.get("file"):
            resource.file = request.FILES["file"]

        resource.save()

        return redirect("dashboard")

    return render(request,
                  "admin/edit_resource.html",
                  {"resource": resource})


def delete_resource(request, id):

    resource = get_object_or_404(Resource, id=id)

    if request.method == "POST":

        resource.delete()

        return redirect('dashboard')

    return render(request, 'admin/delete_resource.html', {'resource': resource})
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def admin_register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():

            return render(request, 'admin/register.html',
                          {'error': 'Username already exists'})

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('admin_login')

    return render(request, 'admin/register.html')


def admin_login(request):

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

            return redirect('dashboard')

        return render(request,
                      'admin/login.html',
                      {'error': 'Invalid Username or Password'})

    return render(request, 'admin/login.html')


def admin_logout(request):

    logout(request)

    return redirect('admin_login')


def dashboard(request):

    resources = Resource.objects.all()

    students = User.objects.all()

    context = {
        'resources': resources,
        'students': students,
        'resource_count': resources.count(),
        'student_count': students.count(),
    }

    return render(request, 'admin/dashboard.html', context)
def delete_student(request, id):

    student = get_object_or_404(User, id=id)

    # Prevent deleting the currently logged-in admin
    if request.user.id != student.id:
        student.delete()

    return redirect('dashboard')