from orders_app import views as orders_app_views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Основные пути
    path('', orders_app_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/orders/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', orders_app_views.register, name='register'),
    path('generate-invite/', orders_app_views.generate_invitation_code, name='generate_invitation_code'),
    path('update_theme_preference/', orders_app_views.update_theme_preference, name='update_theme_preference'),
    path('create_order/', orders_app_views.create_order, name='create_order'),

    # Пути для заказов
    path('orders/', orders_app_views.order_panel, name='order_panel'),
    path('order_list/', orders_app_views.order_list, name='order_list'),
    path('order/<int:order_id>/', orders_app_views.order_detail, name='order_detail'),
    path('order-comments/<int:order_id>/', orders_app_views.order_comments, name='order-comments'),

    # Пути для нераспознанных заказов
    path('unrecognized_orders/', orders_app_views.unrecognized_orders, name='unrecognized_orders'),
    path('unrecognized_order/<int:unrecognized_order_id>/', orders_app_views.unrecognized_order_detail, name='unrecognized_order_detail'),
    path('unrecognized-order-comments/<int:unrecognized_order_id>/', orders_app_views.unrecognized_order_comments, name='unrecognized-order-comments'),

    # Пути для комментариев к заказам
    path('comments/<int:order_id>/', orders_app_views.order_comments, name='comments'),

    path('comments/<int:order_id>/', lambda request, order_id: 
         orders_app_views.generic_comments_view(request, order_id, RecognizedOrder, 'order_detail.html'),
         name='comments_for_recognized'),
    path('all-order-comments/', orders_app_views.all_order_comments, name='all_order_comments'),

    # API пути
    path('api/orders/', orders_app_views.OrderListCreateAPI.as_view(), name='api_order_create'),
]
