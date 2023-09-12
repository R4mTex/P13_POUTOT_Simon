import pytest

from django.urls import reverse
from django.test import Client
from authentication.models import User
from blog.models import Blog
from pytest_django.asserts import assertTemplateUsed


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
    assert response.status_code == 200
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

    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
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


@pytest.mark.django_db  
def test_favorites_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('favorites', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/favorites.html")


@pytest.mark.django_db  
def test_favorites_view_post():
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
    path = reverse('favorites', kwargs={'userID':1})
    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseRemoveTool = client.post(path, data={'removeTool': ['1']})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "authentication/favorites.html")


@pytest.mark.django_db
def test_profile_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('profile', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/profile.html")


@pytest.mark.django_db
def test_profile_view_post():
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
    path = reverse('profile', kwargs={'userID':1})
    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responsePersonalTools = client.post(path, data={'showPersonalTools': ['1']})
    assert responsePersonalTools.status_code == 302
    assert responsePersonalTools.url == '/user/1/personal-tools/'


@pytest.mark.django_db
def test_editProfile_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('edit-profile', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/editProfile.html")


@pytest.mark.django_db  
def test_editProfile_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('edit-profile', kwargs={'userID':1})
    responseProfilePicture = client.post(path, data={'profilePicture': ['', '']})
    assert responseProfilePicture.status_code == 200
    assertTemplateUsed(responseProfilePicture, "authentication/editProfile.html")

    responseUpdateUserProfile = client.post(path, data={'fullname': [''], 'username': ['admin'], 'email': ['poutots@gmail.com'], 'phoneNumber': [''], 'postalAddress': [''], 'bio': [''], 'updateUserProfile': ['']})
    assert responseUpdateUserProfile.status_code == 200
    assertTemplateUsed(responseUpdateUserProfile, "authentication/editProfile.html")


@pytest.mark.django_db
def test_registration_view_get():
    path = reverse('registration')
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/registration.html")


@pytest.mark.django_db  
def test_registration_view_post():
    path = reverse('registration')
    responseFullName = client.post(path, data={'fullname': [''], 'username': [''], 'password1': [''], 'password2': [''], 'email': [''], 'phoneNumber': [''], 'postalAddress': [''], 'bio': ['']})
    assert responseFullName.status_code == 200
    assertTemplateUsed(responseFullName, "authentication/registration.html")

    responseAccept = client.post(path, data={'accept': ['']})
    assert responseAccept.status_code == 200
    assertTemplateUsed(responseAccept, "authentication/registration.html")
