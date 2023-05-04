from django.contrib.auth.forms import AdminPasswordChangeForm


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].password_validators = []  # Очистка списка валидаторов пароля

	def clean_password2(self):
		"""
		Отключение проверки сложности пароля.
		"""
		password1 = self.cleaned_data.get('password1')
		return password1
