from django import forms
from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):    # For validation
		username=self.cleaned_data.get("username")
		password=self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username,password=password)   #Checking whether the user exists in the database
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(UserLoginForm, self).clean(*args, **kwargs)   #return the default i.e. data for the form  


class UserRegistrationForm(forms.ModelForm):
	last_name=forms.CharField()
	email=forms.EmailField(label='Email addresss')
	password=forms.CharField(widget=forms.PasswordInput)  # the widget hides the password
	# email2=forms.EmailField(label='Confirm Email')
	password2=forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
	phone=forms.CharField(min_length=11,max_length=11,label='Phone Number',help_text="Format: 01*********")
	class Meta:
		model= User
		fields= [
			'first_name','last_name','username','password','password2','email','phone'
		]
	def clean_password2(self):
		password= self.cleaned_data.get('password')
		password2= self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Passwords must match")
		return password
	def clean_email(self):
		email=self.cleaned_data.get('email')
		email_qs= User.objects.filter(email=email)  # searches for same email as the input
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username']
