from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from django import forms



class SignUpForm(UserCreationForm):
    group = forms.ChoiceField(choices=[('Professor', 'Professor'), ('Student', 'Student')], required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'group']

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get selected group and assign it to the user
            group_name = form.cleaned_data.get('group')
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            # Automatically log in the user after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on group
                if group_name == 'Professor':
                    return redirect('faculty:index')
                else:
                    return redirect('students:index')

            return redirect('exam:index')  # Redirect to some page after sign-up
    else:
        form = SignUpForm()

    return render(request, 'exam/signup.html', {'form': form})



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