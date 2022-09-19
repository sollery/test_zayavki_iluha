

from django import forms
from django.forms import formset_factory, ModelForm, TextInput, NumberInput, Select
from django.http import request

from .models import ApplicationTest, Facility, EmployeeInSubdivision, Employee


# class ApplicationTestForm(ModelForm):
#     class Meta:
#         model = ApplicationTest
#         fields = ('facility', 'employee', 'employee_count')

    # def __init_(self, id_sub):
    #     super(ApplicationTestForm, self).__init__(self, id_sub)
    #     self.fields['facility'] = Facility.objects.filter(subdivision__id=id_sub)
    #     self.fields['employee'] = EmployeeInSubdivision.objects.filter(subdivision_id=id_sub)
    #     self.fields['employee_count'] = [(i,i) for i in range(0,51)]
    #




    # rabotniki = [(r.id, r.title) for r in Employee.objects.filter(subdivision__id=id_)]
    # rabotniki_count = [(i,i) for i in range(0,50)]
    # obj = [(r.id, r.title) for r in Facility.objects.filter(user_subdivision__id=id_)]
    #
    #
    # name = forms.CharField(widget=forms.Select(choices=rabotniki))
    # count = forms.IntegerField(widget=forms.Select(choices=rabotniki_count))
    # obj_ = forms.CharField(widget=forms.Select(choices=obj))
# class ApplicationTestForm(forms.Form):
#     class Meta:
#         model = ApplicationTest
#         fields = ('facility', 'employee', 'employee_count')
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user:
#             self.fields['facility'].queryset = Facility.objects.filter(subdivision__user=user)
#             self.fields['employee'].queryset = Employee.objects.filter(subdivision__user=user)
#             self.employee_count = [(i,i) for i in range(0,50)]
#
#     widgets = {
#         "facility": Select(attrs={
#             'placeholder': 'Рабочии',
#         }),
#         "employee": Select(attrs={
#             'class': 'myfield',
#             'placeholder': 'Ваша фамилия'
#         }),
#         "employee_count": Select(attrs={
#             'class': 'myfield',
#             'placeholder': 'Ваша почта'
#         }),
#
#     }
#
# ApplicationTestFormset = formset_factory(ApplicationTestForm, extra=6)


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        """ Customises the labels for checkboxes"""
        return "%s" % member.title


class ApplicationTestForm(forms.ModelForm):
    class Meta:
        model = ApplicationTest
        fields = ['facility','employee','count_employee','comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1, 'cols': 60}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ApplicationTestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['facility'].queryset = Facility.objects.filter(subdivision_id=user.subdivision.id)
            self.fields['employee'].queryset = Employee.objects.filter(subdivision_id=user.subdivision.id)
            self.fields['facility'].empty_label = 'Выберите'
            self.fields['employee'].empty_label = 'Выберите'
            self.fields['comment'].initial = 'Введите текст'





    def clean(self):
        # data from the form is fetched using super function
        super(ApplicationTestForm, self).clean()

        # extract the username and text field from the data
        facility = self.cleaned_data.get('facility')
        employee = self.cleaned_data.get('employee')

        # conditions to be met for the username length
        if facility == 'Выберите':
            self._errors['facility'] = self.error_class([
                'Заполните поле'])
        if employee == 'Выберите':
            self._errors['employee'] = self.error_class([
                'Заполните поле'])

        # return any errors if found
        return self.cleaned_data
    # name = forms.CharField()
    # date = forms.DateInput()

    # facility = CustomModelMultipleChoiceField(
    #     queryset=None,
    #     widget=forms.CheckboxSelectMultiple
    # )

    # employee = CustomModelMultipleChoiceField(
    #     queryset=None,
    #     widget=forms.CheckboxSelectMultiple
    # )
    obj = [(i,i) for i in range(0,51)]
    count_employee = forms.CharField(widget=forms.Select(choices=obj))




# ApplicationTestFormset = formset_factory(ApplicationTestForm, extra=6)
# class ApplicationTestForm(forms.Form,):
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