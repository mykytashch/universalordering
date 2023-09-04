from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Comment, CustomUser, InvitationCode, UserProfile
from .serializers import OrderSerializer
from django.http import JsonResponse
from django.contrib.sessions.models import Session

from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)






@csrf_exempt
@login_required
def update_theme_preference(request):
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        new_theme_preference = request.POST.get("theme_preference")
        print("Received theme preference:", new_theme_preference)  # Добавьте эту строку для логирования
        if new_theme_preference in ['light', 'dark']:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.theme_preference = new_theme_preference
            user_profile.save()

            print("Theme preference updated:", new_theme_preference)
            return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error"})





# APIViews

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

# Themes

@login_required
def switch_theme(request):
    if request.method == 'POST':
        new_theme = request.POST.get('theme')  # Предположим, что у вас есть поле 'theme' в форме переключения темы
        if new_theme in ['light', 'dark']:
            request.session['theme_preference'] = new_theme
            request.session.modified = True  # Указываем, что сессия была изменена
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def some_view_name(request):
    theme_preference = request.session.get('theme_preference', 'light')
    # Остальной код для рендеринга страницы



@login_required
def create_order(request):
    if request.method == 'POST':
        raw_text = request.POST.get('order_text')
        try:
            order_data = json.loads(raw_text)

            if isinstance(order_data, dict) and 'customer_name' in order_data and 'product' in order_data:
                Order.objects.create(
                    customer_name=order_data['customer_name'],
                    product=order_data['product'],
                    status=Order.RECOGNIZED
                )
                messages.success(request, "Order created successfully!")
            else:
                Order.objects.create(
                    unrecognized_data=raw_text,
                    status=Order.UNRECOGNIZED
                )
                messages.warning(request, "Order was not recognized and saved for review.")
        except json.JSONDecodeError:
            Order.objects.create(
                unrecognized_data=raw_text,
                status=Order.UNRECOGNIZED
            )
            messages.warning(request, "Order was not recognized and saved for review.")

    return render(request, 'order_form.html')

@login_required
def order_list(request):
    query = request.GET.get('q')
    if query:
        orders = Order.objects.filter(
            Q(customer_name__icontains=query) | 
            Q(product__icontains=query)
        )
    else:
        orders = Order.objects.all()

    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'orders': page_obj}
    return render(request, 'order_panel.html', context)


def order_panel(request):
    query = request.GET.get('q')

    if query:
        orders = Order.objects.filter(Q(customer_name__icontains=query))
    else:
        orders = Order.objects.all().order_by('-created_at')[:5]

    context = {'recent_orders': orders}
    return render(request, 'order_panel.html', context)


@login_required
def home(request):
    logger.info("Function 'home' was called.")
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]  # Получение или создание профиля пользователя
    return render(request, 'home.html', {'recent_orders': recent_orders, 'user_profile': user_profile})





@login_required
def order_comments(request, order_id):
    order_instance = Order.objects.get(id=order_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(order=order_instance, text=comment_text, user=request.user)
            return redirect('comments', order_id=order_id)

    comments = Comment.objects.filter(order=order_instance)
    context = {
        'order': order_instance,
        'comments': comments,
    }
    return render(request, 'order_comments.html', context)


def unrecognized_order_detail(request, order_id):
    try:
        order = UnrecognizedOrder.objects.get(id=order_id)
    except UnrecognizedOrder.DoesNotExist:
        return render(request, 'error.html', {"message": "Unrecognized Order not found!"})

    context = {
        'order': order,
    }

    return render(request, 'unrecognized_order_detail.html', context)



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


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'order_detail.html', context)

@login_required
def unrecognized_orders(request):
    unrecognized_orders_list = Order.objects.filter(status=Order.UNRECOGNIZED)
    paginator = Paginator(unrecognized_orders_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'unrecognized_orders': page,
    }

    return render(request, 'unrecognized_orders.html', context)







def generate_invitation_code(request):
    if request.method == 'POST':
        master_code_input = request.POST.get('master_code')
        if master_code_input == "656546546":
            code = InvitationCode.generate_unique_code()
            invitation = InvitationCode(code=code)
            invitation.set_expiration()
            invitation.save()
            messages.success(request, f"Invitation code {code} was successfully generated!")
        else:
            messages.error(request, "Invalid master code.")

    return render(request, 'invitation_generation.html')

@login_required
def list_invitations(request):
    invitations = InvitationCode.objects.all().order_by('-expiration_date')
    return render(request, 'invitation_list.html', {'invitations': invitations})

def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)

def register_with_invitation_code(request):
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

        if not invitation:
            messages.error(request, "Invalid or used invitation code!")
            return render(request, 'registration_page.html', {'form_data': form_data})

        if invitation.expiration_date <= timezone.now():
            messages.error(request, "Invitation code expired!")
            return render(request, 'registration_page.html', {'form_data': form_data})

        # Создаем нового пользователя:
        user = CustomUser.objects.create_user(
            email=form_data['email'],  # здесь используется 'email', а не 'login'
            password=form_data['password'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name']
        )
        user.save()

        # Помечаем код как использованный
        invitation.is_used = True
        invitation.save()

        messages.success(request, "Registration successful!")
        return redirect('login')
    else:
        return render(request, 'registration_page.html')
