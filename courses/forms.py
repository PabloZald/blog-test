from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from videos.models import Video
from .models import Course, Topic, Lecture, Review

User = get_user_model()

class SignUpForm(UserCreationForm):    
    # template = forms.ModelChoiceField(queryset=Template.objects.all(), widget=forms.RadioSelect(), required=True)
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

        help_text= {
                'username': 'Escribe un nombre de usuario para registrarte e iniciar sesión',
            }
        labels = {
                    'username': 'Nombre de usuario para ingresar a tu cuenta',
                }



class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'topic',
            'order',
            'title',
            'free',
            'video',
            'description',
            'slug', 
        ]
    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        qs = Video.objects.all().unused()
        qs_t = Topic.objects.all().unused()
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
            if obj.topic:    
                this_topic = Topic.objects.filter(pk=obj.topic.pk)
                qs_t = this_topic
            self.fields['topic'].queryset = qs_t
        else:
            self.fields['video'].queryset = qs
            self.fields['topic'].queryset = qs_t


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = forms.ChoiceField(choices=RATING_CHOICES,widget=forms.RadioSelect)
    
    class Meta:
        model = Review
        fields = [
            'rating',
            'comment',
        ]

    widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class CourseForm(forms.ModelForm):
    # number = forms.IntegerField()
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'slug',
            'price',

        ]

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        qs = Course.objects.filter(slug=slug)
        if qs.count() > 1:
            raise forms.ValidationError("Slug must be unique")
        return slug


class SignupFormStep1(UserCreationForm):    
    # template = forms.ModelChoiceField(queryset=Template.objects.all(), widget=forms.RadioSelect(), required=True)
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

        help_text= {
                'username': 'Escribe un nombre de usuario para registrarte e iniciar sesión',
            }
        labels = {
                    'username': 'Nombre de usuario para ingresar a tu cuenta',
                }


class SignupFormStep2(forms.Form):    
    # template = forms.ModelChoiceField(queryset=Template.objects.all(), widget=forms.RadioSelect(), required=True)
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    first_name = forms.CharField(required=True, label=_('Primer nombre'), max_length=50,)
    last_name = forms.CharField(required=True, label=_('Primer apellido'), max_length=50,)
    email = forms.EmailField(required=True, label=_('Email'), max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('Parece que ese correo ya ha sido registrado intenta con otro'))
        return email
