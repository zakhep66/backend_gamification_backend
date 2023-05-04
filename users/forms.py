from django.contrib.auth.forms import AdminPasswordChangeForm


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

	def clean_password2(self):
		"""
		Отключение проверки сложности пароля.
		"""
		password1 = self.cleaned_data.get('password1')
		return password1
