from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name="home"),
  path('private_office/<int:pk>/', views.private_office, name='private_office'),
  path('zayavki_list/',views.zayavki_list, name='zayavki_list'),
  path('application_detail/<int:pk>/',views.application_detail,name='application_detail'),
  path('status_data/', views.status_data, name='status_data')

]