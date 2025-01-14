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

@login_required()
def tweet_plan(request):
    system = '''
    # Role
    1. You make a plan for writing a tweet.
    
    # Audience
    1. Internet audience of different ages.
    
    # Your task
    1. Based on the topic, make a mini-plan for writing a tweet so that it is interesting and engaging.
    
    # Output
    1. Output only the text separated by a dash ('-') for each stage of the plan
    2. At the end of each line, insert <br>
    3. The output must match the language in which the topic is written
    
    # Notes:
    1. Hashtags are not needed!
    '''
    title = request.POST.get('title')
    plan = ai_request(system, title)
    return JsonResponse({'plan': plan})

def make_text(request):
    system = '''
    # Role
    1. You are a skilled writer who has a better command of words than anyone in the world.
    
    # Audience
    1. A thinking internet audience who will not be satisfied with a meaningless post
    
    # Your task
    1. In accordance with the plan and topic, write an exciting and creative text with a limit of 290 characters.
    2. The text must be interesting and meaningful.
    
    # Output data
    1. Output only the text
    2. Limit of 290 characters
    3. The output data must match the language in which the topic and plan are written
    
    # Notes:
    1. Hashtags are not needed!
    '''
    title = request.GET.get('title')
    plan = request.GET.get('plan')
    user = f'Title: {title}, Plan: {plan}'
    text = ai_request(system, user)
    return JsonResponse({'text':text})
