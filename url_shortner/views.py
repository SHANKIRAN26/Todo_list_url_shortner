from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import UrlShortner
import string
import random
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def url_home(request):
    # print(request.path)
    if request.method == "POST":
        url = request.POST["redirect_url"]
        length = 6
        while True:
            slug = "".join(random.choices(string.ascii_uppercase, k=length))
            if UrlShortner.objects.filter(slug=slug).count() == 0:
                break
        print(slug)
        # print(get_current_site(request))
        create_shortened_url = UrlShortner(slug=slug, url=url)
        create_shortened_url.save()
        data = {
            "domain": str(get_current_site(request))+str(request.path),
            "shortened_url_slug": slug
        }
        print(data["shortened_url_slug"])
        return render(request, "url_shortner/url_home.html", data)
    return render(request, "url_shortner/url_home.html")

@login_required(login_url='login')
def url_redirect(request, slug):
    redirect_url = get_object_or_404(UrlShortner, slug=slug)
    # redirect_url = UrlShortner.objects.filter(slug=slug).values()
    # print(redirect_url.url)
    return redirect(redirect_url.url)

