from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import UserForm
from .models import *


class MainView(ListView):

    model = Good
    queryset = Good.objects.all()
    template_name = 'app_shop/main.html'


class CustomLoginView(LoginView):
    template_name = 'app_shop/login.html'
    next_page = 'main'

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        return response

class CustomLogoutView(LogoutView):
    template_name = 'app_shop/logout.html'
    next_page = 'main'

def register_view(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            Profile.objects.create(
                user=user
            )
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            auth_user = authenticate(username=username,
                                     password=password)
            login(request, auth_user)
            return redirect('main')
        return render(request,'app_shop/register.html', context={'user_form': user_form, 'errors': user_form.error_messages})
    else:
        return render(request, 'app_shop/register.html', context={'user_form': user_form})
