from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/orders/', views.OrderCreate.as_view(), name='order_create'),
    path('orders/', views.order_list, name='order_list'),
    path('success/', views.success_page, name='success_page'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/orders/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('generate-invite/', views.generate_invitation_code, name='generate_invitation_code'),
    path('register/', views.register_with_invitation_code, name='register_with_invitation_code'),
]
