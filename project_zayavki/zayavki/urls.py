from django.urls import path
from . import views


urlpatterns = [
 path('subdivision/<int:pk>/', views.subdivision_objects, name="subdivision_objects"),
 path('object/<int:pk>/', views.object_application,name="objects_application"),
]