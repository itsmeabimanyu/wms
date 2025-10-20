from django.shortcuts import redirect
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('dashboard')),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('warehouse/', views.Warehouse.as_view(), name='warehouse'),
]