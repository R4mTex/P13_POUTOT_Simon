import pytest

from django.urls import reverse
from django.test import Client
from authentication.models import User
from blog.models import Blog, Contract, SignatureModel
from pytest_django.asserts import assertTemplateUsed
from datetime import date, timedelta


client = Client()


@pytest.mark.django_db
def test_editTool_view_get():
    '''login requirement'''
    User.objects.create_user(username='Test User',
                             email='',
                             password='',
                             )
    client.login(username='Test User', email='', password='')
    path = reverse('edit-tool', kwargs={'userID': User.objects.all()[0].id})
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
    path = reverse('edit-tool', kwargs={'userID': User.objects.all()[0].id})
    responseEditTool = client.post(path, data={'name': [''],
                                               'image': [''],
                                               'category': [''],
                                               'description': [''],
                                               'location': [''],
                                               'availabalityStart': [''],
                                               'initial-availabalityStart': [''],
                                               'availabalityEnd': [''],
                                               'initial-availabalityEnd': ['']
                                               })
    assert responseEditTool.status_code == 200
    assertTemplateUsed(responseEditTool, "blog/editTool.html")

    responseEditTool = client.post(path, data={'name': ['Test'],
                                               'image': [''],
                                               'category': ['Other'],
                                               'description': ['Test'],
                                               'location': ['La Barrie 46500 GRAMAT'],
                                               'availabalityStart': [date.today()],
                                               'initial-availabalityStart': [date.today()],
                                               'availabalityEnd': [date.today() + timedelta(days=1)],
                                               'initial-availabalityEnd': [date.today() + timedelta(days=1)]
                                               })
    assert responseEditTool.status_code == 302
    assert responseEditTool.url == '/user/' + str(User.objects.all()[0].id) + '/profile/'


