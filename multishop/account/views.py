from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import LoginForm, RegisterForm, CheckOtp, AddressCreationFrom
from account.models import Otp, User
from random import randint
from uuid import uuid4
import ghasedakpack

SMS = ghasedakpack.Ghasedak("cb86dc0320455f7e092ee1ac0d34894f8137071eced5a8bc1755e7983dcb96a7")

# for login with email and phone number
class LoginView(View):  # phone + Email
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("home:home")
            else:
                form.add_error("username", "incorrect data")
        else:
            form.add_error("username", "invalid data")
        return render(request, 'account/login.html', {'form': form})

# you can register by phone and code we send to you
class RegisterView(View):  # phone
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randomcode = randint(1000, 9999)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randomcode})
            print(randomcode)
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], code=randomcode, token=token)
            return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error('phone', 'invalid phone number')
        return render(request, 'account/register.html', {'form': form})

# code for check that is you
class Check_otpView(View):
    def get(self, request):
        form = CheckOtp()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtp(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home:home')
        return render(request, 'account/check_otp.html', {'form': form})

# for address in cart
class AddAddressView(View):
    def get(self, request):
        form = AddressCreationFrom()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressCreationFrom(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'account/add_address.html', {'form': form})


def logoutview(request):
    logout(request)
    return redirect('home:home')


