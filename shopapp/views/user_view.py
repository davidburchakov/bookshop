from django.contrib.auth.models import User

from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models.models import UserProfile
from django.contrib.auth.decorators import login_required


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("A user with that phone number already exists.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user


class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data['email']
        user_id = self.instance.id
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile = user.userprofile
            user_profile.phone = self.cleaned_data['phone']
            user_profile.save()
        return user


def register_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "User created successfully")
            return redirect('index')  # Redirect to a home page
    else:
        form = MyUserCreationForm()
    return render(request, 'shopapp/register.html', context={"form": form})


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


@login_required
def profile_view(request):
    if request.user.is_authenticated:
        try:
            user_profile = get_object_or_404(UserProfile, user=request.user)
            context = {
                'user': request.user,
                'profile': user_profile,
                'phone': user_profile.phone if user_profile.phone else "No phone number provided",
            }
        except:
            context = {
                'user': request.user,
                'profile': None,
                'phone': None
            }
    else:
        context = {
            'error': "permissions denied"
        }

    return render(request, 'user/profile.html', context=context)


def profile_update_view_page(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)

        context = {
            'user': request.user,
            'profile': user_profile,
            'phone': user_profile.phone if user_profile.phone else "No phone number provided"
        }
    else:
        context = {
            'error': "permissions denied"
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


def profile_delete(request):
    if request.method == 'POST':
        print("POST")
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Your account has been successfully deleted!")
            return redirect('index')
        else:
            messages.error(request, "Permissions denied.")
            return redirect('index')
    else:
        messages.error(request, "Invalid Request Method.")
        return render(request, 'user/profile.html')
