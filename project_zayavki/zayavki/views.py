from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import formset_factory, forms, BaseFormSet
from django.shortcuts import render, redirect
from accounts.models import CustomUser,Subdivision
from datetime import datetime

from django.utils.datastructures import MultiValueDictKeyError

from .forms import ApplicationTestForm, CountServiceForm, BaseApplicationTestFormset
from django.forms import formset_factory
from .models import *
from .send_email_for_customer import send_email_customer


# class MyApplicationTestForm(ApplicationTestForm):
#     def __init__(self, *args, user, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)


# ArticleFormSet = formset_factory(ArticleForm, formset=BaseArticleFormSet)
#
def update_zayavki(request,id_ap,id_sub):
    apps = ApplicationTest.objects.filter(application_id=id_ap).values('facility','employee','employee_count')
    count = ApplicationTest.objects.filter(application_id=id_ap).count()
    print(apps)
    title = 'Редактирование заявки'
    ApplicationTestFormset = formset_factory(ApplicationTestForm, can_delete=True, extra=0,
                                             formset=BaseApplicationTestFormset, validate_min=True)
    date_now = datetime.today().strftime('%Y-%m-%d')
    user = request.user.id
    formset = ApplicationTestFormset(
        form_kwargs={
            'user': request.user,
            'id_pk': id_sub,

    }, initial=[i for i in apps])

    # print(formset)
    subdivision = Subdivision.objects.get(pk=id_sub)
    viza = CustomUser.objects.all()
    if request.method == 'POST':
        ApplicationTestFormset = formset_factory(ApplicationTestForm,
                                                 can_delete=True,formset=BaseApplicationTestFormset,min_num = 1, validate_min = True)
        formset = ApplicationTestFormset(request.POST,form_kwargs={'user': request.user,'id_pk': id_sub,})
        data_date = request.POST['date']

        error = 'Проверьте свои поля'
        date_now = datetime.today().strftime('%Y-%m-%d')
        my_check = [form.prefix for form in formset if formset.data.get(f"{form.prefix}-DELETE", False)]
        if request.POST['viza_k'] != 'Выберите визу':
            viza_k = CustomUser.objects.get(fio=request.POST['viza_k'])
        else:
            viza_k = None
        if formset.is_valid():
            app = ListApplication.objects.get(pk=id_ap)
            app.status = 'на рассмотрении'
            app.save()
            customer = app.customer
            apl = ApplicationTest.objects.filter(application_id = app)
            apl.delete()
            for form in formset:
                facility = form.cleaned_data.get('facility')
                emp = form.cleaned_data.get('employee')
                emp_count = form.cleaned_data.get('employee_count')
                comment = form.cleaned_data.get('comment')
                if form.prefix in my_check:
                    continue
                ApplicationTest.objects.update_or_create(customer=customer, date_application=data_date, facility=facility,
                                                           employee=emp, employee_count=emp_count,
                                                           subdivision=subdivision,
                                                           comment=comment,application_id=app)
                # apps.append(m)
                # print(apps)


        else:
            try:
                error = formset.errors[0]['__all__']
            except:
                pass
            return render(request, "subdivision_detail.html", {'formset': formset,'date_now':date_now,'error':error,'viza':viza,'title':title,'my_check':my_check})
        data_m = ApplicationTest.objects.filter(subdivision=subdivision, date_application=data_date, employee_count__gt=0,application_id=app).order_by('facility')
        rabotniki_sum = ApplicationTest.objects.filter(application_id_id=id_ap).aggregate(Sum('employee_count'))
        count_rabotniki = rabotniki_sum['employee_count__sum']
        send_email_customer(data_m, customer.email, date_now, customer.fio,customer.position,subdivision,count_rabotniki,viza_k)
        return redirect('zayavki_list')
    return render(request,'subdivision_detail.html',{'formset':formset,'date_now': date_now,'viza':viza,'title':title})



