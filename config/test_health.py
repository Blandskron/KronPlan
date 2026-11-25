# Copyright (c) 2026 Blandskron. All rights reserved.
# Author: Bastian Landskron (Cybersecurity, DevOps & AI)

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_health_check(client):
    url = reverse('health_check')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_renders_landing_for_anonymous_visitors(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert b'KronPlan' in response.content


@pytest.mark.django_db
def test_home_redirects_authenticated_users_to_dashboard(client):
    User.objects.create_user(username='homeuser', password='StrongPassword123!')
    client.login(username='homeuser', password='StrongPassword123!')
    response = client.get(reverse('home'))
    assert response.status_code == 302
    assert response.url == reverse('dashboard')
