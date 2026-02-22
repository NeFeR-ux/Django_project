from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.flatpages.models import FlatPage


def page1(request):
    flatpage = get_object_or_404(FlatPage, url='/page1/')
    return render(request, 'pages/page1.html', {'flatpage': flatpage})

def page2(request):
    return render(request, 'pages/page2.html')

@login_required
def page3(request):
    return render(request, 'pages/page3.html')

def test(request):
    return render(request, 'flatpages/test.html')