def shablon_zayavki(request,id_ap,id_sub):
    apps = ApplicationTest.objects.filter(application_id=id_ap).values('facility','employee','employee_count')
    count = ApplicationTest.objects.filter(application_id=id_ap).count()
    print(apps)
    title = 'Создание по шаблону'
    # apps_for_shablon = ApplicationTest.objects.filter(id_ap)
    ApplicationTestFormset = formset_factory(ApplicationTestForm, can_delete=True, extra=0,
                                             formset=BaseApplicationTestFormset, validate_min=True)
    date_now = datetime.today().strftime('%Y-%m-%d')
    # default_facility = Facility.objects.get(title='тест1')
    # default_employee = Employee.objects.get(title='ПОВАР')
    # default_facility_1 = Facility.objects.get(title='тест2')
    # default_employee_1 = Employee.objects.get(title='АЙТИШНИК')
    # print(Subdivision.objects.all())
    user = request.user.id
    formset = ApplicationTestFormset(
        form_kwargs={
            'user': request.user,
            'id_pk': id_sub,

    }, initial=[i for i in apps])

    # print(formset)
    subdivision = Subdivision.objects.get(pk=id_sub)
    viza = CustomUser.objects.all()
    if request.method == 'POST':
        ApplicationTestFormset = formset_factory(ApplicationTestForm,
                                                 can_delete=True,formset=BaseApplicationTestFormset,min_num = 1, validate_min = True)
        formset = ApplicationTestFormset(request.POST,form_kwargs={'user': request.user,'id_pk': id_sub,})
        data_date = request.POST['date']
        customer = CustomUser.objects.get(pk=user)
        error = 'Проверьте свои поля'
        date_now = datetime.today().strftime('%Y-%m-%d')
        my_check = [form.prefix for form in formset if formset.data.get(f"{form.prefix}-DELETE", False)]
        apps = []
        if request.POST['viza_k'] != 'Выберите визу':
            viza_k = CustomUser.objects.get(fio=request.POST['viza_k'])
        else:
            viza_k = None
        if formset.is_valid():
            app_id = ListApplication.objects.create(customer=customer, date_applications=data_date,
                                                    subdivision=subdivision,viza=viza_k)
            for form in formset:

                # print(form)
                facility = form.cleaned_data.get('facility')
                emp = form.cleaned_data.get('employee')
                emp_count = form.cleaned_data.get('employee_count')
                comment = form.cleaned_data.get('comment')
                if form.prefix in my_check:
                    continue
                m = ApplicationTest.objects.create(customer=customer, date_application=data_date, facility=facility,
                                                           employee=emp, employee_count=emp_count,
                                                           subdivision=subdivision,
                                                           comment=comment,application_id=app_id)
                # apps.append(m)
                # print(apps)


        else:
            try:
                error = formset.errors[0]['__all__']
            except:
                pass
            return render(request, "subdivision_detail.html", {'formset': formset,'date_now':date_now,'error':error,'viza':viza,'title':title,'my_check':my_check})
        data_m = ApplicationTest.objects.filter(subdivision=subdivision, date_application=data_date, employee_count__gt=0,application_id= app_id).order_by('facility')
        rabotniki_sum = ApplicationTest.objects.filter(application_id_id=app_id).aggregate(Sum('employee_count'))
        count_rabotniki = rabotniki_sum['employee_count__sum']
        send_email_customer(data_m, customer.email, date_now, customer.fio,customer.position,subdivision,count_rabotniki,viza_k)

        return redirect('zayavki_list')
    return render(request,'subdivision_detail.html',{'formset':formset,'date_now': date_now,'viza':viza,'title':title})