@pytest.mark.django_db
def test_personalTools_view_get():
    '''login requirement'''
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
                        author=User.objects.all()[0]
                        )
    Blog.objects.create(name='Test Blog 2',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-18',
                        availabalityEnd='2023-09-20',
                        deposit='True',
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('personal-tools', kwargs={'userID': User.objects.all()[0].id})
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
                        author=User.objects.all()[0]
                        )
    Blog.objects.create(name='Test Blog 2',
                        image='userPersonalToolPicture/test.png',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.all()[0]
                        )
    Blog.objects.create(name='Test Blog 3',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-18',
                        availabalityEnd='2023-09-20',
                        deposit='True',
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('personal-tools', kwargs={'userID': User.objects.all()[0].id})
    responseToolDetails = client.post(path, data={'toolDetails': [Blog.objects.all()[0].id]})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/' + str(User.objects.all()[0].id) + '/tool/' + str(Blog.objects.all()[0].id) +'/details/'

    responseSupprTool = client.post(path, data={'supprTool': [Blog.objects.all()[0].id]})
    assert responseSupprTool.status_code == 200
    assertTemplateUsed(responseSupprTool, "blog/personalTools.html")

    responseSupprTool = client.post(path, data={'supprTool': [Blog.objects.all()[1].id]})
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
                             phoneNumber='0000000000',)
    client.login(username='Test User', email='', password='')
    path = reverse('member-tools', kwargs={'userID': User.objects.all()[0].id, 'memberID': User.objects.all()[1].id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/personalTools.html")


@pytest.mark.django_db
def test_memberTools_view_post():
    User.objects.create_user(username='Test User',
                             email='',
                             password='',)
    User.objects.create_user(username='Test User 2',
                             email='test@test.com',
                             password='',
                             fullname='TestTest',
                             phoneNumber='0000000000',)
    Blog.objects.create(name='Test Blog',
                        category='Other',
                        location='La Barrie 46500 GRAMAT',
                        description='Test',
                        availabalityStart='2023-09-12',
                        availabalityEnd='2023-09-13',
                        deposit='True',
                        author=User.objects.all()[0])
    client.login(username='Test User', email='', password='')
    path = reverse('member-tools', kwargs={'userID': User.objects.all()[0].id, 'memberID': User.objects.all()[1].id})
    responseToolDetails = client.post(path, data={'toolDetails': [Blog.objects.all()[0].id]})
    assert responseToolDetails.status_code == 302
    assert responseToolDetails.url == '/user/' + str(User.objects.all()[0].id) + '/tool/' + str(Blog.objects.all()[0].id) + '/details/'

    responseAddTool = client.post(path, data={'addTool': [Blog.objects.all()[0].id]})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "blog/personalTools.html")

    responseRemoveTool = client.post(path, data={'removeTool': [Blog.objects.all()[0].id]})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "blog/personalTools.html")

    responseAuthorProfile = client.post(path, data={'authorProfile': [User.objects.all()[1].id]})
    assert responseAuthorProfile.status_code == 302
    assert responseAuthorProfile.url == '/user/' + str(User.objects.all()[0].id) + '/member/' + str(User.objects.all()[1].id) + '/member-profile/'


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
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('tool-details', kwargs={'userID': User.objects.all()[0].id, 'toolID': Blog.objects.all()[0].id})
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
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('tool-details', kwargs={'userID': User.objects.all()[0].id, 'toolID': Blog.objects.all()[0].id})
    responseAddTool = client.post(path, data={'addTool': [Blog.objects.all()[0].id]})
    assert responseAddTool.status_code == 200
    assertTemplateUsed(responseAddTool, "blog/toolDetails.html")

    responseRemoveTool = client.post(path, data={'removeTool': [Blog.objects.all()[0].id]})
    assert responseRemoveTool.status_code == 200
    assertTemplateUsed(responseRemoveTool, "blog/toolDetails.html")

    responseBorrowRequest = client.post(path, data={'borrowRequest': [Blog.objects.all()[0].id]})
    assert responseBorrowRequest.status_code == 302
    assert responseBorrowRequest.url == '/user/' + str(User.objects.all()[0].id) + '/tool/' + str(Blog.objects.all()[0].id) + '/details/borrow-request-contract/'

    responseSupprTool = client.post(path, data={'supprTool': [Blog.objects.all()[0].id]})
    assert responseSupprTool.status_code == 302
    assert responseSupprTool.url == '/user/' + str(User.objects.all()[0].id) + '/research/'


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
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('borrow-request-form', kwargs={'userID': User.objects.all()[0].id, 'toolID': Blog.objects.all()[0].id})
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
                        availabalityStart=date.today(),
                        availabalityEnd=date.today() + timedelta(days=1),
                        deposit='True',
                        author=User.objects.all()[0]
                        )
    client.login(username='Test User', email='', password='')
    path = reverse('borrow-request-form', kwargs={'userID': User.objects.all()[0].id, 'toolID': Blog.objects.all()[0].id})

    response = client.post(path, data={'startOfUse': [date.today()],
                                       'initial-startOfUse': [date.today()],
                                       'endOfUse': [date.today() + timedelta(days=1)],
                                       'applicantName': ['TestTest'],
                                       'applicantApproval': ['Read and Approved'],
                                       'requestDate': [date.today()],
                                       'initial-requestDate': [date.today()],
                                       'applicantPostalAddress': ['La Barrie 46500 GRAMAT'],
                                       'signature': ['[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]'],
                                       'sendContract': ['']})
    assert response.status_code == 302
    assert response.url == '/user/' + str(User.objects.all()[0].id) + '/tool/' + str(Blog.objects.all()[0].id) + '/details/borrow-request-confirmation/'


