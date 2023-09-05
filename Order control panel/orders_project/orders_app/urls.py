from orders_app import views as orders_app_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', orders_app_views.home, name='home'),
    path('all-order-comments/', orders_app_views.all_order_comments, name='all_order_comments'),
    path('orders/', orders_app_views.order_panel, name='order_panel'),
    path('unrecognized_orders/', orders_app_views.unrecognized_orders, name='unrecognized_orders'),
    path('unrecognized_order/<int:unrecognized_order_id>/comments/', orders_app_views.unrecognized_order_comments, name='unrecognized_order_comments'),
    path('unrecognized_order/<int:unrecognized_order_id>/', orders_app_views.unrecognized_order_detail, name='unrecognized_order_detail'),
    path('order/<int:order_id>/', orders_app_views.order_detail, name='order_detail'),
    path('order_list/', orders_app_views.order_list, name='order_list'),
    
    path('create_order/', orders_app_views.create_order, name='create_order'),  # Updated this line
    
    path('update_theme_preference/', orders_app_views.update_theme_preference, name='update_theme_preference'),
    path('generate-invite/', orders_app_views.generate_invitation_code, name='generate_invitation_code'),
    path('register/', orders_app_views.register, name='register'),  # Updated this line
    
    path('api/orders/', orders_app_views.OrderListCreateAPI.as_view(), name='api_order_create'),  # Updated this line
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/orders/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
