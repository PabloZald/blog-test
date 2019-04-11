from django.conf.urls import url


from .views import (
    CourseListView,
    MyCoursesListView, 
    CourseDetailView, 
    # CourseCreateView, 
    # CourseUpdateView,
    # CourseDeleteView,
    LectureDetailView,
    CoursePurchaseView,
    ReviewView,
    signup_login_view,
    CreateCertificateView,
    GeneratePdf,
    MyCertificatesListView,
    )

urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    # url(r'^mis-certificados/$', MyCertificatesListView.as_view(), name='my-certificates'),
    url(r'^certificado/(?P<slug>[\w-]+)/$', GeneratePdf.as_view(), name='show-certificate'),
    url(r'^mis-cursos/$', MyCoursesListView.as_view(), name='my-courses'),
    url(r'^mis-certificados/$', MyCertificatesListView.as_view(), name='my-certificates'),
    url(r'^(?P<slug>[\w-]+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^signup-login/(?P<courseslug>[\w-]+)/$', signup_login_view, name='signup-login'),
    url(r'^(?P<slug>[\w-]+)/purchase/$', CoursePurchaseView.as_view(), name='purchase'),
    url(r'^(?P<slug>[\w-]+)/create-certificate/$', CreateCertificateView.as_view(), name='create-certificate'),


    url(r'^(?P<slug>[\w-]+)/review/$', ReviewView.as_view(), name='review'),
    url(r'^(?P<cslug>[\w-]+)/(?P<lslug>[\w-]+)/$', LectureDetailView.as_view(), name='lecture-detail'),

    # url(r'^(?P<slug>[\w-]+)/edit/$', CourseUpdateView.as_view(), name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', CourseDeleteView.as_view(), name='delete'),
]