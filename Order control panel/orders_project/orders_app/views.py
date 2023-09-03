from django.shortcuts import render, redirect
from django.db.models import Q
from .models import InvitationCode, Order  # У вас была дублирующаяся строка, которая импортировала Order из 'your_app.models'
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

def home(request):
    recent_orders = Order.objects.all().order_by('-created_at')[:5]  # Предполагая, что у вас есть поле 'created_at' для отслеживания времени создания заказа.
    return render(request, 'home.html', {'recent_orders': recent_orders})

def success_page(request):
    return render(request, 'success.html')  

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

        return redirect('success_page')  
    else:
        return render(request, 'registration_page.html')

