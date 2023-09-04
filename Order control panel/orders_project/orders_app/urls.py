from orders_app import views as orders_app_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', orders_app_views.home, name='home'),
    path('orders/', orders_app_views.order_panel, name='order_panel'),
    path('order/<int:order_id>/comments/', orders_app_views.order_comments, name='comments'),
    path('unrecognized_orders/', orders_app_views.unrecognized_orders, name='unrecognized_orders'),
    path('unrecognized_order/<int:unrecognized_order_id>/comments/', orders_app_views.unrecognized_order_comments, name='unrecognized_order_comments'),
    path('unrecognized_order/<int:unrecognized_order_id>/', orders_app_views.unrecognized_order_detail, name='unrecognized_order_detail'),
    path('order/<int:order_id>/', orders_app_views.order_detail, name='order_detail'),
    path('order_list/', orders_app_views.order_list, name='order_list'),
    path('order_create/', orders_app_views.OrderCreate.as_view(), name='order_create'),
    path('create_order/', orders_app_views.create_order, name='create_order'),
    path('update_theme_preference/', orders_app_views.update_theme_preference, name='update_theme_preference'),
    path('api/orders/', orders_app_views.OrderCreate.as_view(), name='api_order_create'),  # Я изменил имя этого URL, чтобы избежать конфликта с другим 'order_create'.
    path('success/', orders_app_views.success_page, name='success_page'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/orders/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('generate-invite/', orders_app_views.generate_invitation_code, name='generate_invitation_code'),
    path('register/', orders_app_views.register_with_invitation_code, name='register_with_invitation_code'),
]
