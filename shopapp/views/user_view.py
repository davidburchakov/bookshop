from django.contrib.auth.models import User

from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django import forms
from django.core.exceptions import ValidationError
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit - False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


# def register_view(request):
#     if request.method == 'POST' and request.POST.get('form_type') == "register_form":
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')  # Redirect to a home page
#     else:
#         form = MyUserCreationForm()
#     return render(request, 'shopapp/register.html', context={"form": form})


def register_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']  # Make sure to hash this password

            # SQL to insert the new user
            sql = """
            INSERT INTO users (username, password, email) VALUES (%s, %s, %s);
            """
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql, [username, password, email])
                messages.success(request, "User created successfully")
                return redirect('index')  # Redirect to a home page
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = MyUserCreationForm()
    return render(request, 'shopapp/register.html', context={"form": form})


# Login View
def login_view(request: HttpRequest):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a home page
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'shopapp/login.html')


def profile_view(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, 'user/profile.html', context=context)


def profile_update_view_page(request: HttpRequest):
    context = {
        'user': request.user
    }
    return render(request, "user/profile-update.html", context=context)


def profile_update_view(request: HttpRequest):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user/profile-update.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirects to the home page after logout
