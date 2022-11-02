import json

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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

@login_required(login_url='/login/')
def home(request):
    customer = request.user
    print(customer)
    if request.user.is_authenticated:
        customer = CustomUser.objects.get(id=request.user.id)
    return render(request,'home.html',{'customer':customer})

@login_required(login_url='/login/')
def private_office(request,pk):
    if request.user.is_superuser:
        return render(request, 'private_office.html')
    subdivision_user = Subdivision.objects.get(user_subdivision=pk)
    print(subdivision_user.id)
    return render(request,'private_office.html',{'subdivision_user':subdivision_user})

@login_required(login_url='/login/')
def zayavki_list(request):
    if request.user.is_superuser:
        zayavki = ListApplication.objects.all().order_by('-created')
        paginator = Paginator(zayavki, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'zayavki_list.html', {'page_obj': page_obj,'zayavki':zayavki})
    zayavki = ListApplication.objects.filter(subdivision=request.user.subdivision).order_by('-created')
    print(request.user.subdivision)
    paginator = Paginator(zayavki, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = request.user
    id_sub = Subdivision.objects.get(pk=user.id).id
    print(id_sub)
    print(paginator)
    return render(request,'zayavki_list.html',{'page_obj': page_obj,'zayavki':zayavki,'id_sub':int(id_sub)})

@login_required(login_url='/login/')
def application_detail(request,pk):
    app = ListApplication.objects.get(id=pk)
    number = app.id
    status = app.status
    comment = app.comment
    zayavki = ApplicationTest.objects.filter(application_id_id=pk)
    rabotniki_sum = ApplicationTest.objects.filter(application_id_id=pk).aggregate(Sum('employee_count'))
    print(rabotniki_sum['employee_count__sum'])
    return render(request,'application_detail.html',{'zayavki':zayavki,'number':number,'status':status,'app':app,'comment': comment})


def status_data(request):
    if request.method == 'POST':
        text = ''
        temp = json.load(request)
        print(temp)
        status = temp.get('status')
        comment = temp.get('comment')
        id = temp.get('app_id')
        app = ListApplication.objects.get(pk=id)
        app.comment = 'Нет комментария'
        app.save()
        if status == 'approve':
            app.status = 'Согласованно'
            if len(comment):
                app.comment = comment
            app.save()
            text = f'Согласованно'
        if status == 'not_approve':
            app.status = 'Не согласованно'
            if len(comment):
                app.comment = comment
            app.save()
            text = f'Не согласованно'
        return HttpResponse(text)

# def customer_zayavki(request,pk):
#     zayavki = ApplicationTest.objects.filter(customer=request.user.pk)


