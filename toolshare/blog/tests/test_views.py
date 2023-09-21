import pytest

from django.urls import reverse
from django.test import Client
from authentication.models import User
from blog.models import Blog
from pytest_django.asserts import assertTemplateUsed


client = Client()

@pytest.mark.django_db
def test_editTool_view_get():
    '''login requirement'''
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('edit-tool', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/editTool.html")


@pytest.mark.django_db
def test_editTool_view_post():
    '''login requirement'''
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('edit-tool', kwargs={'userID':1})
    responseeEditTool = client.post(path, data={'name': [''], 'image': [''], 'category': [''], 'description': [''], 'location': [''], 'availabalityStart': [''], 'initial-availabalityStart': [''], 'availabalityEnd': [''], 'initial-availabalityEnd': ['']})
    assert responseeEditTool.status_code == 200
    assertTemplateUsed(responseeEditTool, "blog/editTool.html")


@pytest.mark.django_db
def test_personalTools_view_get():
    '''login requirement'''
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('personal-tools', kwargs={'userID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/personalTools.html")


@pytest.mark.django_db  
def test_personalTools_view_post():
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
    path = reverse('personal-tools', kwargs={'userID':1})
    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseSupprTool = client.post(path, data={'supprTool': ['1']})
    assert responseSupprTool.status_code == 200
    assertTemplateUsed(responseSupprTool, "blog/personalTools.html")


@pytest.mark.django_db
def test_memberTools_view_get():
    '''login requirement'''
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
    path = reverse('member-tools', kwargs={'userID':1, 'memberID':2})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/personalTools.html")


@pytest.mark.django_db  
def test_memberTools_view_post():
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
    path = reverse('member-tools', kwargs={'userID':1, 'memberID':2})
    responseToolDetails = client.post(path, data={'toolDetails': ['1']})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/1/tool/1/details/'

    responseAddTool = client.post(path, data={'addTool': ['1']})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "blog/personalTools.html")

    responseRemoveTool = client.post(path, data={'removeTool': ['1']})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "blog/personalTools.html")

    responseAuthorProfile = client.post(path, data={'authorProfile': ['2']})
    assert responseAuthorProfile.status_code == 302
    assert responseAuthorProfile.url == '/user/1/member/2/member-profile/'


@pytest.mark.django_db
def test_toolDetails_view_get():
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
    path = reverse('tool-details', kwargs={'userID':1, 'toolID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/toolDetails.html")


@pytest.mark.django_db
def test_toolDetails_view_post():
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
    path = reverse('tool-details', kwargs={'userID':1, 'toolID':1})
    responseAddTool = client.post(path, data={'addTool': ['1']})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "blog/toolDetails.html")

    responseRemoveTool = client.post(path, data={'removeTool': ['1']})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "blog/toolDetails.html")

    responseBorrowRequest = client.post(path, data={'borrowRequest': ['1']})
    assert responseBorrowRequest.status_code == 302
    assert responseBorrowRequest.url == '/user/1/tool/1/details/borrow-request/'

    responseSupprTool = client.post(path, data={'supprTool': ['1']})
    assert responseSupprTool.status_code == 302
    assert responseSupprTool.url == '/user/1/research/'


@pytest.mark.django_db
def test_borrowRequestForm_view_get():
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
    path = reverse('borrow-request-form', kwargs={'userID':1, 'toolID':1})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/borrowRequestForm.html")


@pytest.mark.django_db
def test_borrowRequestForm_view_post():
    User.objects.create_user(username='Test User',
                             fullname='TestTest',
                             email='',
                             password='',
                             postalAddress='La Barrie 46500 GRAMAT'
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
    path = reverse('borrow-request-form', kwargs={'userID':1, 'toolID':1})
    response = client.post(path, data={'applicantName': ['TestTest'], 
                                       'applicantApproval': ['Read and approved'], 
                                       'requestDate': ['2023-09-12'], 
                                       'initial-requestDate': ['2023-09-12'], 
                                       'applicantPostalAddress': ['La Barrie 46500 GRAMAT'], 
                                       'applicantSignature': ['[{"x":[154,136,122,112,104,101,109,119,136,157,179,198,214,235,246,253,254,246,232,213,187,159,138,119,109,105,104,105,108,115,126,137,148,159,168,176,181,185,188,188,185,175,162,145,131,114,102,94,90,87,87,91,99,110,125,144,157,173,182,188,192,190,186],"y":[55,58,59,60,61,63,64,66,66,66,64,61,59,55,52,50,46,44,42,40,40,39,41,46,53,59,65,71,80,88,98,104,109,110,112,110,106,101,94,87,76,62,49,37,29,22,20,20,21,27,33,43,57,71,87,101,109,116,120,121,122,118,115]}]'], 
                                       'sendContract': ['']})
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/borrowRequestForm.html")

"""
@pytest.mark.django_db
def test_consentToBorrowForm_view_get():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('consent-to-borrow-form', kwargs={})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/consentToBorrowForm.html")
"""