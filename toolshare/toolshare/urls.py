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
    path('', authView.home, name='home'),
    path('research', authView.research, name='research'),
    path('favorites/', authView.favorites, name='favorites'),
    path('profile/', authView.Profile.as_view(template_name='authentication/profile.html'), name='profile'),
    path('edit-profile/<int:id>/', authView.editProfile.as_view(template_name='authentication/editProfile.html'), name='edit-profile'),
    path('edit-tool/<int:id>/', blogView.blog_and_photo_upload, name='edit-tool'),
    path('personal-tools/<int:id>/', blogView.personalTools.as_view(template_name='blog/personalTools.html'), name='personal-tools'),
    path('registration/', authView.Registration.as_view(template_name='authentication/registration.html'),
                                                     name='registration'),

    path('blog/create', blogView.blog_and_photo_upload, name='blog_create'),


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