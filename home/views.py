from django.shortcuts import render , HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import feedparser

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Logged in as {request.user.first_name} {request.user.last_name}")
    else:
        return render(request,"home.html")
    
    
def news(request):
    feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")
    entries = feed.entries
    # https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    paginator = Paginator(entries, 8)
    page = request.GET.get('page', 1)
    try:
        post_pagin = paginator.page(page)
    except PageNotAnInteger:
        post_pagin = paginator.page(1)
    except EmptyPage:
        post_pagin = paginator.page(paginator.num_pages)
    for entry in post_pagin:
         entry['thumbnail'] = entry.links[1]['href']
    context = {"post_pagin":post_pagin}
    return render(request, 'news.html', context)