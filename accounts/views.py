import json
import datetime
from PIL import Image
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic import DetailView, UpdateView, View, FormView, ListView, CreateView, DeleteView
from .forms import (
                AboutForm,
                ProfilePictureForm,
                UserDegreeSettingsEditForm,
                UserEditForm,
                UserGeneralSettingsEditForm,
            )

from .models import UserProfile

# <---------------- EDIT SITE VIEWS --------------------->
User = get_user_model()

@method_decorator(login_required, name='dispatch')
class _PasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_url = reverse_lazy('sites:settings_account')
    success_message = "Tu contraseña ha sido actualizada"
    template_name = 'accounts/edit/edit_account.html'

    def get_context_data(self, *args, **kwargs):
        context = super(_PasswordChangeView, self).get_context_data(*args, **kwargs)
        # context['instructions'] = 'Tu contraseña no puede asemejarse a otra información personal, \
        # ni tampoco ser una clave utilizada comunmente. Debe contener al menos ocho caracteres \
        # y cambiarse de forma periódica.'
        return context


@method_decorator(login_required, name='dispatch')
class UserAccountUpdateView(SuccessMessageMixin, UpdateView):    
    model = User
    form_class = UserEditForm
    login_url = '/login/'
    template_name = 'accounts/edit/edit_account.html'
    success_url = reverse_lazy('accounts:settings_account')
    success_message = "Tus cambios han sido aplicados con éxito"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserAccountUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Credenciales'
        context['is_settings_credentials'] = 'active font-weight-bold'
        return context


@method_decorator(login_required, name='dispatch')
class UserGeneralUpdateView(SuccessMessageMixin, UpdateView):    
    model = UserProfile
    login_url = '/login/'
    template_name = 'accounts/edit/edit_account.html'
    success_url = reverse_lazy('accounts:settings_general')
    form_class  = UserGeneralSettingsEditForm
    success_message = "Tus cambios han sido aplicados con éxito"

    def get_object(self):
        self.profile = self.request.user.userprofile
        return self.profile

    # def get_form_class(self):
    #     form = BasicUserSiteEditForm
    #     if self.site.whatsapp_add_on or self.site.web_plan.plan_name == 'Avanzado' or self.site.web_plan.plan_name == 'Pro':
    #         form = AdvancedUserSiteEditForm
    #     return form

    def get_context_data(self, *args, **kwargs):
        context = super(UserGeneralUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Configuración general'
        context['is_settings_general'] = 'active font-weight-bold'
        # context['instructions'] = 'Actualiza tu información general.'
        return context


class ProfilePictureUploadView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    login_url = '/login/'
    form_class = ProfilePictureForm
    success_url = reverse_lazy('accounts:settings_profile_picture')
    success_message = "Tu fotografía de perfil ha sido actualizada"
    template_name = 'accounts/edit/edit_profile_picture.html'

    def get_object(self):
        self.profile = self.request.user.userprofile
        return self.profile

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePictureUploadView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Fotografía de perfil'
        context['is_foto_info'] = 'active font-weight-bold'
        context['instructions'] = 'Selecciona la imagen desde tu equipo o dispositivo.'
        context['modal_title'] = '¿Realmente deseas eliminar la imagen?'
        return context


@method_decorator(login_required, name='dispatch')
class AboutSettingsView(SuccessMessageMixin, UpdateView):
    model = UserProfile
    login_url = '/login/'
    form_class = AboutForm
    success_url = reverse_lazy('accounts:settings_about')
    success_message = "La sección Acerca de ha sido actualizada"
    template_name = 'accounts/edit/edit_site_about_section.html'
  
    def get_object(self):
        self.profile = self.request.user.userprofile
        return self.profile

    def get_success_message(self, cleaned_data): #IT ADDS BUTTONS TO DE SUCCESS MESSAGE BAR
        return 'La sección Acerca de ha sido actualizada'

    def get_context_data(self, *args, **kwargs):
        context = super(AboutSettingsView, self).get_context_data(*args, **kwargs)
        section_name = 'Acerca de'
        context['title'] = section_name
        context['is_about_information'] = 'active font-weight-bold'        
        context['instructions'] = 'Añade una breve descripción a tu perfil.'
        return context


@method_decorator(login_required, name='dispatch')
class UserDegreeUpdateView(SuccessMessageMixin, UpdateView):    
    model = UserProfile
    login_url = '/login/'
    template_name = 'accounts/edit/edit_account.html'
    success_url = reverse_lazy('accounts:settings_degree')
    form_class  = UserDegreeSettingsEditForm
    success_message = "Tus cambios han sido aplicados con éxito"

    def get_object(self):
        self.profile = self.request.user.userprofile
        return self.profile

    # def get_form_class(self):
    #     form = BasicUserSiteEditForm
    #     if self.site.whatsapp_add_on or self.site.web_plan.plan_name == 'Avanzado' or self.site.web_plan.plan_name == 'Pro':
    #         form = AdvancedUserSiteEditForm
    #     return form

    def get_context_data(self, *args, **kwargs):
        context = super(UserDegreeUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Configuración grado académico'
        context['is_settings_degree'] = 'active font-weight-bold'
        # context['instructions'] = 'Actualiza tu información general.'
        return context


class UserProfileView(DetailView):
    model = UserProfile

    template_name = 'accounts/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        # context['user_post_list'] = Post.objects.filter(author=self.object.user).order_by("-created_at")[:5]
        return context


