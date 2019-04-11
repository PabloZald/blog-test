import random
import datetime
from io import BytesIO
from django.db.models import Avg
from django.core.files import File
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login, authenticate
from django.db.models import Prefetch, Q, Count
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .utils import render_to_pdf 
from django.contrib.auth.forms import (
    AuthenticationForm,)
from django.http import Http404, HttpResponse, FileResponse

# from weasyprint import HTML, CSS

from django.views.generic import (
        CreateView,
        DetailView,
        ListView,
        UpdateView,
        DeleteView,
        RedirectView,
        FormView,
        View,
    )

#from .forms import VideoForm
# from analytics.models import CourseViewEvent
# from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from categories.models import Category
from .forms import CourseForm, SignupFormStep1,SignupFormStep2, ReviewForm, SignUpForm
from .models import Course, Lecture, MyCourses, Topic, Review, Certificate, MyLecture


def signup_form_step_1(request):
    if request.user.is_authenticated():
        return redirect(reverse_lazy('courses:list'))
    if request.method == 'POST':
        form = SignupFormStep1(request.POST or None)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(reverse('signup_step_2'))
        else:
            form = SignupFormStep1(request.POST)
    else:
        form = SignupFormStep1()
    context = {
        "form": form,
        "title": 'Regístrate en la comunidad de formación en salud y bienestar',
        "step_1": True,
    }
    return render(request, 'registration/signup.html', context)


@login_required
def signup_form_step_2(request):
    if request.user.first_name:
            return redirect(reverse_lazy('courses:list'))
    if request.method == 'POST':
            form = SignupFormStep2(request.POST or None)
            if form.is_valid():
                user = request.user
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()
                return redirect(reverse('courses:list'))
            else:
                form = SignupFormStep2(request.POST)
    else:
        form = SignupFormStep2()
    context = {
            "form": form,
            "step": 'Paso 2',
            "title": 'Información para tu cuenta',
        }
    return render(request, 'registration/signup.html', context)


class HomeView(ListView):
    def get(self, request, *args, **kwargs): # GET -- retrieve view / list view / search
        if self.request.user.is_authenticated():
            return redirect('courses:list')
        course_list = Course.objects.annotate(
            avg_rating=Avg('review__rating')
            )
        context = {
            "course_list": course_list,
        }
        return render(request, "home.html", context)
        

class CourseListView(LoginRequiredMixin, ListView):
    template_name = 'courses/dashboard.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        # print(dir(context.get('page_obj')))
        user = self.request.user
        context['categories_list'] = Category.objects.all()
        context['title'] = 'Cursos para ti'
        context['owned'] = user.mycourses
        context['my_certificates'] = user.certificate_set.all().count()
        return context

    def get_queryset(self):
        request = self.request
        qs = Course.objects.all().annotate(
            avg_rating=Avg('review__rating'),
            rating_num=Count('review')
            )
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(title__icontains=query)
        if user.is_authenticated():
            qs = qs.owned(user)
        return qs


class MyCoursesListView(LoginRequiredMixin, ListView):
    template_name = 'courses/dashboard.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(MyCoursesListView, self).get_context_data(*args, **kwargs)
        # print(dir(context.get('page_obj')))
        user = self.request.user
        context['categories_list'] = Category.objects.all()
        context['title'] = 'Mis cursos'
        context['owned'] = user.mycourses
        context['my_certificates'] = user.certificate_set.all().count()
        return context

    def get_queryset(self):
        user = self.request.user
        qs = Course.objects.filter(owned__user=user).owned(user)
        return qs


class MyCertificatesListView(LoginRequiredMixin, ListView):
    template_name = 'courses/certificates.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(MyCertificatesListView, self).get_context_data(*args, **kwargs)
        # print(dir(context.get('page_obj')))
        user = self.request.user
        context['categories_list'] = Category.objects.all()
        context['title'] = 'Mis certificados'
        context['owned'] = user.mycourses
        context['my_certificates'] = user.certificate_set.all().count()
        return context

    def get_queryset(self):
        user = self.request.user
        qs = Certificate.objects.filter(user=user)
        return qs


class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, slug=None):
        qs = Course.objects.filter(slug=slug).owned(self.request.user)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated():
                my_courses = user.mycourses
                print(my_courses)
                print(my_courses)
                print(my_courses)
                print(my_courses)
                # run transaction
                # if transaction successful:
                my_courses.courses.add(qs.first())
                return qs.first().lecture_set.first().get_absolute_url()
            return qs.first().lecture_set.first().get_absolute_url()
        return "/courses/"


