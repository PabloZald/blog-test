from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
# from django.contrib.sitemaps.views import sitemap
# from .sitemaps import CabalahiSitemap

from django.contrib.auth.views import (
                                            LoginView, 
                                            LogoutView, 
                                            PasswordResetView, 
                                            PasswordResetDoneView, 
                                            PasswordResetConfirmView, 
                                            PasswordResetCompleteView,
                                        )

from .views import (
                    AboutSettingsView,
                    _PasswordChangeView,
                    ProfilePictureUploadView,
                    UserAccountUpdateView,
                    UserGeneralUpdateView,
                    UserProfileView,
                    UserDegreeUpdateView,
                    )


urlpatterns = [ 
    # <-------- SETTINGS_URLS ---------->
    url(r'^settings/account/$', UserAccountUpdateView.as_view(), name='settings_account'),
    url(r'^settings/about/$', AboutSettingsView.as_view(), name='settings_about'),
    url(r'^settings/password/$', _PasswordChangeView.as_view(), name='settings_password_change'),
    url(r'^settings/general/$', UserGeneralUpdateView.as_view(), name='settings_general'),
    url(r'^settings/degree/$', UserDegreeUpdateView.as_view(), name='settings_degree'),
    url(r'^settings/profile-picture/$', ProfilePictureUploadView.as_view(), name='settings_profile_picture'),
    url(r'^(?P<slug>[\w-]+)/$', UserProfileView.as_view(), name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    