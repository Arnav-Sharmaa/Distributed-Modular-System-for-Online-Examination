from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            if user.is_superuser or user.is_staff:
                return redirect('/admin')
            
            if user.groups.filter(name='Professor').exists():
                return redirect('faculty:index')
            
            return redirect('students:index')
            

        return render(request, 'exam/login.html', { 'wrong_cred_message': 'Error' })

    return render(request, 'exam/login.html')


def logoutUser(request):
    logout(request)
    return render(request, 'exam/logout.html',{ 'logout_message': 'Logged out Successfully' })