class CreateCertificateView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, slug=None):
        course = Course.objects.filter(slug=slug).owned(self.request.user).first()
        if course:
            user = self.request.user
            if user.is_authenticated():
                certificate_exists, new_certificate = Certificate.objects.get_or_create(user=self.request.user, course=course)
                if new_certificate:
                    obj = Certificate.objects.get(user=self.request.user, course=course)                    
                    context = {'instance': obj}
                    pdf = render_to_pdf('courses/certificate_pdf_template.html', context)
                    print("1")
                    print("1")
                    print("1")
                    filename = "certificado-{}-{}.pdf".format(course.slug, obj.slug)
                    obj.pdf.save(filename, File(BytesIO(pdf.content)))
                return course.get_absolute_url()
                print("2")
                print("2")
                print("2")
            return course.get_absolute_url()
        return "/courses/"


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.filter(slug=self.kwargs['slug']).owned(self.request.user).first()
            obj = Certificate.objects.get(user=self.request.user, course=course)
            pdf = obj.pdf.path
            if self.request.GET.get('download'):
                # response = HttpResponse(open(pdf, 'rb'), content_type='application/pdf')
                response = FileResponse(open(pdf, 'rb'), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(obj.pdfname)
                return response
            return FileResponse(open(pdf, 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


@method_decorator(login_required, name='dispatch')
class LectureDetailView(View):
    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        obj = None
        qs = Course.objects.filter(slug=cslug).lectures().reviews().owned(request.user)
        # qs = Course.objects.filter(slug=cslug).topics().owned(self.request.user)
        if not qs.exists():
            raise Http404
        course_ = qs.first()
        # if request.user.is_authenticated():
        #     view_event, created = CourseViewEvent.objects.get_or_create(user=request.user, course=course_)
        #     if view_event:
        #         view_event.views += 1
        #         view_event.save()
        lectures_qs = course_.lecture_set.filter(slug=lslug)
        if not lectures_qs.exists():
            raise Http404
        obj = lectures_qs.first()
        # lectures = Topic.objects.get(title=obj.topic).lecture_set.all()
        lectures = Lecture.objects.filter(topic=obj.topic).lecture_seen(user=request.user, topic=obj.topic)
        # print('LECTURES')
        # print('LECTURES')
        # print('LECTURES')
        # print len("-------------------")
        # print(lectures.query)
        # for lecture in lectures:
        #     print lecture.title
        # print(len(db.connection.queries))
        # print("-------------------")
        next_ = Lecture.objects.filter(order__gt=obj.order, course=course_).order_by('order').first()
        previous_ = Lecture.objects.filter(order__lt=obj.order, course=course_).order_by('-order').first()
        if course_.review_set.all().exists():
            review = True
        else:
            review = False
        if request.user.is_authenticated() and course_.is_owner:
            mlqs= MyLecture.objects.filter(user=request.user, lecture=obj, topic=obj.topic).first()
            if not mlqs:
                 MyLecture.objects.create(user=request.user, lecture=obj, topic=obj.topic)
        context = {
            "object": obj,
            "course": course_,
            "lectures": lectures,
            "next_": next_,
            "previous_": previous_,
            "review": review
        }
        return render(request, "courses/lecture_detail.html", context)


class CourseDetailView(DetailView):
    #queryset = Course.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        # qs = Course.objects.filter(slug=slug).lectures().owned(self.request.user)
        self.qs = Course.objects.filter(slug=slug).topics().owned(self.request.user)
        if self.qs.exists():
            self.obj = self.qs.first()
            # ACTIVATE WHEN ANALYTICS IS READY
            # if self.request.user.is_authenticated():
            #     view_event, created = CourseViewEvent.objects.get_or_create(user=self.request.user, course=obj)
            #     if view_event:
            #         view_event.views += 1
            #         view_event.save()
            return self.obj
        raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        # print(dir(context.get('page_obj')))
        lecture_1 = self.obj.lecture_set.first()
        if self.obj.review_set.exists():
            review_list = self.obj.review_set.all()
        else:
            review_list = None
        try:
            certificate = Certificate.objects.get(user=self.request.user, course=self.obj)  
        except:
            certificate = None
        context['lecture_1'] = lecture_1
        context['review_list'] = review_list 
        context['certificate'] = certificate
        return context


@method_decorator(login_required, name='dispatch')
class ReviewView(SuccessMessageMixin, FormView):
    template_name = "courses/review.html"
    form_class = ReviewForm
    success_message = "¡Genial! tu reseña ha sido agregada al curso"

    # def get_success_url(self):
    #     if 'slug' in self.kwargs:
    #         slug = self.kwargs['slug']
    #         return reverse_lazy('courses:detail', kwargs={'slug':slug })
    #     else:
    #         return reverse_lazy('courses:list')

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            return reverse_lazy('courses:create-certificate', kwargs={'slug':slug })
        else:
            return reverse_lazy('courses:list')

    def get_context_data(self, **kwargs):
        context = super(ReviewView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_message(self, cleaned_data):
        return '¡Genial! tu reseña ha sido agregada al curso "<strong>{}</strong>"'.format(self.course)

    def form_valid(self, form):
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        self.course = Course.objects.get(slug=self.kwargs['slug'])
        Review.objects.create(course= self.course, user = self.request.user, comment=comment, rating=rating)
        return super(ReviewView, self).form_valid(form)


def signup_login_view(request, **kwargs):
    signup_form = SignUpForm()
    login_form = AuthenticationForm()
    if request.method == "POST":
        print(request.POST.get('submit'))
        if request.POST.get('submit') == 'sign_up':
            print('PASO 1')
            signup_form = SignUpForm(request.POST or None)
            if signup_form.is_valid():
                print('PASO 2')
                user = signup_form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                raw_password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                print('PASO 3')
                return redirect(reverse_lazy('courses:detail', kwargs={'slug':kwargs.get("courseslug")}))
            else:
                signup_form = SignUpForm(request.POST)
                login_form = AuthenticationForm()
    args = {
        'login_form': login_form,
        'signup_form': signup_form,
        'next': kwargs.get("courseslug")
        }            
    return render(request, 'registration/signup-login.html', args)