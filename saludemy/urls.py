from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import (
                                        LoginView, 
                                        LogoutView, 
                                        PasswordResetView, 
                                        PasswordResetDoneView, 
                                        PasswordResetConfirmView, 
                                        PasswordResetCompleteView,
                                        )
from courses.views import (
                            HomeView,
                            signup_form_step_1,
                            signup_form_step_2,
                            )
# from categories import views as categories_views
# from cabalahi_sites import views as cabalahi_sites_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(template_name = "home.html"), name='home'),
    url(r'^login/$', LoginView.as_view(
                                        redirect_authenticated_user=True, 
                                        template_name='registration/login.html'
                                        ), 
                                        name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^reset/$', PasswordResetView.as_view(
                                            email_template_name='registration/password_reset_email.html',
                                            subject_template_name='registration/password_reset_subject.txt'
                                        ),
                                        name='password_reset'),
    url(r'^reset/done/$', PasswordResetDoneView.as_view(
                                        template_name='registration/password_reset_done.html'
                                        ),
                                        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                                PasswordResetConfirmView.as_view(
                                        template_name='registration/password_reset_confirm.html'
                                        ),
                                        name='password_reset_confirm'),
    url(r'^reset/complete/$', PasswordResetCompleteView.as_view(
                                        template_name='registration/password_reset_complete.html'),
                                        name='password_reset_complete'),
    url(r'^signup/$', signup_form_step_1, name='signup'),
    url(r'^signup-step-2/$', signup_form_step_2, name='signup_step_2'),

    url(r'^dashboard/', TemplateView.as_view(template_name = "old_dashboard.html"), name='dashboard'),
    url(r'^cursos/', include('courses.urls', namespace='courses')),
    url(r'^a/', include('accounts.urls', namespace='accounts')),
    url(r'^curso/detalle', TemplateView.as_view(template_name = "course_detail.html"), name='detail'),
    url(r'^curso/leccion', TemplateView.as_view(template_name = "course_lesson.html"), name='lesson'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)