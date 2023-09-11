import pytest
from django.urls import reverse, resolve
from authentication import models

# Create your tests here.
@pytest.mark.django_db
def test_about_url():
    models.User.objects.create(username='Test User',
                                email='',
                                password='',
                                )
    path = reverse('about', kwargs={'userID': 1})

    assert path == "/user/1/about/"
    assert resolve(path).view_name == "about"
