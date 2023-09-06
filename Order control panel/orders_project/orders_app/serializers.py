from rest_framework import serializers
from .models import Order, UnrecognizedOrder

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    customer_name = serializers.CharField(max_length=255)
    product = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    # Обязательные поля
    dmn = serializers.CharField(max_length=255)  # Домен сайта, откуда идет продажа.
    oid = serializers.IntegerField(required=False)  # ID заказа с сайта (если есть).

    # Дополнительные переменные
    uid = serializers.IntegerField(required=False)  # ID пользователя.
    dt = serializers.DateTimeField(required=False)  # Дата и время заказа.
    ip = serializers.IPAddressField(required=False)  # IP-адрес покупателя.
    itm = serializers.ListField(child=serializers.CharField(max_length=100), required=False)  # Список товаров в заказе.
    pmt = serializers.CharField(max_length=50, required=False)  # Используемый способ оплаты.
    amt = serializers.FloatField(required=False)  # Общая сумма заказа.
    shp = serializers.JSONField(required=False)  # Информация о доставке.
    disc = serializers.CharField(max_length=100, required=False)  # Используемые скидки или купоны.
    eml = serializers.EmailField(required=False)  # Электронная почта покупателя.
    tel = serializers.CharField(max_length=20, required=False)  # Телефон покупателя.
    addr = serializers.CharField(max_length=255, required=False)  # Адрес доставки.
    note = serializers.CharField(required=False)  # Примечания к заказу.
    cur = serializers.CharField(max_length=3, required=False)  # Валюта транзакции.
    sts = serializers.CharField(max_length=50, required=False)  # Статус заказа.
    rfid = serializers.IntegerField(required=False)  # ID реферера.
    tax = serializers.FloatField(required=False)  # Примененные налоги к заказу.
    geo = serializers.JSONField(required=False)  # Геолокация покупателя.
    brw = serializers.CharField(max_length=50, required=False)  # Используемый браузер.
    os = serializers.CharField(max_length=50, required=False)  # Операционная система покупателя.
    aff = serializers.IntegerField(required=False)  # Аффилированный ID.
    crt = serializers.JSONField(required=False)  # Содержимое корзины.
    src = serializers.CharField(max_length=100, required=False)  # Источник трафика.
    loy = serializers.JSONField(required=False)  # Данные о лояльности покупателя.
    rev = serializers.JSONField(required=False)  # Отзывы о товаре/сервисе.
    sub = serializers.JSONField(required=False)  # Подписки покупателя.
    gdr = serializers.CharField(max_length=10, required=False)  # Пол покупателя.
    age = serializers.IntegerField(required=False)  # Возраст покупателя.
    prfl = serializers.JSONField(required=False)  # Профиль покупателя на сайте.
    hist = serializers.JSONField(required=False)  # История покупок пользователя.
    fav = serializers.JSONField(required=False)  # Избранные товары.
    size = serializers.CharField(max_length=20, required=False)  # Размер товара (если применимо).
    col = serializers.CharField(max_length=50, required=False)  # Цвет товара.
    wgt = serializers.FloatField(required=False)  # Вес товара.
    brand = serializers.CharField(max_length=100, required=False)  # Бренд или производитель товара.
    cat = serializers.CharField(max_length=100, required=False)  # Категория товара.
    dur = serializers.IntegerField(required=False)  # Продолжительность услуги или гарантии.
    rat = serializers.FloatField(required=False)  # Рейтинг товара на сайте.
    view = serializers.IntegerField(required=False)  # Количество просмотров товара перед покупкой.
    lstv = serializers.DateTimeField(required=False)  # Дата последнего визита пользователя.
    wishlist = serializers.JSONField(required=False)  # Товары в списке желаний пользователя.
    cartab = serializers.IntegerField(required=False)  # Количество раз, когда пользователь добавлял товар в корзину, но не оформлял покупку.
    refurl = serializers.URLField(required=False)  # URL-адрес, с которого пришел покупатель.
    churn = serializers.FloatField(required=False)  # Вероятность оттока этого покупателя.
    camp = serializers.CharField(max_length=100, required=False)  # Рекламная кампания, которая привела пользователя.
    coupon = serializers.CharField(max_length=50, required=False)  # Код используемого купона.
    pltf = serializers.CharField(max_length=50, required=False)  # Платформа (мобильный, десктоп).
    mems = serializers.CharField(max_length=50, required=False)  # Статус членства или подписки.
    srchq = serializers.CharField(max_length=255, required=False)  # Поисковый запрос на сайте перед покупкой.
    shipm = serializers.CharField(max_length=100, required=False)  # Метод доставки.
    ret = serializers.JSONField(required=False)  # Информация о возвратах покупателя в прошлом.
    lang = serializers.CharField(max_length=10, required=False)  # Язык интерфейса.
    nviews = serializers.IntegerField(required=False)  # Общее количество просмотров сайта пользователем.
    feedb = serializers.JSONField(required=False)  # Обратная связь или комментарии покупателя.
    lgnmth = serializers.CharField(max_length=50, required=False)  # Метод входа в учетную запись.
    dev = serializers.CharField(max_length=100, required=False)  # Тип устройства.
    pricetg = serializers.CharField(max_length=50, required=False)  # Ценовая категория товара.
    recprod = serializers.BooleanField(required=False)  # Был ли товар рекомендован системой.
    fit = serializers.BooleanField(required=False)  # Подходит ли размер.
    stk = serializers.CharField(max_length=50, required=False)  # Состояние акций товара.
    adgrp = serializers.CharField(max_length=100, required=False)  # Группа рекламного объявления.
    vchat = serializers.BooleanField(required=False)  # Использование виртуального чата или ассистента.
    vtry = serializers.BooleanField(required=False)  # Виртуальная примерка или демонстрация товара.
    abtest = serializers.BooleanField(required=False)  # Был ли пользователь частью A/B теста.
    vidrev = serializers.BooleanField(required=False)  # Просмотрел ли пользователь видеообзоры или демонстрации товара.
    pback = serializers.BooleanField(required=False)  # Просил ли пользователь уведомление о поступлении товара.
    mktseg = serializers.CharField(max_length=100, required=False)  # Маркетинговый сегмент пользователя.
    intnt = serializers.CharField(max_length=50, required=False)  # Оценка намерений пользователя.
    push = serializers.BooleanField(required=False)  # Подписка на push-уведомления.
    app = serializers.BooleanField(required=False)  # Покупка через мобильное приложение.
    loytier = serializers.CharField(max_length=50, required=False)  # Уровень лояльности покупателя.
    smshare = serializers.BooleanField(required=False)  # Поделился ли пользователь покупкой в социальных сетях.
    repbuy = serializers.BooleanField(required=False)  # Повторная покупка одного и того же товара.
    gtway = serializers.CharField(max_length=50, required=False)  # Платежный шлюз.
    savwl = serializers.BooleanField(required=False)  # Сохранил ли пользователь товар в списке желаемого.
    hlpdesk = serializers.BooleanField(required=False)  # Обращался ли покупатель в службу поддержки.
    custseg = serializers.CharField(max_length=50, required=False)  # Сегментация пользователя.
    dlvryex = serializers.JSONField(required=False)  # Ожидания по доставке.
    prodsrc = serializers.CharField(max_length=100, required=False)  # Источник товара.
    paylatr = serializers.BooleanField(required=False)  # Опция "купить сейчас, заплатить позже".
    charity = serializers.BooleanField(required=False)  # Пожертвование части суммы заказа.
    
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {field: {'required': False} for field in fields}

    def validate(self, data):
        # Проверка, что у нас есть хотя бы 3 непустых значения
        non_empty_fields = [field for field, value in data.items() if value]
        
        # Проверка, что хотя бы одно из полей - это либо телефон, либо почта
        if len(non_empty_fields) < 3 or (not data.get('tel') and not data.get('eml')):
            raise serializers.ValidationError("You must provide at least three fields, including either a phone number or an email address.")

        return data

    def create(self, validated_data):
        non_empty_fields = [field for field, value in validated_data.items() if value]
        
        if len(non_empty_fields) < 3 or (not validated_data.get('tel') and not validated_data.get('eml')):
            unrecognized_order = UnrecognizedOrder.objects.create(**validated_data)
            return unrecognized_order
        
        return super().create(validated_data)