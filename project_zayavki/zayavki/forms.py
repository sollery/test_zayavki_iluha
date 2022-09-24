

from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, ModelForm, TextInput, NumberInput, Select, BaseFormSet
from django.http import request

from .models import ApplicationTest, Facility, EmployeeInSubdivision, Employee


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        """ Customises the labels for checkboxes"""
        return "%s" % member.title


class ApplicationTestForm(forms.ModelForm):
    class Meta:
        model = ApplicationTest
        fields = ['facility','employee','count_employee','comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 10,'placeholder': 'Введите комментарий'}),

        }
        labels = {'facility': 'Объект', 'employee': 'Специальность', 'count_employee': 'Кол-во',
                  'comment' :'Коммент'}
        help_text = {'text': 'Любую абракадабру', 'group': 'Из уже существующих'}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ApplicationTestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['facility'].queryset = Facility.objects.filter(subdivision_id=user.subdivision.id)
            self.fields['employee'].queryset = Employee.objects.filter(subdivision_id=user.subdivision.id)
            self.fields['facility'].empty_label = 'Выберите объект'
            self.fields['employee'].empty_label = 'Выберите услугу'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




    def clean(self):
        super(ApplicationTestForm, self).clean()
        facility = self.cleaned_data.get('facility')
        employee = self.cleaned_data.get('employee')
        if employee is None and facility is not None:
            raise ValidationError(f"Для объекта {facility.title} не была указанна специальность.")
        if facility is None and employee is not None:
            raise ValidationError(f"Для специальности {employee.title} не был указан объект.")
        if facility is None and employee is None:
            raise ValidationError(f"У вас есть пустые поля")


    # def clean_facility(self):
    #     facility = self.cleaned_data.get("facility")
    #     employee = self.cleaned_data.get("employee")
    #     if facility is None:
    #         raise ValidationError(
    #             f"Для специальности {employee.title} не был указан объект.")
    #
    #
    #
    # def clean_emploee(self):
    #     facility = self.cleaned_data.get("facility")
    #     employee = self.cleaned_data.get("employee")
    #

    #
    #     # return any errors if found
    #     return self.cleaned_data

    obj = [(i,i) for i in range(0,51)]
    count_employee = forms.CharField(widget=forms.Select(choices=obj),label='Кол-во')


class BaseApplicationTestFormset(BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            return
        facility_emps = []
        count = 0
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                count += 1
                continue
            employee = form.cleaned_data.get('employee')
            facility = form.cleaned_data.get('facility')
            count_employee = form.cleaned_data.get('count_employee')
            if [employee.title,facility.title] in facility_emps:
                raise ValidationError(f"Для объекта {facility.title} была продублирована специальность {employee.title}.")
            facility_emps.append([employee.title, facility.title])
            if int(count_employee) == 0:
                raise ValidationError(
                    f"Для объекта {facility.title} не было указано кол-во {employee.title}.")








class CountServiceForm(forms.Form):
    count_s = [(i, i) for i in range(1, 51)]
    count_service = forms.CharField(widget=forms.Select(choices=count_s),label='Выберите кол-во строк')

# ApplicationTestFormset = formset_factory(ApplicationTestForm, extra=6)
# class ApplicationTestForm(class ApplicationTestForm(forms.Form,):,):
#
#     def __init_(self, id_sub):
#         super(ApplicationTestForm, self).__init__(self, id_sub)
#         obj = Facility.objects.filter(subdivision_id=id_sub)
#         rabotniki = EmployeeInSubdivision.filter(subdivision_id=id_sub)
#
#     name = forms.CharField(widget=forms.Select(choices=rabotniki))
#     isbn_number = forms.CharField(widget=forms.Select(choices=rabotniki_count))
#     obj = forms.CharField(widget=forms.Select(choices=obj))

# BookFormset = formset_factory(BookForm, extra=6)