import pytest

from django.urls import reverse
from django.test import Client
from authentication.models import User
from blog.models import Blog, Contract, SignatureModel, Favorite
from pytest_django.asserts import assertTemplateUsed
from datetime import date, timedelta


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
    path = reverse('about', kwargs={'userID': 1})
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
    path = reverse('contact', kwargs={'userID': 1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/contact.html")


@pytest.mark.django_db
def test_contact_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    print("1", User.objects.all())
    print("2", User.objects.all()[0])
    print("3", User.objects.all()[0].id)
    print("3", User.objects.all()[0].username)
    print("3", User.objects.all()[0].email)
    print("3", User.objects.all()[0].password)
    client.login(username='Test User', email='', password='')
    path = reverse('contact', kwargs={'userID': 1})
    response = client.post(path, data={'subject': ['Test'],
                                       'message': ['Test']
                                       })
    assert response.status_code == 302
    assert response.url == '/user/1/contact/success/'

    response = client.post(path, data={'subject': ['Test']
                                       })
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/contact.html")


@pytest.mark.django_db
def test_publisher_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('publisher', kwargs={'userID': 1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/publisher.html")


@pytest.mark.django_db
def test_research_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',)
    User.objects.create_user(username='Test User 2',
                             fullname='Test2Test2',
                             email='test@test.com',
                             password='',
                             postalAddress='La Barrie 46500 GRAMAT',
                             phoneNumber='0000000000',
                             )
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.get(id=2)
                        )
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-15',
                        availabalityEnd='2023-09-16',
                        deposit='True',
                        author=User.objects.get(id=2)
                        )
    Favorite.objects.create(user=User.objects.get(id=1),
                            blog=Blog.objects.get(id=1))
    SignatureModel.objects.create(user=User.objects.get(id=1),
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.get(id=2),
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.get(id=1),
                            supplier=User.objects.get(id=2),
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.get(id=1),
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.get(id=1),
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.get(id=2),
                            )
    Contract.objects.create(applicant=User.objects.get(id=1),
                            supplier=User.objects.get(id=2),
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.get(id=1),
                            startOfUse=date.today(),
                            endOfUse='2023-09-21',
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.get(id=1),
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.get(id=2),
                            )
    client.login(username='Test User', email='', password='')
    path = reverse('research', kwargs={'userID': 1})
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
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    Blog.objects.create(name='Test Blog 2',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-18',
                        availabalityEnd='2023-09-20',
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    Blog.objects.create(name='Test Blog 3',
                        category='Equipment',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-25',
                        availabalityEnd='2023-09-30',
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    Blog.objects.create(name='Test Blog 4',
                        category='Equipment',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.get(id=1)
                        )
    Favorite.objects.create(user=User.objects.get(id=1),
                            blog=Blog.objects.get(id=1))
    Favorite.objects.create(user=User.objects.get(id=1),
                            blog=Blog.objects.get(id=2))
    Favorite.objects.create(user=User.objects.get(id=1),
                            blog=Blog.objects.get(id=3))
    client.login(username='Test User', email='', password='')
    path = reverse('research', kwargs={'userID': 1})

    responseAllTools = client.post(path, data={'allTools': ['']})
    assert responseAllTools.status_code == 200
    assertTemplateUsed(responseAllTools, "authentication/research.html")

    responseEquipments = client.post(path, data={'allEquipments': ['']})
    assert responseEquipments.status_code == 200
    assertTemplateUsed(responseEquipments, "authentication/research.html")

    responseMostPopular = client.post(path, data={'mostPopular': ['']})
    assert responseMostPopular.status_code == 200
    assertTemplateUsed(responseMostPopular, "authentication/research.html")

    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseAddTool = client.post(path, data={'addTool': ['1']})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "authentication/research.html")

    responseAddTool = client.post(path, data={'addTool': ['4']})
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
                             fullname='TestTest',
                             email='',
                             password='',
                             postalAddress='La Barrie 46500 GRAMAT'
                             )
    User.objects.create_user(username='Test User 2',
                             fullname='Test2Test2',
                             email='test@test.com',
                             password='',
                             postalAddress='La Barrie 46500 GRAMAT',
                             phoneNumber='0000000000',
                             )
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.get(id=2)
                        )
    SignatureModel.objects.create(user=User.objects.get(id=1),
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.get(id=2),
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.get(id=1),
                            supplier=User.objects.get(id=2),
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.get(id=1),
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.get(id=1),
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.get(id=2),
                            )
    client.login(username='Test User', email='', password='')
    path = reverse('member-profile', kwargs={'userID': 1, 'memberID': 2})
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
    path = reverse('member-profile', kwargs={'userID': 1, 'memberID': 2})

    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseShowPersonalTools = client.post(path, data={'showPersonalTools': ['2']})
    assert responseShowPersonalTools.status_code == 302
    assert responseShowPersonalTools.url == '/user/1/member/2/member-tools/'

    responseToolDetailsContract = client.post(path, data={'toolDetailsContract': ['1']})
    assert responseToolDetailsContract.status_code == 302
    assert responseToolDetailsContract.url == '/user/1/tool/1/details/'


@pytest.mark.django_db
def test_favorites_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('favorites', kwargs={'userID': 1})
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
    path = reverse('favorites', kwargs={'userID': 1})
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
    path = reverse('profile', kwargs={'userID': 1})
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
    path = reverse('profile', kwargs={'userID': 1})
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
    path = reverse('edit-profile', kwargs={'userID': 1})
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
    path = reverse('edit-profile', kwargs={'userID': 1})
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
