# Copyright (c) 2026 Blandskron. All rights reserved.
# Author: Bastian Landskron (Cybersecurity, DevOps & AI)

from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": "ok"})


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('accounts/', include('accounts.urls')),
    path('', include('rooms.urls')),
    path('', home, name='home'),
]
