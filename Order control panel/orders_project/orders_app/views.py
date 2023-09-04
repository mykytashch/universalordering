from django.shortcuts import render, redirect
from django.db.models import Q
import logging

from .models import InvitationCode, Order, UnrecognizedOrder, Comment
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer
from .forms import MasterCodeForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.core.paginator import Paginator, Page

logger = logging.getLogger(__name__)

class OrderCreate(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
def create_order(request):
    if request.method == 'POST':
        raw_text = request.POST.get('order_text')  # Получите текстовую строку из формы

        try:
            order_data = json.loads(raw_text)  # Попробуйте разобрать текст как JSON

            # Проверьте, является ли order_data словарем и соответствует ли JSON вашим критериям
            if isinstance(order_data, dict) and 'customer_name' in order_data and 'product' in order_data:
                # Создайте новый заказ
                Order.objects.create(
                    customer_name=order_data['customer_name'],
                    product=order_data['product']
                )
                messages.success(request, "Order created successfully!")
            else:
                # Сохраните JSON как нераспознанный заказ
                UnrecognizedOrder.objects.create(data=raw_text)
                messages.warning(request, "Order was not recognized and saved for review.")
        except (json.JSONDecodeError, TypeError):
            # Если текст не может быть разобран как JSON, сохраните его как нераспознанный заказ
            UnrecognizedOrder.objects.create(data=raw_text)
            messages.warning(request, "Order was not recognized and saved for review.")

    return render(request, 'order_form.html')

def order_list(request):
    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
            # Если есть другие поля для поиска, добавьте их здесь следуя паттерну выше.
        )
    else:
        orders = Order.objects.all()

    context = {'orders': orders}
    return render(request, 'order_list.html', context)

 

def order_panel(request):
    query = request.GET.get('q')

    if query:
        # Фильтрация заказов по имени заказчика
        orders = Order.objects.filter(Q(customer_name__icontains=query))
    else:
        # Если нет поискового запроса, показываем последние 5 заказов
        orders = Order.objects.all().order_by('-created_at')[:5]

    context = {'recent_orders': orders}
    return render(request, 'order_panel.html', context)


def order_comments(request, order_id):
    regular_order = None
    unrecognized_order = None
    
    try:
        regular_order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        try:
            unrecognized_order = UnrecognizedOrder.objects.get(id=order_id)
        except UnrecognizedOrder.DoesNotExist:
            return render(request, 'error.html', {"message": "Order not found!"})

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            if regular_order:
                Comment.objects.create(order=regular_order, text=comment_text, user=request.user)
            else:
                Comment.objects.create(unrecognized_order=unrecognized_order, text=comment_text, user=request.user)
            return redirect('comments', order_id=order_id)

    if regular_order:
        comments = Comment.objects.filter(order=regular_order)
    else:
        comments = Comment.objects.filter(unrecognized_order=unrecognized_order)

    context = {
        'order': regular_order or unrecognized_order,
        'comments': comments,
    }

    return render(request, 'order_comments.html', context)




def unrecognized_order_comments(request, unrecognized_order_id):
    try:
        unrecognized_order_instance = UnrecognizedOrder.objects.get(id=unrecognized_order_id)
    except UnrecognizedOrder.DoesNotExist:
        return render(request, 'error.html', {"message": "Order not found!"})

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(unrecognized_order=unrecognized_order_instance, text=comment_text, user=request.user)
            return redirect('unrecognized_order_comments', unrecognized_order_id=unrecognized_order_id)


    comments = Comment.objects.filter(unrecognized_order=unrecognized_order_instance)

    context = {
        'order': unrecognized_order_instance,
        'comments': comments,
    }

    return render(request, 'order_comments.html', context)



def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        try:
            order = UnrecognizedOrder.objects.get(id=order_id)
        except UnrecognizedOrder.DoesNotExist:
            return render(request, 'error.html', {"message": "Order not found!"})

    context = {
        'order': order,
    }

    return render(request, 'order_detail.html', context)



def unrecognized_order_detail(request, order_id):
    try:
        order = UnrecognizedOrder.objects.get(id=order_id)
    except UnrecognizedOrder.DoesNotExist:
        return render(request, 'error.html', {"message": "Unrecognized Order not found!"})

    context = {
        'order': order,
    }

    return render(request, 'unrecognized_order_detail.html', context)



@login_required
def unrecognized_orders(request):
    # Получите все заказы или используйте ваши собственные фильтры
    all_orders = UnrecognizedOrder.objects.all()

    # Создайте объект Paginator с количеством заказов на странице
    paginator = Paginator(all_orders, 10)  # 10 заказов на странице

    # Получите номер запрошенной страницы из параметра запроса
    page_number = request.GET.get('page')

    # Получите объект Page для текущей страницы
    page: Page = paginator.get_page(page_number)

    context = {
        'unrecognized_orders': page,
    }

    return render(request, 'unrecognized_orders.html', context)


@login_required
def update_theme_preference(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        theme_preference = request.POST.get("theme_preference")
        if theme_preference in ["light", "dark"]:
            # Update the user's theme preference in the database
            request.user.theme_preference = theme_preference
            request.user.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)    
        

MASTER_CODE = "656546546"

@login_required
def home(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    return render(request, 'home.html', {'recent_orders': recent_orders})

def success_page(request):
    return render(request, 'success.html')  


def generate_invitation_code(request):
    if request.method == 'POST':
        master_code_input = request.POST.get('master_code')
        if master_code_input == MASTER_CODE:
            code = InvitationCode.generate_unique_code()
            invitation = InvitationCode(code=code)
            invitation.set_expiration(24)  # Сначала устанавливаем срок действия
            invitation.save()  # Затем сохраняем объект
            return render(request, 'generated_code.html', {'code': code})  # Возвращаем страницу с кодом
    return render(request, 'generate_code.html')



def register_with_invitation_code(request):
    if request.method == 'POST':
        provided_code = request.POST.get('invitation_code')
        login = request.POST.get('login')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', "")  # Если поля нет, используем пустую строку
        last_name = request.POST.get('last_name', "")

        try:
            invitation = InvitationCode.objects.get(code=provided_code, is_used=False)
        except InvitationCode.DoesNotExist:
            return render(request, 'error.html', {"message": "Invalid code!"})

        if invitation.expiration_date <= timezone.now():
            return render(request, 'error.html', {"message": "Code expired!"})

        # Создаем нового пользователя:
        user = User.objects.create_user(
            username=login,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Помечаем код как использованный
        invitation.is_used = True
        invitation.save()

        return redirect('login') 
    else:
        return render(request, 'registration_page.html')


