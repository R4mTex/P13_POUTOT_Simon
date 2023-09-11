import pytest

from django.urls import reverse, resolve
from django.shortcuts import render, redirect 
from django.test import Client
from authentication.models import User
from pytest_django.asserts import assertTemplateUsed
from authentication import forms
from authentication.views import Registration, Profile
from django.contrib.auth import views as auth_views
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from toolshare import settings
from django.core.mail import EmailMessage 

"""
@pytest.mark.django_db  
def test_book_infos_view():
    client = Client()
    Book.objects.create(author = "Jules Verne",
                        title = "20 milles lieues sous les mers")
    path = reverse('infos', kwargs={'pk':1})
    response = client.get(path)
    content = response.content.decode()
    expected_content = "<p>Jules Verne | 20 milles lieues sous les mers</p>"

    assert content == expected_content
    assert response.status_code == 200
    assertTemplateUsed(response, "book_infos.html")
"""

client = Client()

@pytest.mark.django_db
def test_home_view_get():
    '''login requirement'''
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('home')
    response = client.get(path)

    expected_value = 200
    assert response.status_code == expected_value
    assertTemplateUsed(response, "authentication/home.html")


@pytest.mark.django_db  
def test_about_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('about', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/about.html")


@pytest.mark.django_db  
def test_contact_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('contact', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/contact.html")


@pytest.mark.django_db  
def test_contact_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    formData = {'subject': "Test", 'message': "Test"}
    form = forms.ContactForm(data=formData)
    user = User.objects.get(id=1)
    name = user.fullname
    emailFrom = user.email
    if form.is_valid():
        subject = form.cleaned_data['subject'] 
        message = "The user named " + name + " has sent you a message : \n" + form.cleaned_data['message'] + ".\nYou can reach him at this address : " + emailFrom 
        recipientList = [settings.EMAIL_HOST_USER,]
        email = EmailMessage(subject, message, emailFrom, recipientList) 
        assert email.send() == True
        path = reverse('contact-success', kwargs={'userID':1})
        response = client.post(path)
        assert response.status_code == 200
    path = reverse('contact', kwargs={'userID':1})
    response = client.post(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/contact.html")


@pytest.mark.django_db  
def test_publisher_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('publisher', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/publisher.html")


@pytest.mark.django_db  
def test_research_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('research', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/research.html")


@pytest.mark.django_db  
def test_research_view_post(request):
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    request.POST.get('allItems')
    if "allItems" in request.POST:
        assert None
    path = reverse('research', kwargs={'userID':1})
    response = client.post(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/research.html")