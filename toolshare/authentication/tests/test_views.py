import pytest

from django.urls import reverse, resolve
from django.shortcuts import render, redirect 
from django.test import Client
from authentication.models import User
from blog.models import Blog
from pytest_django.asserts import assertTemplateUsed
from authentication import forms
from authentication.views import Registration, Profile
from django.contrib.auth import views as auth_views
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from toolshare import settings
from django.core.mail import EmailMessage
from django import urls

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
def test_research_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-12',
                        availabalityEnd='2023-09-13',
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('research', kwargs={'userID':1})

    responseAllItems = client.post(path, data={'allItems': ['']})
    assert responseAllItems.status_code == 200
    assertTemplateUsed(responseAllItems, "authentication/research.html")

    responseAllTools = client.post(path, data={'allTools': ['']})
    assert responseAllTools.status_code == 200
    assertTemplateUsed(responseAllTools, "authentication/research.html")

    responseEquipments = client.post(path, data={'allEquipments': ['']})
    assert responseEquipments.status_code == 200
    assertTemplateUsed(responseEquipments, "authentication/research.html")

    responseMostPopular = client.post(path, data={'mostPopular': ['']})
    assert responseMostPopular.status_code == 200
    assertTemplateUsed(responseMostPopular, "authentication/research.html")

    responseBestRated = client.post(path, data={'bestRated': ['']})
    assert responseBestRated.status_code == 200
    assertTemplateUsed(responseBestRated, "authentication/research.html")

    responseToolDetails= client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'
    
    responseAddTool = client.post(path, data={'addTool': ['1']})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "authentication/research.html")

    responseRemoveTool = client.post(path, data={'removeTool': ['1']})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "authentication/research.html")

    responseSupprTool = client.post(path, data={'supprTool': ['1']})
    assert responseSupprTool.status_code == 200
    assertTemplateUsed(responseSupprTool, "authentication/research.html")

    responseAuthorProfile = client.post(path, data={'authorProfile': ['1']})
    assert responseAuthorProfile.status_code == 302
    assert responseAuthorProfile.url == '/user/1/profile/'


@pytest.mark.django_db  
def test_memberProfile_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    User.objects.create_user(username='Test User 2',
                             email='test@test.com',
                             password='',
                             fullname='TestTest',
                             phoneNumber='0000000000',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('member-profile', kwargs={'userID':1, 'memberID':2})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/profile.html")


@pytest.mark.django_db  
def test_memberProfile_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    User.objects.create_user(username='Test User 2',
                             email='test@test.com',
                             password='',
                             fullname='TestTest',
                             phoneNumber='0000000000',
                             )
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-12',
                        availabalityEnd='2023-09-13',
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('member-profile', kwargs={'userID':1, 'memberID':2})

    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseShowPersonalTools = client.post(path, data={'showPersonalTools': ['2']})
    assert responseShowPersonalTools.status_code == 302
    assert responseShowPersonalTools.url == '/user/1/member/2/member-tools/'