from django.urls import path
from . import views


urlpatterns = [
 path('subdivision/<int:pk>/<int:count>/', views.subdivision_objects, name="subdivision_objects"),
 path('count_service/',views.count_service,name='count_service')

 # path('object/<int:pk>/', views.object_application,name="objects_application"),
]