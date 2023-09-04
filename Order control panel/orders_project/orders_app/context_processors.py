# context_processors.py

def theme_context_processor(request):
    theme_preference = request.COOKIES.get('theme_preference', 'light')  # 'light' по умолчанию
    return {'theme_preference': theme_preference}
