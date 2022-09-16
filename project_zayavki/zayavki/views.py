from django.shortcuts import render, redirect
from accounts.models import CustomUser
from datetime import datetime


from .models import *
from .send_email_for_customer import send_email_customer


def subdivision_objects(request,pk):
    objects_sub = Facility.objects.filter(subdivision__id=pk)
    m = [i.title for i in objects_sub]
    print(m)
    return render(request,'subdivision_detail.html',{'objects_sub':objects_sub})


# Create your views here.

def object_application(request,pk):
    application_obj = EmployeeInFacility.objects.filter(facility_id=pk)
    date_now = datetime.today().strftime('%Y-%m-%d')
    print(application_obj)
    emp = [i.employee.title for i in application_obj]
    print(emp)
    if request.method == "POST":
        customer = CustomUser.objects.get(pk=request.user.id)
        customer_name = customer.fio
        customer_position = customer.position.title
        customer_podrazdel = customer.subdivision.id
        customer_email = customer.email
        
        print(customer_name,customer_podrazdel,customer_email,customer_position)
        fac = Facility.objects.get(id=pk)
        data = dict(request.POST.copy())
        print(data)
        data_date = request.POST.get('date', None)
        print(data_date)
        del data['csrfmiddlewaretoken']
        del data['date']
        # print(data)
        # print(type(data))
        # print(data['3'])
        for emp in dict(data):
        #     print(type(data[emp]))
            ApplicationTest.objects.create(customer=customer, data_application=data_date, facility=fac,
                                           employee=Employee.objects.get(pk=int(emp)), employee_count=int(data[emp][0]),
                                           subdivision=customer.subdivision,
                                           comment=data[emp][1])
        print('заявка создана')
        data_m = ApplicationTest.objects.filter(customer=customer,data_application=data_date,employee_count__gt=0)

        send_email_customer(data_m, customer_email, date_now, fac.title, customer_name,customer_position)
        return redirect('home')
    return render(request,'application_object.html',{'application_obj':application_obj,'date_now': date_now})