from django import forms
from core import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs=dict(required=True, max_length=30, placeholder='На какой email вам выставлять счет')
		), label=_("Email адрес"), error_messages={ 'invalid': _('Email уже существует') })
	
	password1 = forms.CharField(
		widget=forms.PasswordInput(
			attrs=dict(required=True, max_length=30,
				render_value=False, placeholder='Придумайте надежный пароль')
			),
			label=_("Пароль"),
			error_messages={ 'invalid': _('Пароли не совпадают') }
	)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30,
																	  render_value=False, placeholder='Повторите его еще раз')), label=_("Пароль (еще раз)"))
	name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30, placeholder='Представьтесь, пожалуйста')),
								label=_('Имя'),
								error_messages={ 'invalid': _('Имя может содержать только буквы') })

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("Пароли не совпадают."))

		email = self.cleaned_data.get('email', None)

		if not email:
			# if models.User.objects.filter(mobile_phone__exact=phone).exists():
			#         raise forms.ValidationError(_("Пользователь с таким номером телефона уже существует."))
			raise forms.ValidationError(_("Ошибка сервера, обновите страницу."))
		else:
			if models.User.objects.filter(email__iexact=email).exists():
					raise forms.ValidationError(_("Пользователь с таким email адресом уже существует."))

		return self.cleaned_data