from django import forms

from .models import Post
from .models import Comment

#class Post(forms.Form):
	
class PostForm(forms.ModelForm):
	content=forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
	class Meta:
		model=Post
		fields=[
			"content",   #This is the field shown in the form
		]

class CommentForm(forms.ModelForm):
	content=forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
	class Meta:
		model=Comment
		fields=[
			"content",
		]