import pytest
from django.urls import reverse, resolve
from authentication.models import User


# Create your tests here.
@pytest.mark.django_db
def test_about_url():
    User.objects.create(username='Test User',
                        email='',
                        password='',
                        )
    path = reverse('about', kwargs={'userID': User.objects.all()[0].id})

    assert path == '/user/' + str(User.objects.all()[0].id) + '/about/'
    assert resolve(path).view_name == "about"
