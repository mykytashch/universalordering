# импорты стандартных библиотек
import json
import logging

# импорты сторонних библиотек
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

# внутренние импорты
from .models import (Order, Comment, CustomUser, InvitationCode, UserProfile, 
                     UnrecognizedOrder, RecognizedOrder, TextEntry)
from orders_project.secrets import MASTER_CODE

from .serializers import OrderSerializer

logger = logging.getLogger(__name__)



def generate_invitation_code(request):
    if request.method == 'POST':
        master_code_input = request.POST.get('master_code')
        if master_code_input == MASTER_CODE:
            code = InvitationCode.generate_unique_code()
            invitation = InvitationCode(code=code)
            invitation.set_expiration()
            invitation.save()
            messages.success(request, f"Invitation code {code} was successfully generated!")
        else:
            messages.error(request, "Invalid master code.")
    return render(request, 'invitation_generation.html')


@login_required
def all_order_comments(request):
    orders_for_page = Order.objects.all()  # Извлечение всех заказов. Если база данных будет большой, этот запрос может быть неэффективным.
    paginator = Paginator(orders_for_page, 15)  # Показывать 15 заказов на странице
    page = request.GET.get('page')
    orders_for_page = paginator.get_page(page)
    
    return render(request, 'all_order_comments.html', {'orders_for_page': orders_for_page})


def create_order(request):
    if request.method == 'POST':
        order_text = request.POST.get('order_text')
        if order_text:
            # Здесь вы можете добавить логику обработки данных из формы.
            # Например, сохранение данных в модели Order.
            Order.objects.create(unrecognized_data=order_text)
            messages.success(request, "Заказ успешно создан!")
            return redirect('home')
        else:
            messages.error(request, "Пожалуйста, введите данные заказа.")
    return render(request, 'create_order.html')

class PasswordManager:
    ALLOWED_PASSWORDS = ["password1", "password2", "password3"]

    @staticmethod
    def is_valid(password: str) -> bool:
        return password in PasswordManager.ALLOWED_PASSWORDS

class DataHandlers:
    @staticmethod
    def handle_json(data: dict) -> None:
        Order.objects.create(data=data)

    @staticmethod
    def handle_text(text: str) -> None:
        TextEntry.objects.create(text=text)

@csrf_exempt
def receive_order(request):
    if request.method == 'POST':
        lines = request.body.decode('utf-8').strip().split('\n')
        if not PasswordManager.is_valid(lines[0]):
            return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=401)
        
        content = '\n'.join(lines[1:])
        try:
            data = json.loads(content)
            RecognizedOrder.objects.create(**data)  # Создаем RecognizedOrder
            return JsonResponse({'status': 'success', 'message': 'Data received'})
        except json.JSONDecodeError:
            UnrecognizedOrder.objects.create(unrecognized_data=content)  # Создаем UnrecognizedOrder
            return JsonResponse({'status': 'success', 'message': 'Text received'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@login_required
def dashboard(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'recent_orders': recent_orders, 'user_profile': user_profile})



def order_panel(request):
    query = request.GET.get('q')
    orders = Order.objects.filter(Q(customer_name__icontains=query)) if query else Order.objects.all().order_by('-created_at')[:5]
    context = {'recent_orders': orders}
    return render(request, 'order_panel.html', context)

@login_required
def home(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'recent_orders': recent_orders, 'user_profile': user_profile})

@login_required
def update_theme_preference(request):
    if request.method == 'POST':
        new_theme = request.POST.get('theme')
        if new_theme in ['light', 'dark']:
            request.session['theme_preference'] = new_theme
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)




def register(request):
    if request.method == 'POST':
        form_data = {
            'invitation_code': request.POST.get('invitation_code'),
            'login': request.POST.get('login'),
            'password': request.POST.get('password'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name', ""),
            'last_name': request.POST.get('last_name', "")
        }
        invitation = InvitationCode.objects.filter(code=form_data['invitation_code'], is_used=False).first()
        if not invitation or invitation.expiration_date <= timezone.now():
            messages.error(request, "Invalid or expired invitation code!")
            return render(request, 'registration_page.html', {'form_data': form_data})

        user = CustomUser.objects.create_user(
            email=form_data['email'],
            password=form_data['password'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name']
        )
        user.save()
        invitation.is_used = True
        invitation.save()
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'registration_page.html')

class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@login_required
def switch_theme(request):
    if request.method == 'POST' and request.POST.get('theme') in ['light', 'dark']:
        request.session['theme_preference'] = request.POST.get('theme')
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def unrecognized_order_detail(request, order_id):
    order = get_object_or_404(UnrecognizedOrder, id=order_id)
    return render(request, 'unrecognized_order_detail.html', {'order': order})

@login_required
def generic_comments_view(request, order_id, order_model, template_name):
    order_instance = get_object_or_404(order_model, id=order_id)

    if order_model == RecognizedOrder:
        related_field_name = "recognized_order"
    elif order_model == UnrecognizedOrder:
        related_field_name = "unrecognized_order"
    elif order_model == Order:  # обработка модели Order
        related_field_name = "order"
    else:
        raise ValueError("Unsupported order model.")

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(**{
                related_field_name: order_instance, 
                'text': comment_text, 
                'user': request.user
            })
            return redirect('comments', order_id=order_id)

    comments = Comment.objects.filter(**{related_field_name: order_instance})
    return render(request, template_name, {'order': order_instance, 'comments': comments})


@login_required
def order_comments(request, order_id):
    # Проверяем, к какой модели относится данный заказ
    if RecognizedOrder.objects.filter(id=order_id).exists():
        order_model = RecognizedOrder
    elif UnrecognizedOrder.objects.filter(id=order_id).exists():
        order_model = UnrecognizedOrder
    elif Order.objects.filter(id=order_id).exists():  # Добавим эту проверку
        order_model = Order
    else:
        # Вместо поднятия исключения, вы можете рендерить страницу с сообщением об ошибке
        return render(request, 'error_page.html', {'message': 'Order not found.'})
    
    # Здесь мы просто вызываем generic_comments_view с правильными параметрами
    return generic_comments_view(request, order_id, order_model, 'order_comments.html')


@login_required
def unrecognized_order_comments(request, unrecognized_order_id):
    return generic_comments_view(request, unrecognized_order_id, UnrecognizedOrder, 'unrecognized_order', 'order_comments.html')

@login_required
def generic_order_list(request, template_name, queryset):
    query = request.GET.get('q')
    orders = queryset.filter(Q(customer_name__icontains=query) | Q(product__icontains=query)) if query else queryset
    page_obj = Paginator(orders, 15).get_page(request.GET.get('page'))
    return render(request, template_name, {'orders': page_obj})

@login_required
def order_list(request):
    return generic_order_list(request, 'order_panel.html', Order.objects.all())

@login_required
def unrecognized_orders(request):
    return generic_order_list(request, 'unrecognized_orders.html', Order.objects.filter(status=Order.UNRECOGNIZED))