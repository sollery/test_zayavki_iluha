from django.urls import path
from . import views


urlpatterns = [
 path('create/<int:pk>/<int:pk_sub>/<int:count>/', views.subdivision_objects, name="create"),
 path('shablon/<int:id_ap>/<int:id_sub>/', views.shablon_zayavki, name="shablon_zayavki"),
 path('update/<int:id_ap>/<int:id_sub>/', views.update_zayavki, name="update_zayavki"),

 path('count_service/',views.count_service,name='count_service'),

 # path('object/<int:pk>/', views.object_application,name="objects_application"),
]
