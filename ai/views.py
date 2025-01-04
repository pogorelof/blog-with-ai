from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
from django.contrib.auth.decorators import login_required
from articles.models import Article
from django.utils import timezone
from .cache import Cache


cache = Cache()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def summarize_subscriptions(request):
    system = '''
    You receive news for the day. You must summarize this news. Take only the most important and return.

    # Steps
    1. Get news
    2. Give a brief summary of the day

    # Output format
    - Output only the summary text separated by a dash ('-') for each fact
    - At the end of the line insert <br>
    
    # Note
    - You should not add anything of your own or be biased
    '''
    
    now = timezone.now()
    start_of_day = now.replace(hour=1, minute=0, second=0, microsecond=0)
    articles_for_day = Article.objects.filter(upload_at__gte=start_of_day, upload_at__lte=now).exclude(author=request.user)
    if not articles_for_day.exists():
        return JsonResponse({'text': 'Сегодня новостей нет'})
    articles_for_day = ''.join([f'Начало статьи: {a.body} Конец статьи.' for a in articles_for_day])
    
    if cache.check(articles_for_day):
        text = cache.get(articles_for_day)
    else:
        text = ai_request(system, articles_for_day)
        cache.set(articles_for_day, text)
    
    return JsonResponse({'text': text})

def ai_request(system, user):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {'role':'system', 'content': system},
        {'role':'user', 'content': user}
    ],
    response_format={
        "type": "text"
    },
    temperature=1,
    max_tokens=10000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content.strip()