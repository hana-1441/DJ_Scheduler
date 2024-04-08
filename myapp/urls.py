from django.urls import path,include
from myapp import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('user_ip/', views.user_ip, name='user_ip'),
]
