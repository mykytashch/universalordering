python3 manage.py migrate
python manage.py migrate

createdb mykyta
psql           

virtualenv venv
source venv/bin/activate


python manage.py runserver


Инструкция по отправке заказов на нашу панель:
Для отправки заказов на нашу панель, вам потребуется выполнить HTTP POST запрос на следующий URL:
http://127.0.0.1:8000/create_order/

Python:

import requests

url = "http://127.0.0.1:8000/create_order/"
data = {
    "id": None,
    "customer_name": "Имя Заказчика",
    "product": "Название Продукта",
    "created_at": "YYYY-MM-DDTHH:MM:SS.ZZZZZZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SS.ZZZZZZ"
}

response = requests.post(url, json=data)
print(response.status_code, response.text)


JavaScript (с использованием Fetch):

let url = "http://127.0.0.1:8000/create_order/";
let data = {
    id: null,
    customer_name: "Имя Заказчика",
    product: "Название Продукта",
    created_at: "YYYY-MM-DDTHH:MM:SS.ZZZZZZ",
    updated_at: "YYYY-MM-DDTHH:MM:SS.ZZZZZZ"
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));



cURL (php)

curl -X POST -H "Content-Type: application/json" -d '{
    "id": null,
    "customer_name": "Имя Заказчика",
    "product": "Название Продукта",
    "created_at": "YYYY-MM-DDTHH:MM:SS.ZZZZZZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SS.ZZZZZZ"
}' http://127.0.0.1:8000/create_order/
