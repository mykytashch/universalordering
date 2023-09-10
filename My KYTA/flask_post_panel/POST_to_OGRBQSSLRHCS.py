import requests
import random
import json

# Генерация случайного числа для заказов
def generate_order_id():
    return ''.join(random.choice('1234567890') for _ in range(6))

# Генерация случайной даты для заказов
def generate_order_date():
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

# Список данных для 5 не похожих заказов
orders = [
    {
        "order_id": generate_order_id(),
        "customer_name": "Ivan Ivanov",
        "order_date": generate_order_date(),
        "items": [
            {"product_name": "Chandelier", "quantity": 1, "price": 150},
            {"product_name": "Carpet", "quantity": 2, "price": 50},
        ],
        "shipping_address": {
            "street": "Pushkin St.",
            "house_number": "10",
            "city": "Moscow",
        },
        "payment_method": "Cash",
        "status": "Delivering",
    },
    {
        "order_id": generate_order_id(),
        "customer_name": "Anna Smirnova",
        "order_date": generate_order_date(),
        "products": [
            {"name": "Table", "quantity": 1, "cost": 200},
            {"name": "Chairs", "quantity": 4, "cost": 25},
        ],
        "delivery": {
            "address": "Lenin Ave., 5, St. Petersburg",
            "courier": True,
        },
        "paid": True,
    },
    {
        "order_id": generate_order_id(),
        "customer": {
            "first_name": "Maria",
            "last_name": "Kozlova",
            "email": "maria@example.com",
        },
        "order_date": generate_order_date(),
        "cart": [
            {"item_id": 1234, "quantity": 2},
            {"item_id": 5678, "quantity": 1},
        ],
        "shipping_address": "Gagarin St., 15, Yekaterinburg",
    },
    {
        "id": generate_order_id(),
        "created_at": generate_order_date(),
        "items": [
            {"product": "Coffee Machine", "quantity": 1, "price": 300},
            {"product": "Coffee Beans", "quantity": 2, "price": 10},
        ],
        "status": "Canceled",
    },
    {
        "reference_number": generate_order_id(),
        "customer": "Svetlana Petrova",
        "order_date": generate_order_date(),
        "items": [
            {"product_name": "Smartphone", "quantity": 1, "price": 400},
        ],
        "address": "Kirov Ave., 3, Kazan",
    },
]

# Отправка заказов
for order in orders:
    url = "http://127.0.0.1:5000/api/post/OGRBQSSLRHCS"
    response = requests.post(url, json=order, headers={"Content-Type": "application/json; charset=utf-8"})
    print(f"Response Code: {response.status_code}")
    print(response.text)
    print("\n")
