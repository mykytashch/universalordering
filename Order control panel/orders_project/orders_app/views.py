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
from rest_framework import generics, status
from rest_framework.response import Response

# внутренние импорты
from .models import Order, Comment, CustomUser, InvitationCode, UserProfile, UnrecognizedOrder
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)

# ----- Обработчики форм -----

@login_required
def dashboard(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'recent_orders': recent_orders, 'user_profile': user_profile})

# ...

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


def order_panel(request):
    query = request.GET.get('q')

    if query:
        orders = Order.objects.filter(Q(customer_name__icontains=query))
    else:
        orders = Order.objects.all().order_by('-created_at')[:5]

    context = {'recent_orders': orders}
    return render(request, 'order_panel.html', context)


def all_order_comments(request):
    orders = list(Order.objects.all()) + list(UnrecognizedOrder.objects.all())
    paginator = Paginator(orders, 10) # 10 заказов на страницу, можно изменить
    page = request.GET.get('page')
    orders_for_page = paginator.get_page(page)
    
    return render(request, 'all_order_comments.html', {'orders_for_page': orders_for_page})


@login_required
def home(request):
    logger.info("Function 'home' was called.")
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]  # Получение или создание профиля пользователя
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
        if not invitation:
            messages.error(request, "Invalid or used invitation code!")
            return render(request, 'registration_page.html', {'form_data': form_data})

        if invitation.expiration_date <= timezone.now():
            messages.error(request, "Invitation code expired!")
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
    else:
        return render(request, 'registration_page.html')

# ... [Rest of the views]

class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@login_required
def switch_theme(request):
    if request.method == 'POST':
        new_theme = request.POST.get('theme')
        if new_theme in ['light', 'dark']:
            request.session['theme_preference'] = new_theme
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def view_with_theme(request):
    theme_preference = request.session.get('theme_preference', 'light')
    # ... [Your render code]

# ... [Rest of the views]



class OrderListCreateAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def handle_order_creation(request, data, recognized=True):
    if recognized:
        Order.objects.create(
            customer_name=data['customer_name'],
            product=data['product'],
            status=Order.RECOGNIZED
        )
        messages.success(request, "Order created successfully!")
    else:
        Order.objects.create(
            unrecognized_data=data,
            status=Order.UNRECOGNIZED
        )
        messages.warning(request, "Order was not recognized and saved for review.")

def create_order(request):
    if request.method == 'POST':
        raw_text = request.POST.get('order_text')
        try:
            order_data = json.loads(raw_text)
            recognized = isinstance(order_data, dict) and 'customer_name' in order_data and 'product' in order_data
            handle_order_creation(request, order_data if recognized else raw_text, recognized)
        except json.JSONDecodeError:
            handle_order_creation(request, raw_text, False)

    return render(request, 'order_form.html')

@login_required
def generic_order_list(request, template_name, queryset):
    query = request.GET.get('q')
    orders = queryset.filter(Q(customer_name__icontains=query) | Q(product__icontains=query)) if query else queryset

    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template_name, {'orders': page_obj})

@login_required
def order_list(request):
    return generic_order_list(request, 'order_panel.html', Order.objects.all())

@login_required
def unrecognized_orders(request):
    return generic_order_list(request, 'unrecognized_orders.html', Order.objects.filter(status=Order.UNRECOGNIZED))

@login_required
def generic_comments_view(request, order_id, order_model, related_field_name, template_name):
    order_instance = get_object_or_404(order_model, id=order_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(**{
                related_field_name: order_instance, 
                'text': comment_text, 
                'user': request.user
            })
            return redirect('comments', order_id=order_id)

    # Здесь мы создаём словарь фильтрации на лету.
    comments_filter = {related_field_name: order_instance}
    comments = Comment.objects.filter(**comments_filter)
    
    context = {
        'order': order_instance,
        'comments': comments,
    }
    return render(request, template_name, context)

@login_required
def order_comments(request, order_id):
    return generic_comments_view(request, order_id, Order, 'related_order', 'order_comments.html')

@login_required
def unrecognized_order_comments(request, unrecognized_order_id):
    return generic_comments_view(request, unrecognized_order_id, UnrecognizedOrder, 'unrecognized_order', 'order_comments.html')



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def unrecognized_order_detail(request, order_id):
    order = get_object_or_404(UnrecognizedOrder, id=order_id)
    return render(request, 'unrecognized_order_detail.html', {'order': order})

# ... [Rest of the views]