@pytest.mark.django_db
def test_consentToBorrowForm_view_get():
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
                        author=User.objects.all()[1]
                        )
    SignatureModel.objects.create(user=User.objects.all()[0],
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.all()[1],
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.all()[0],
                            supplier=User.objects.all()[1],
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.all()[0],
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.all()[0],
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.all()[1],
                            )
    client.login(username='Test User', email='', password='')
    path = reverse('consent-to-borrow-form', kwargs={'userID': User.objects.all()[0].id, 'contractID': Contract.objects.all()[0].id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/consentToBorrowForm.html")


@pytest.mark.django_db
def test_consentToBorrowForm_view_post():
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
                        author=User.objects.all()[1])
    SignatureModel.objects.create(user=User.objects.all()[0],
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.all()[1],
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.all()[0],
                            supplier=User.objects.all()[1],
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.all()[0],
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.all()[0],
                            supplierName='',
                            supplierApproval='',
                            approvalDate=date.today(),
                            supplierPostalAddress='',
                            supplierSignature=SignatureModel.objects.all()[1],
                            )
    client.login(username='Test User 2', email='test@test.com', password='')
    path = reverse('consent-to-borrow-form', kwargs={'userID': User.objects.all()[1].id, 'contractID': Contract.objects.all()[0].id})
    response = client.post(path, data={'supplierName': ['Test2Test2'],
                                       'supplierApproval': ['Read and Approved'],
                                       'approvalDate': [date.today()],
                                       'supplierPostalAddress': ['La Barrie 46500 GRAMAT'],
                                       'signature': ['[{"x":[180,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]'],
                                       'consent': ['']})
    assert response.status_code == 302
    assert response.url == '/user/' + str(User.objects.all()[1].id) + '/contract/' + str(Contract.objects.all()[0].id) + '/consent-to-borrow-confirmation/'


@pytest.mark.django_db
def test_consentToBorrowConfirmation_view_get():
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
                        author=User.objects.all()[1])
    SignatureModel.objects.create(user=User.objects.all()[0],
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.all()[1],
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.all()[0],
                            supplier=User.objects.all()[1],
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.all()[0],
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.all()[0],
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.all()[1],
                            )
    client.login(username='Test User', email='', password='')
    path = reverse('consent-to-borrow-confirmation', kwargs={'userID': User.objects.all()[0].id, 'contractID': Contract.objects.all()[0].id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/consentToBorrowConfirmation.html")


@pytest.mark.django_db
def test_borrowContractPDF_view_get():
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
                        author=User.objects.all()[1])
    SignatureModel.objects.create(user=User.objects.all()[0],
                                  signature='[{"x":[178,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    SignatureModel.objects.create(user=User.objects.all()[1],
                                  signature='[{"x":[179,172,165,156,145,133,121,112,102,96,92,97,103,116,131,146,169,185,202,220,234,245,254,261,266,268,268,267,262,256,247,238,229,218,208,198,188,181,177,177,176,176,178,183,187,194,201,208,213,219,211,201,189,174,154,135,114,100,86,75,67,62,60,60,60,60,61,62,64],"y":[59,56,56,54,54,54,53,51,50,48,46,39,34,28,22,19,14,13,11,11,12,16,20,26,32,37,44,50,56,61,67,71,74,77,78,78,78,77,75,70,64,56,48,39,32,23,16,9,5,0,1,5,9,15,23,31,41,51,62,75,88,100,108,118,125,131,136,141,145]}]',)
    Contract.objects.create(applicant=User.objects.all()[0],
                            supplier=User.objects.all()[1],
                            applicantName='TestTest',
                            contractedBlog=Blog.objects.all()[0],
                            startOfUse=date.today(),
                            endOfUse=date.today() + timedelta(days=1),
                            applicantApproval='Read and Approved',
                            requestDate=date.today(),
                            applicantPostalAddress='La Barrie 46500 GRAMAT',
                            applicantSignature=SignatureModel.objects.all()[0],
                            supplierName='Test2Test2',
                            supplierApproval='Read and Approved',
                            approvalDate=date.today(),
                            supplierPostalAddress='La Barrie 46500 GRAMAT',
                            supplierSignature=SignatureModel.objects.all()[1],
                            )
    client.login(username='Test User', email='', password='')
    path = reverse('borrowContract', kwargs={'userID': User.objects.all()[0].id, 'contractID': Contract.objects.all()[0].id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "blog/borrowContract.html")
