import json

from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from zayavki.models import ApplicationTest,ListApplication
from .models import CustomUser, Subdivision
from .forms import LoginForm, RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator

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
        zayavki = ListApplication.objects.all().order_by('-created')
        paginator = Paginator(zayavki, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'zayavki_list.html', {'page_obj': page_obj,'zayavki':zayavki})
    zayavki = ListApplication.objects.filter(customer=request.user.pk).order_by('-created')
    paginator = Paginator(zayavki, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(paginator)
    return render(request,'zayavki_list.html',{'page_obj': page_obj,'zayavki':zayavki})


def application_detail(request,pk):
    app = ListApplication.objects.get(id=pk)
    number = app.id
    status = app.status
    zayavki = ApplicationTest.objects.filter(application_id_id=pk)
    print(zayavki)
    return render(request,'application_detail.html',{'zayavki':zayavki,'number':number,'status':status,'app':app})


def status_data(request):
    if request.method == 'POST':
        text = ''
        temp = json.load(request)
        status = temp.get('status')
        id = temp.get('app_id')
        if status == 'approve':
            app = ListApplication.objects.get(pk=id)
            app.status = 'Согласованно'
            app.save()
            text = 'Согласованно'
        if status == 'not_approve':
            app = ListApplication.objects.get(pk=id)
            app.status = 'Не согласованно'
            app.save()
            text = 'Не согласованно'
        return HttpResponse(text)

# def customer_zayavki(request,pk):
#     zayavki = ApplicationTest.objects.filter(customer=request.user.pk)


