from django.contrib import admin
from django.urls import path
from check_phone import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.ApiView.as_view(), name='api'),
    path('', views.WebView.as_view()),
]
