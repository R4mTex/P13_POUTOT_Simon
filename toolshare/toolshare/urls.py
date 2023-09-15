"""
URL configuration for toolshare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views as authView
from blog import views as blogView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    ### Home / About / Contact / Publisher ###
    path('', authView.Home.as_view(template_name='authentication/home.html'), name='home'),
    path('pdf', authView.pdf.as_view(template_name='authentication/pdf.html'), name='pdf'),
    path('user/<int:userID>/about/', authView.About.as_view(template_name='authentication/about.html'), name='about'),
    path('user/<int:userID>/contact/', authView.Contact.as_view(template_name='authentication/contact.html'), name='contact'),
    path('user/<int:userID>/contact/success/', authView.Contact.as_view(template_name='authentication/contactSuccess.html'), name='contact-success'),
    path('user/<int:userID>/publisher/', authView.Publisher.as_view(template_name='authentication/publisher.html'), name='publisher'),
    ### Research ###
    path('user/<int:userID>/research/', authView.Research.as_view(template_name='authentication/research.html'), name='research'),
    path('user/<int:userID>/research/all-items/', authView.Research.as_view(template_name='authentication/research.html'), name='research-all-items'),
    path('user/<int:userID>/research/all-tools/', authView.Research.as_view(template_name='authentication/research.html'), name='research-all-tools'),
    path('user/<int:userID>/research/all-equipments/', authView.Research.as_view(template_name='authentication/research.html'), name='research-all-equipments'),
    path('user/<int:userID>/research/most-popular/', authView.Research.as_view(template_name='authentication/research.html'), name='research-most-popular'),
    path('user/<int:userID>/research/best-rated/', authView.Research.as_view(template_name='authentication/research.html'), name='research-best-rated'),
    ### /Research ###
    path('user/<int:userID>/favorites/', authView.Favorites.as_view(template_name='authentication/favorites.html'), name='favorites'),
    path('user/<int:userID>/profile/', authView.Profile.as_view(template_name='authentication/profile.html'), name='profile'),
    path('user/<int:userID>/member/<int:memberID>/member-profile/', authView.memberProfile.as_view(template_name='authentication/profile.html'), name='member-profile'),
    path('user/<int:userID>/edit-profile/', authView.editProfile.as_view(template_name='authentication/editProfile.html'), name='edit-profile'),
    path('user/<int:userID>/edit-tool/', blogView.editTool.as_view(template_name='blog/editTool.html'), name='edit-tool'),
    path('user/<int:userID>/personal-tools/', blogView.personalTools.as_view(template_name='blog/personalTools.html'), name='personal-tools'),
    path('user/<int:userID>/member/<int:memberID>/member-tools/', blogView.memberTools.as_view(template_name='blog/personalTools.html'), name='member-tools'),
    path('registration/', authView.Registration.as_view(template_name='authentication/registration.html'), name='registration'),
    path('user/<int:userID>/tool/<int:toolID>/details/', blogView.toolDetails.as_view(template_name='blog/toolDetails.html'), name='tool-details'),
    path('user/<int:userID>/tool/<int:toolID>/details/borrow-request-contract/', blogView.borrowRequestForm.as_view(template_name='blog/borrowRequestConfirmation.html'), name='borrow-request-confirmation'),
    path('user/<int:userID>/tool/<int:toolID>/details/borrow-request-confirmation/', blogView.borrowRequestForm.as_view(template_name='blog/borrowRequestForm.html'), name='borrow-request-form'),
    path('user/<int:userID>/contract/<int:contractID>/consent-to-borrow-contract/', blogView.consentToBorrowForm.as_view(template_name='blog/consentToBorrowForm.html'), name='consent-to-borrow-form'),


    # Login / Logout / Change Password Urls
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',
                                                redirect_authenticated_user=True),
                                                name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
                                                                   name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
                                                                            name='password_change_done'),

    # Reset Password Urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)