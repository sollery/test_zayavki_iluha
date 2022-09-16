from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse_lazy

from zayavki.models import ApplicationTest
from .models import CustomUser, Subdivision
from .forms import LoginForm, RegisterForm
from django.shortcuts import render
from django.contrib.auth import logout


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")


def home(request):
    customer = request.user
    print(customer)
    if request.user.is_authenticated:
        customer = CustomUser.objects.get(id=request.user.id)
    return render(request,'home.html',{'customer':customer})


def private_office(request,pk):
    if request.user.is_superuser:
        return render(request, 'private_office.html')
    subdivision_user = Subdivision.objects.get(user_subdivision=pk)
    print(subdivision_user.id)
    return render(request,'private_office.html',{'subdivision_user':subdivision_user})



def zayavki_list(request):
    if request.user.is_superuser:
        zayavki = ApplicationTest.objects.filter(employee_count__gt=0)
        return render(request, 'zayavki_list.html', {'zayavki': zayavki})
    zayavki = ApplicationTest.objects.filter(customer=request.user.pk,employee_count__gt=0)
    return render(request,'zayavki_list.html',{'zayavki':zayavki})


# def customer_zayavki(request,pk):
#     zayavki = ApplicationTest.objects.filter(customer=request.user.pk)