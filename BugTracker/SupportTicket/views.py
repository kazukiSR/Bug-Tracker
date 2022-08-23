from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.clean_email()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('index')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.clean_email()
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'registration/login.html', context)


def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    return redirect('dashboard')


def detail(request, ticket_id):
    return HttpResponse("You're looking at ticket %s." % ticket_id)


@login_required
def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    return render(request, 'SupportTicket/dashboard.html')