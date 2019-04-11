from PIL import Image, ImageOps
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.utils.translation import ugettext_lazy as _
User = get_user_model()

class UserEditForm(forms.ModelForm):
        # email = forms.EmailField()
        # category = forms.CharField(required=False, validators=[validate_category])
        class Meta:
            model = User
            fields = [ 
                        'first_name',
                        'last_name',
                        'email',
                        'username',
                        ]

            labels = {
                        'first_name': 'Primer nombre',
                        'last_name': 'Primer apellido',
                        'username': 'Nombre de usuario para Iniciar Sesión',
                    }

class UserGeneralSettingsEditForm(forms.ModelForm):
        # city    =   forms.ModelChoiceField(queryset=CityOptions.objects.all(), label = "Ciudad", to_field_name="city_name")

    class Meta:
        model = UserProfile
        fields  = [  
                    'birthday',
                    'phone',
                    'whatsapp',
                    'website',
                    'gender',
                    'country',
                    'city',
                    ]
        # # labels = {
        # #         'site_name': 'Nombre de tu Sucursal Digital',
        # #         'phone': 'Teléfono principal ej. +503 2502 6108',
        # #         'city': 'Ciudad',
        # #     }
        # widgets = {
        #     'site_keywords_tag': forms.Textarea(attrs={'rows': 2}),
        #     'site_description_tag': forms.Textarea(attrs={'rows': 4}),
        #     }
        # help_texts={'phone':'Prefijo internacional + código de área + número. Ej. +503 2502 6108'}
        error_messages = {
            'phone': {
                'invalid': "Ingresa un número de teléfono válido Ej. +503 2502 6108"
            },
            'whatsapp': {
                'invalid': "Ingresa un número de teléfono válido Ej. +503 7390 5006"
            }
        }


class UserDegreeSettingsEditForm(forms.ModelForm):
        # city    =   forms.ModelChoiceField(queryset=CityOptions.objects.all(), label = "Ciudad", to_field_name="city_name")

    class Meta:
        model = UserProfile
        fields  = [  
                    'degree',
                    'speciality',
                    'abbreviation',
                    'academic_abbreviation_visible',
                    ]
     

# class ProfilePictureForm(forms.ModelForm):
#     profile_picture = forms.ImageField(label=_('Actualizar foto de perfil:'),required=False, error_messages = {'invalid':_("Solo formatos de imagen válidos .PNG o .JPG")}, widget=forms.FileInput)
#     remove_photo = forms.BooleanField(label=_('Eliminar foto'), required=False) #REMOVED BECAUSE DIGITAL OCEAN SPACES

#     class Meta:
#         model  = UserProfile
#         fields = ['profile_picture',]

#     def save(self, commit=True):
#         _form = super(ProfilePictureForm, self).save()
#         if self.cleaned_data.get('profile_picture'):
#             try:
#                 image = Image.open(_form.profile_picture)
#                 width, height = image.size
#                 new_height = 300
#                 new_width = new_height * width / height
#                 size = (300, new_height * width / height)
#                 # resized_image = image.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
#                 resized_image = ImageOps.fit(image, (300, 300), Image.ANTIALIAS)
#                 resized_image.save(_form.profile_picture.path, optimize=True, quality=85)
#             except:
#                 pass
        
#         if self.cleaned_data.get('remove_photo'):   
#             try:
#                 os.unlink(_form.profile_picture.name)
#             except OSError:
#                 pass
#             _form.profile_picture = None
#         if commit:
#             _form.save()
#         return _form

class ProfilePictureForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    profile_picture = forms.ImageField(label=_('Actualizar foto de perfil:'),required=False, error_messages = {'invalid':_("Solo formatos de imagen válidos .PNG o .JPG")}, widget=forms.FileInput)


    class Meta:
        model  = UserProfile
        fields = ('profile_picture', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(ProfilePictureForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_picture)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
        print(resized_image)
        resized_image.save(photo.profile_picture.path)

        return photo


class AboutForm(forms.ModelForm):

        class Meta:
            model = UserProfile
            fields  = [  
                        'description',
                        ]
            widgets = {
                    'description': forms.Textarea(attrs={'rows': 15}),

                }