@login_required(login_url='/login/')
def subdivision_objects(request,pk,pk_sub,count):
    ApplicationTestFormset = formset_factory(ApplicationTestForm,can_delete = True, extra=count,
                                             formset = BaseApplicationTestFormset,min_num = 1, validate_min = True)
    date_now = datetime.today().strftime('%Y-%m-%d')

    # default_facility = Facility.objects.get(title='тест1')
    # default_employee = Employee.objects.get(title='ПОВАР')
    # default_facility_1 = Facility.objects.get(title='тест2')
    # default_employee_1 = Employee.objects.get(title='АЙТИШНИК')
    # print(Subdivision.objects.all())
    title = 'Создание заявки'
    formset = ApplicationTestFormset(
        form_kwargs={
            'user': request.user,
            'id_pk': pk_sub,
        })
        # }, initial=[{'facility': default_facility, 'employee':default_employee, "count_employee": 12,
        #              },{'facility': default_facility_1, 'employee':default_employee_1, "count_employee": 13},])

    # print(formset)
    viza = CustomUser.objects.all()
    # print(viza.count())
    if request.method == 'POST':
        my_formset = request.POST.copy()
        ApplicationTestFormset = formset_factory(ApplicationTestForm,
                                                 can_delete=True,formset=BaseApplicationTestFormset,min_num = 1, validate_min = True)
        formset = ApplicationTestFormset(my_formset,form_kwargs={'user': request.user,'id_pk': pk_sub,})
        data_date = request.POST['date']
        customer = CustomUser.objects.get(pk=pk)
        error = 'Проверьте свои поля'
        date_now = datetime.today().strftime('%Y-%m-%d')
        apps = []
        if request.POST['viza_k'] != 'Выберите визу':
            viza_k = CustomUser.objects.get(fio=request.POST['viza_k'])
        else:
            viza_k = None
        subdivision = Subdivision.objects.get(pk=pk_sub)
        total = int(formset.data['form-TOTAL_FORMS'])
        my_check = [form.prefix for form in formset if formset.data.get(f"{form.prefix}-DELETE", False)]
        print(my_check)
        if formset.is_valid():

            app_id = ListApplication.objects.create(customer=customer, date_applications=data_date,
                                                    subdivision=subdivision,viza=viza_k)

            for form in formset:

                # if formset.data[f"{form.prefix}-DELETE"]:
                #     if formset.data[f"{form.prefix}-DELETE"] == 'on':
                #         print(formset.data[f"{form.prefix}-DELETE"])
                        # formset.data['form-TOTAL_FORMS'] -= 1
                        # formset.forms.remove(form)
                        # print(form)
                facility = form.cleaned_data.get('facility')
                emp = form.cleaned_data.get('employee')
                emp_count = form.cleaned_data.get('employee_count')
                comment = form.cleaned_data.get('comment')
                if form.prefix in my_check:
                    continue
                m = ApplicationTest.objects.create(customer=customer, date_application=data_date, facility=facility,
                                                           employee=emp, employee_count=emp_count,
                                                           subdivision=subdivision,
                                                           comment=comment,application_id=app_id)
                # apps.append(m)
                # print(apps)


        else:
            # for form in formset:
            #     try:
            #         if formset.data[f"{form.prefix}-DELETE"] == 'on' and total > 1:
            #             # print(formset.data[f"{form.prefix}-DELETE"])
            #             # print(formset.data['form-TOTAL_FORMS'])
            #             total -= 1
            #             formset.data['form-TOTAL_FORMS'] = str(total)
            #             formset.forms.remove(form)
            #             # print(formset.data[f"{form.prefix}-DELETE"])
            #             # print(formset.forms)
            #     except MultiValueDictKeyError:
            #         print('net')
            #     print(total)
            try:
                error = formset.errors[0]['__all__']
            except:
                pass
            return render(request, "subdivision_detail.html", {'formset': formset,'date_now':date_now,'error':error,'viza':viza,'title':title,'my_check':my_check})

        data_m = ApplicationTest.objects.filter(subdivision=subdivision, date_application=data_date, employee_count__gt=0,application_id= app_id).order_by('facility')
        rabotniki_sum = ApplicationTest.objects.filter(application_id_id=app_id).aggregate(Sum('employee_count'))
        count_rabotniki = rabotniki_sum['employee_count__sum']
        send_email_customer(data_m, customer.email, date_now, customer.fio,customer.position,subdivision,count_rabotniki,viza_k)
        return redirect('zayavki_list')
    return render(request,'subdivision_detail.html',{'formset':formset,'date_now': date_now,'viza':viza,'title':title})

@login_required(login_url='/login/')
def count_service(request):
    form = CountServiceForm()
    subdivisions = Subdivision.objects.all()
    if request.method == 'POST':
        user_id = request.user.id
        form = CountServiceForm(request.POST)
        pk_sub = request.user.subdivision_id
        # check whether it's valid:
        if form.is_valid():
            if request.user.is_staff:
                print(request.POST['sub'])
                pk_sub = Subdivision.objects.get(title=request.POST['sub']).id
            count = int(form.cleaned_data.get('count_service'))-1
            return redirect(f'/zayavki/create/{user_id}/{pk_sub}/{count}/')
    return render (request,'count_service.html', {'form':form,'subdivisions':subdivisions})
# Create your views here.

# def object_application(request,pk):
#     application_obj = EmployeeInFacility.objects.filter(facility_id=pk)
#     date_now = datetime.today().strftime('%Y-%m-%d')
#     print(application_obj)
#     emp = [i.employee.title for i in application_obj]
#     print(emp)
#     if request.method == "POST":
#         customer = CustomUser.objects.get(pk=request.user.id)
#         customer_name = customer.fio
#         customer_position = customer.position.title
#         customer_podrazdel = customer.subdivision.id
#         customer_email = customer.email
#
#         print(customer_name,customer_podrazdel,customer_email,customer_position)
#         fac = Facility.objects.get(id=pk)
#         data = dict(request.POST.copy())
#         print(data)
#         data_date = request.POST.get('date', None)
#         print(data_date)
#         del data['csrfmiddlewaretoken']
#         del data['date']
#         # print(data)
#         # print(type(data))
#         # print(data['3'])
#         for emp in dict(data):
#         #     print(type(data[emp]))
#             ApplicationTest.objects.create(customer=customer, data_application=data_date, facility=fac,
#                                            employee=Employee.objects.get(pk=int(emp)), employee_count=int(data[emp][0]),
#                                            subdivision=customer.subdivision,
#                                            comment=data[emp][1])
#         print('заявка создана')
#         data_m = ApplicationTest.objects.filter(customer=customer,data_application=data_date,employee_count__gt=0)
#
#         send_email_customer(data_m, customer_email, date_now, fac.title, customer_name,customer_position)
#         return redirect('home')
#     return render(request,'application_object.html',{'application_obj':application_obj,'date_now': date_now})

