from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from openai import OpenAI
from django.conf import settings
from django.contrib.auth.decorators import login_required
from articles.models import Article, Comment
from django.utils import timezone
from .cache import Cache
import json


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
    1. You are an experienced email forger.
    2. Write the text using the user's style.
    
    # Audience
    1. A thinking internet audience that will not be satisfied with a meaningless post
    
    # Your task
    1. According to the topic and the user's past posts, write an exciting and creative text with a limit of 290 characters maximum and 10 characters minimum.
    2. The text should be interesting and informative.
    3. The text should completely match the user's style.
    
    # Input
    1. Subject
    3. The user's last 10 posts
    
    # Output
    1. Output only the text.
    2. Limit of maximum 290 characters and minimum 10 characters.
    3. The output should match the language in which the subject and the latest posts are written.
    
    # Notes:
    1. No hashtags needed!
    '''
    title = request.GET.get('title')
    prev = Article.objects.all()[:10]
    prev = ''.join([f'Начало статьи: {a.body} Конец статьи.' for a in prev])
    user = f'Title: {title}, Previous posts: {prev}'
    text = ai_request(system, user)
    return JsonResponse({'text':text})

def opinion(request):
    system = '''
    #Role
    1. You are an experienced marketer who qualitatively tracks opinions about people and products.
    
    # Audience
    1. Internet audience
    
    # Your task
    1. Analyze the latest comments under the user's post and return the analysis result.
    
    # Input
    1. The latest comments under the user's posts.
    
    # Output
    1. JSON
    2. In the reflections tags, you must first write your thoughts after analyzing the comments.
    3. In the result tags, you must return the final result that the user will see.
    4. The language must be russian
    
    # Notes:
    1. You must write an opinion in one paragraph. You can also give advice.
    2. You must write on russian
    
    # Example
    User:
    ("Cool content", "Awesome at times, but very dry, could have used some emoticons", "Could have been brief")
    Your answer:
    {
    "reflections": "Your thoughts...",
    "result": "Overall positive feedback, but some people are not happy with the dryness of the content and its volume. Advice: add emoticons and write briefly."
    }
    '''

    user = request.user
    comments = Comment.objects.filter(Q(article__author=user) & ~Q(user=user)).order_by('-upload_at')[:20]
    comments_list = tuple([c.body for c in comments])
    if cache.check(comments_list):
        result = cache.get(comments_list)
    else:
        result_json = ai_request(system, str(comments_list))
        result = json.loads(result_json).get('result')
        cache.set(comments_list, result)
    return JsonResponse({'result': result})
